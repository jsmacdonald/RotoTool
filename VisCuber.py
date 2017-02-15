## This is a super basic python code that will read in a list of cards and convert each card into it's own visual cube html call.

# Create the html string that will show the card, sans the card's name.  This will be in 4 parts.
String1 = '<li data-checked="true"><a href="http://gatherer.wizards.com/Pages/Card/Details.aspx?name="'
String2 = '"><img src="http://gatherer.wizards.com/Handlers/Image.ashx?name='
String3 = '&amp;set=&amp;type=card" alt="'
StringEnd = '"></a></li>\n'

# Now let's open the input file and read the contents, then create the output
InputFN = 'Input.txt'
OutputFN = 'Output.txt'

InputFile = open(InputFN, 'r')
OutputFile = open(OutputFN, 'w')
#print InputFile.read()
for card in InputFile:
    #print card
    card1 = card.strip()
    cardhtml = card1
    ## Replace commas
    cardhtml=cardhtml.replace(",","%2C")
    ## Replace //
    cardhtml=cardhtml.replace("/","%2F")
    ## Replace Spaces
    cardhtml=cardhtml.replace(" ","%20")
    #print cardhtml
    htmlString = String1 + cardhtml + String2 + cardhtml + String3 + card1 + StringEnd
    OutputFile.write(htmlString)

InputFile.close()
OutputFile.close()