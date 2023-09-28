CREATE TABLE `live_ticketing_db`.`tickets` (
  `ticket_id` INT AUTO_INCREMENT PRIMARY KEY,
  `assigned_to` INT NULL,
  `status` TINYINT NULL,
  `start_date` DATETIME NULL,
  `close_date` DATETIME NULL,
  `department` INT NULL,
  `description` VARCHAR(3072) NULL
);

CREATE TABLE `live_ticketing_db`.`employees` (
  `employees_id` INT AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `department` INT UNSIGNED NOT NULL,
  `position` VARCHAR(45) NULL,
  PRIMARY KEY (`employees_id`),
  UNIQUE INDEX `employees_id_UNIQUE` (`employees_id` ASC)
);

CREATE TABLE `live_ticketing_db`.`department` (
  `dept_id` INT AUTO_INCREMENT PRIMARY KEY,
  `dept_name` VARCHAR(256) NULL
);

CREATE TABLE `live_ticketing_db`.`tasks` (
	`task_id` INT AUTO_INCREMENT PRIMARY KEY,
    `description` VARCHAR(3072),
    `ticket_id` INT,
    `status` INT,
    `assigned_to` INT NOT NULL,
    `assigned_date` DATETIME
);

ALTER TABLE `employees`
  ADD UNIQUE INDEX `email_UNIQUE` (`email`);

ALTER TABLE live_ticketing_db.department
	ADD UNIQUE INDEX `dept_name_UNIQUE` (`dept_name`);
