-- MySQL Script generated by MySQL Workbench
-- Thu Mar  8 23:00:00 2018
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema cucumber
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema cucumber
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cucumber` DEFAULT CHARACTER SET utf8mb4 ;
SHOW WARNINGS;
USE `cucumber` ;

-- -----------------------------------------------------
-- Table `cucumber`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cucumber`.`users` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `cucumber`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` BINARY(60) NOT NULL,
  `is_admin` INT NOT NULL DEFAULT 0,
  `created_at` DATETIME(6) NOT NULL,
  `updated_at` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE UNIQUE INDEX `email_UNIQUE` ON `cucumber`.`users` (`email` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `cucumber`.`books`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cucumber`.`books` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `cucumber`.`books` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `author` VARCHAR(255) NULL,
  `publisher` VARCHAR(255) NULL,
  `isbn13` VARCHAR(13) NOT NULL,
  `language` VARCHAR(63) NULL,
  `price` DECIMAL(10) NOT NULL,
  `reldate` DATETIME(6) NULL,
  `shelf` VARCHAR(63) NULL,
  `classify` VARCHAR(63) NULL,
  `description` TEXT NULL,
  `picture` VARCHAR(512) NULL,
  `created_at` DATETIME(6) NOT NULL,
  `updated_at` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `cucumber`.`stock_types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cucumber`.`stock_types` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `cucumber`.`stock_types` (
  `type` VARCHAR(63) NOT NULL COMMENT 'sold, returned, reserved',
  PRIMARY KEY (`type`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `cucumber`.`stocks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cucumber`.`stocks` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `cucumber`.`stocks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `book_id` INT NOT NULL,
  `type` VARCHAR(63) NOT NULL,
  `created_at` DATETIME(6) NOT NULL,
  `updated_at` DATETIME(6) NOT NULL,
  `price` DECIMAL(10,0) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_stocks_books1`
    FOREIGN KEY (`book_id`)
    REFERENCES `cucumber`.`books` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_stocks_stock_types1`
    FOREIGN KEY (`type`)
    REFERENCES `cucumber`.`stock_types` (`type`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_stocks_books1_idx` ON `cucumber`.`stocks` (`book_id` ASC);

SHOW WARNINGS;
CREATE INDEX `fk_stocks_stock_types1_idx` ON `cucumber`.`stocks` (`type` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `cucumber`.`returned`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cucumber`.`returned` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `cucumber`.`returned` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stock_id` INT NOT NULL,
  `remarks` TEXT NULL,
  `created_at` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_returned_stocks_stocks1`
    FOREIGN KEY (`stock_id`)
    REFERENCES `cucumber`.`stocks` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_returned_stocks_stocks1_idx` ON `cucumber`.`returned` (`stock_id` ASC);

SHOW WARNINGS;
CREATE UNIQUE INDEX `stock_id_UNIQUE` ON `cucumber`.`returned` (`stock_id` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `cucumber`.`sold`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cucumber`.`sold` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `cucumber`.`sold` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stock_id` INT NOT NULL,
  `remarks` TEXT NULL,
  `created_at` DATETIME(6) NOT NULL,
  `price` DECIMAL(10,0) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_sold_stocks_stocks1`
    FOREIGN KEY (`stock_id`)
    REFERENCES `cucumber`.`stocks` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_sold_stocks_stocks1_idx` ON `cucumber`.`sold` (`stock_id` ASC);

SHOW WARNINGS;
CREATE UNIQUE INDEX `stock_id_UNIQUE` ON `cucumber`.`sold` (`stock_id` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `cucumber`.`order_statuses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cucumber`.`order_statuses` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `cucumber`.`order_statuses` (
  `status` VARCHAR(45) NOT NULL,
  `status_group` INT NOT NULL,
  PRIMARY KEY (`status`, `status_group`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `cucumber`.`orders`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cucumber`.`orders` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `cucumber`.`orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `book_id` INT NOT NULL,
  `stock_id` INT NULL,
  `user_id` INT NOT NULL,
  `latest_status` VARCHAR(45) NOT NULL,
  `created_at` DATETIME(6) NOT NULL,
  `updated_at` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `cucumber`.`users` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `book_id`
    FOREIGN KEY (`book_id`)
    REFERENCES `cucumber`.`books` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `status`
    FOREIGN KEY (`latest_status`)
    REFERENCES `cucumber`.`order_statuses` (`status`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `stock_id`
    FOREIGN KEY (`stock_id`)
    REFERENCES `cucumber`.`stocks` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `user_idx` ON `cucumber`.`orders` (`user_id` ASC);

SHOW WARNINGS;
CREATE INDEX `book_idx` ON `cucumber`.`orders` (`book_id` ASC);

SHOW WARNINGS;
CREATE INDEX `status_idx` ON `cucumber`.`orders` (`latest_status` ASC);

SHOW WARNINGS;
CREATE INDEX `stock_id_idx` ON `cucumber`.`orders` (`stock_id` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `cucumber`.`order_events`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cucumber`.`order_events` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `cucumber`.`order_events` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  `created_at` DATETIME(6) NOT NULL,
  `remarks` TEXT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `order_id`
    FOREIGN KEY (`order_id`)
    REFERENCES `cucumber`.`orders` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `order_status`
    FOREIGN KEY (`status`)
    REFERENCES `cucumber`.`order_statuses` (`status`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `id_idx` ON `cucumber`.`order_events` (`order_id` ASC);

SHOW WARNINGS;
CREATE INDEX `status_idx` ON `cucumber`.`order_events` (`status` ASC);

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `cucumber`.`stock_types`
-- -----------------------------------------------------
START TRANSACTION;
USE `cucumber`;
INSERT INTO `cucumber`.`stock_types` (`type`) VALUES ('instock');
INSERT INTO `cucumber`.`stock_types` (`type`) VALUES ('returned');
INSERT INTO `cucumber`.`stock_types` (`type`) VALUES ('sold');
INSERT INTO `cucumber`.`stock_types` (`type`) VALUES ('reserved');

COMMIT;


-- -----------------------------------------------------
-- Data for table `cucumber`.`order_statuses`
-- -----------------------------------------------------
START TRANSACTION;
USE `cucumber`;
INSERT INTO `cucumber`.`order_statuses` (`status`, `status_group`) VALUES ('引き取り済み', 1);
INSERT INTO `cucumber`.`order_statuses` (`status`, `status_group`) VALUES ('仕入れ承認待機', 2);
INSERT INTO `cucumber`.`order_statuses` (`status`, `status_group`) VALUES ('取り寄せ承認待機', 2);
INSERT INTO `cucumber`.`order_statuses` (`status`, `status_group`) VALUES ('取り置き承認待機', 2);
INSERT INTO `cucumber`.`order_statuses` (`status`, `status_group`) VALUES ('仕入れ待機', 2);
INSERT INTO `cucumber`.`order_statuses` (`status`, `status_group`) VALUES ('引き取り待機', 2);
INSERT INTO `cucumber`.`order_statuses` (`status`, `status_group`) VALUES ('仕入れ却下', 3);
INSERT INTO `cucumber`.`order_statuses` (`status`, `status_group`) VALUES ('取り寄せ却下', 3);
INSERT INTO `cucumber`.`order_statuses` (`status`, `status_group`) VALUES ('取り置き却下', 3);
INSERT INTO `cucumber`.`order_statuses` (`status`, `status_group`) VALUES ('引き取り却下', 3);

COMMIT;

