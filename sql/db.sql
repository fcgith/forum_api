-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema forum
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema forum
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forum` DEFAULT CHARACTER SET utf8 ;
USE `forum` ;

-- -----------------------------------------------------
-- Table `forum`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `birthday` DATE NOT NULL,
  `avatar` TINYTEXT NULL,
  `admin` TINYINT NOT NULL DEFAULT 0,
  `creation_date` DATE NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum`.`categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum`.`topics` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `content` MEDIUMTEXT NOT NULL,
  `date` DATE NOT NULL DEFAULT NOW(),
  `category_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `category_id`, `user_id`),
  INDEX `fk_topics_categories_idx` (`category_id` ASC) VISIBLE,
  INDEX `fk_topics_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_topics_categories`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum`.`replies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` TEXT(16800) NOT NULL,
  `date` DATE NOT NULL DEFAULT NOW(),
  `topic_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `topic_id`, `user_id`),
  INDEX `fk_replies_topics1_idx` (`topic_id` ASC) VISIBLE,
  INDEX `fk_replies_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_replies_topics1`
    FOREIGN KEY (`topic_id`)
    REFERENCES `forum`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum`.`conversations`
-- -----------------------------------------------------
... (91 lines left)