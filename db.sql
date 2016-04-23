use `sms_db`;

CREATE TABLE `users`(
	`id` INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`username` VARCHAR(30) NOT NULL UNIQUE,
	`passwd` CHAR(32) NOT NULL,
	`hostname` VARCHAR(50) NOT NULL,
	`portnum` VARCHAR(10) NOT NULL
);