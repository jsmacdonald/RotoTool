CREATE TABLE `rotodrafts`.`draft_users` (
  `user_id` BIGINT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) NULL,
  `user_username` VARCHAR(45) NULL,
  `user_email` VARCHAR(45) NULL,
  `user_password` VARCHAR(45) NULL,
  UNIQUE KEY (`user_id`));

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(45),
    IN p_username VARCHAR(45),
    IN p_email VARCHAR(45),
    IN p_password VARCHAR(45)
)
BEGIN
    if ( select exists (select 1 from draft_users where user_username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into draft_users
        (
            user_name,
            user_username,
            user_email,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_email,
            p_password
        );
     
    END IF;
END$$
DELIMITER ;