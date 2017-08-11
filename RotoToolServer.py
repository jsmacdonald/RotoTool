from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'rotoAdmin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rotoAdmin'
app.config['MYSQL_DATABASE_DB'] = 'rotodrafts'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    
    try: # read the posted values from the UI
        _name = request.form['inputName']
        _username = request.form['inputUserName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
     
        # validate the received values
        if _name and _email and _password and _username:
            #Things are good, let's get to calling mySQL
            #connect to the sql db and define a cursor
            conn = mysql.connect()
            cursor = conn.cursor()

            #salt our passwords
            _hashed_password = generate_password_hash(_password)

            #Call the a predefined query structure (sp_createUser) that we have already defined in the DB
            cursor.callproc('sp_createUser',(_name,_username,_email,_hashed_password))

            #If it was sucessful, commit our changes to the DB Table
            data = cursor.fetchall()
             
            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    
    except Exception as e:
        return json.dumps({'error':str(e)})

    finally:
        cursor.close() 
        conn.close()


@app.route('/getcards/<string:card>')
def MagicCards(card):
    # Using code from my viscuber to evaluate a card name and find it on gatherer
    #static strings
    String1 = '<ul><li data-checked="true"><a href="http://gatherer.wizards.com/Pages/Card/Details.aspx?name='
    String2 = '"><img src="http://gatherer.wizards.com/Handlers/Image.ashx?name='
    String3 = '&amp;set='
    String4 = '&amp;type=card" alt="'
    StringEnd = '"></a></li></ul>\n'
    
    #separate card name from parentheticals (the first should include the set code)
    card0=card.split('(')
    if len(card0)>1:
        setcode = card0[1].strip()
        setcode = setcode[:-1]
        #print setcode
    else:
        setcode=''

    #Create the strings for cardname and cardhtml for url use 
    cardname = card0[0].strip()
    cardhtml = cardname
    ## Replace commas
    cardhtml=cardhtml.replace(",","%2C")
    ## Replace //
    cardhtml=cardhtml.replace("/","%2F")
    ## Replace Spaces
    cardhtml=cardhtml.replace(" ","%20")
    #print cardhtml
    htmlString = String1 + cardhtml + String2 + cardhtml + String3 + setcode + String4 + cardname + StringEnd
    return htmlString

if __name__ == "__main__":
    app.run(port=5000)
