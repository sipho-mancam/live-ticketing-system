CREATE DATABASE live_ticketing_db;

CREATE TABLE `live_ticketing_db`.`tickets` (
  `ticket_id` INT AUTO_INCREMENT PRIMARY KEY,
  `assigned_to` INT NULL,
  `status` TINYINT NULL,
  `start_date` DATETIME NULL,
  `close_date` DATETIME NULL,
  `department` INT NULL,
  `description` VARCHAR(3072) NULL,
  `owner` INT NULL
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

CREATE TABLE `live_ticketing_db`.`events_tracker` (
  `event_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  `ticket_id` INT NOT NULL,
  `object` INT NOT NULL,
  `action` INT NOT NULL,
  `time_stamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `employee_id` INT NULL
  );

CREATE TABLE `live_ticketing_db`.`event_objects` (
  `object_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  `object_name` VARCHAR(255) NULL);

CREATE TABLE `live_ticketing_db`.`event_action` (
  `action_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `action_name` VARCHAR(255) NOT NULL);


CREATE TABLE `live_ticketing_db`.`email_templates` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `template_name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`));


  CREATE TABLE `live_ticketing_db`.`email_records` (
  `email_id` INT NOT NULL AUTO_INCREMENT,
  `subject` VARCHAR(255) NOT NULL,
  `template` INT NOT NULL,
  `recipient` INT NOT NULL,
  `ticket_id` INT NOT NULL,
  `status` TINYINT NOT NULL,
  `actuator` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`email_id`),
  INDEX `fk_template_idx` (`template` ASC) VISIBLE,
  INDEX `fk_employee_idx` (`recipient` ASC) VISIBLE,
  INDEX `fk_ticket_idx` (`ticket_id` ASC) VISIBLE,
  CONSTRAINT `fk_template`
    FOREIGN KEY (`template`)
    REFERENCES `live_ticketing_db`.`email_templates` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_employee`
    FOREIGN KEY (`recipient`)
    REFERENCES `live_ticketing_db`.`employees` (`employees_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ticket`
    FOREIGN KEY (`ticket_id`)
    REFERENCES `live_ticketing_db`.`tickets` (`ticket_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);



ALTER TABLE `live_ticketing_db`.`events_tracker` 
ADD INDEX `tickets_idx` (`ticket_id` ASC) VISIBLE;
;
ALTER TABLE `live_ticketing_db`.`events_tracker` 
ADD CONSTRAINT `tickets_fk`
  FOREIGN KEY (`ticket_id`)
  REFERENCES `live_ticketing_db`.`tickets` (`ticket_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;


ALTER TABLE `live_ticketing_db`.`events_tracker` 
ADD INDEX `e_employee_idx` (`employee_id` ASC) VISIBLE;
;
ALTER TABLE `live_ticketing_db`.`events_tracker` 
ADD CONSTRAINT `e_employee`
  FOREIGN KEY (`employee_id`)
  REFERENCES `live_ticketing_db`.`employees` (`employees_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `live_ticketing_db`.`events_tracker` 
ADD INDEX `e_action_idx` (`action` ASC) VISIBLE;
;
ALTER TABLE `live_ticketing_db`.`events_tracker` 
ADD CONSTRAINT `e_action`
  FOREIGN KEY (`action`)
  REFERENCES `live_ticketing_db`.`event_action` (`action_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `live_ticketing_db`.`events_tracker` 
ADD CONSTRAINT `e_objects`
  FOREIGN KEY (`object`)
  REFERENCES `live_ticketing_db`.`event_objects` (`object_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;


CREATE TABLE `live_ticketing_db`.`user_filter` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `employee_id` INT NULL,
  `filter_query` VARCHAR(1024) NULL,
  PRIMARY KEY (`id`),
  INDEX `employee_idx` (`employee_id` ASC) VISIBLE,
  CONSTRAINT `employee`
    FOREIGN KEY (`employee_id`)
    REFERENCES `live_ticketing_db`.`employees` (`employees_id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION);


INSERT INTO live_ticketing_db.event_objects (object_name)
	VALUES ("Ticket"), ("Task");

INSERT INTO `live_ticketing_db`.`event_action` (action_name)
	VALUES ("CREATED"),
		    ("OPENED"),
        ("CLOSED"),
        ("ASSIGNED"),
        ("DELETED");


INSERT INTO live_ticketing_db.email_templates (template_name)
	VALUES ("ticket_closed.html"),("ticket_assigned.html"), ("task_assigned.html")


ALTER TABLE `live_ticketing_db`.`employees`
  ADD UNIQUE INDEX `email_UNIQUE` (`email`);

ALTER TABLE `live_ticketing_db`.`department`
	ADD UNIQUE INDEX `dept_name_UNIQUE` (`dept_name`);

ALTER TABLE `live_ticketing_db`.`department`
  ADD COLUMN `manager` INT NOT NULL;

ALTER TABLE `live_ticketing_db`.`tickets` 
ADD INDEX `deps_idx` (`department` ASC) VISIBLE,
ADD INDEX `emps_idx` (`owner` ASC, `assigned_to` ASC) VISIBLE;
;

ALTER TABLE `live_ticketing_db`.`tickets` 
ADD CONSTRAINT `deps`
  FOREIGN KEY (`department`)
  REFERENCES `live_ticketing_db`.`department` (`dept_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `live_ticketing_db`.`tickets` 
ADD CONSTRAINT `emps`
  FOREIGN KEY (`owner` )
  REFERENCES `live_ticketing_db`.`employees` (`employees_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `live_ticketing_db`.`tickets` 
ADD CONSTRAINT `assigned`
  FOREIGN KEY ( `assigned_to`)
  REFERENCES `live_ticketing_db`.`employees` (`employees_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `live_ticketing_db`.`tasks` 
ADD INDEX `tickets_idx` (`ticket_id` ASC) VISIBLE;
;
ALTER TABLE `live_ticketing_db`.`tasks` 
ADD CONSTRAINT `tickets`
  FOREIGN KEY (`ticket_id`)
  REFERENCES `live_ticketing_db`.`tickets` (`ticket_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;