-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Student` (
  `Permissions` TINYINT NOT NULL,
  `NetID` VARCHAR(11) NOT NULL,
  `FirstName` VARCHAR(15) NOT NULL,
  `LastName` VARCHAR(15) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `Password` VARCHAR(18) NULL,
  PRIMARY KEY (`NetID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Professor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Professor` (
  `ProfessorNetID` VARCHAR(15) NOT NULL,
  `FirstName` VARCHAR(15) NOT NULL,
  `LastName` VARCHAR(15) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `Password` VARCHAR(18) NULL,
  PRIMARY KEY (`ProfessorNetID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Class`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Class` (
  `ClassName` VARCHAR(50) NOT NULL,
  `ClassID` INT NOT NULL,
  `sectionNumber` INT NOT NULL,
  `Size` INT NOT NULL,
  `Professor_ProfessorNetID` VARCHAR(15) NOT NULL,
  `ClassNumber` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`ClassID`),
  INDEX `fk_Class_Professor1_idx` (`Professor_ProfessorNetID` ASC) VISIBLE,
  CONSTRAINT `fk_Class_Professor1`
    FOREIGN KEY (`Professor_ProfessorNetID`)
    REFERENCES `mydb`.`Professor` (`ProfessorNetID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Enrollment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Enrollment` (
  `idEnrollment` INT NOT NULL AUTO_INCREMENT,
  `Student_NetID` VARCHAR(11) NOT NULL,
  `Class_ClassID` INT NOT NULL,
  PRIMARY KEY (`idEnrollment`),
  INDEX `fk_Enrollment_Student_idx` (`Student_NetID` ASC) VISIBLE,
  INDEX `fk_Enrollment_Class1_idx` (`Class_ClassID` ASC) VISIBLE,
  CONSTRAINT `fk_Enrollment_Student`
    FOREIGN KEY (`Student_NetID`)
    REFERENCES `mydb`.`Student` (`NetID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Enrollment_Class1`
    FOREIGN KEY (`Class_ClassID`)
    REFERENCES `mydb`.`Class` (`ClassID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`File`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`File` (
  `FileName` VARCHAR(45) NOT NULL,
  `FileType` VARCHAR(45) NOT NULL,
  `FileContent` LONGBLOB NOT NULL,
  `Class_ClassID` INT NOT NULL,
  INDEX `fk_File_Class1_idx` (`Class_ClassID` ASC) VISIBLE,
  PRIMARY KEY (`FileName`),
  CONSTRAINT `fk_File_Class1`
    FOREIGN KEY (`Class_ClassID`)
    REFERENCES `mydb`.`Class` (`ClassID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Thread`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Thread` (
  `Class_ClassID` INT NOT NULL,
  `ThreadID` INT NOT NULL AUTO_INCREMENT,
  `CreationDate` DATETIME NOT NULL,
  `ThreadContent` TINYTEXT NOT NULL,
  `Student_NetID` VARCHAR(11) NOT NULL,
  `ThreadTitle` VARCHAR(45) NOT NULL,
  INDEX `fk_Thread_Class1_idx` (`Class_ClassID` ASC) VISIBLE,
  PRIMARY KEY (`ThreadID`),
  INDEX `fk_Thread_Student1_idx` (`Student_NetID` ASC) VISIBLE,
  CONSTRAINT `fk_Thread_Class1`
    FOREIGN KEY (`Class_ClassID`)
    REFERENCES `mydb`.`Class` (`ClassID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Thread_Student1`
    FOREIGN KEY (`Student_NetID`)
    REFERENCES `mydb`.`Student` (`NetID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Reply`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Reply` (
  `Thread_ThreadID` INT NOT NULL,
  `CreationDate` DATETIME NOT NULL,
  `Content` TINYTEXT NOT NULL,
  `Student_NetID` VARCHAR(11) NOT NULL,
  INDEX `fk_Reply_Thread1_idx` (`Thread_ThreadID` ASC) VISIBLE,
  INDEX `fk_Reply_Student1_idx` (`Student_NetID` ASC) VISIBLE,
  CONSTRAINT `fk_Reply_Thread1`
    FOREIGN KEY (`Thread_ThreadID`)
    REFERENCES `mydb`.`Thread` (`ThreadID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Reply_Student1`
    FOREIGN KEY (`Student_NetID`)
    REFERENCES `mydb`.`Student` (`NetID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
