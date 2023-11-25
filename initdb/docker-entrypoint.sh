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
-- Table `mydb`.`USUARIOS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`USUARIOS` (
  `IDUSUARIOS` INT NOT NULL,
  `NOMEUSU` VARCHAR(45) NULL,
  `LOGIN` VARCHAR(45) NOT NULL,
  `SENHA` VARCHAR(45) NOT NULL,
  `DTCRIACAO` DATE NOT NULL,
  PRIMARY KEY (`IDUSUARIOS`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ENDERECO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ENDERECO` (
  `IDENDERECO` INT NOT NULL,
  `ENDERCO` VARCHAR(100) NULL,
  `TIPO` VARCHAR(45) NULL,
  PRIMARY KEY (`IDENDERECO`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`BAIRRO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`BAIRRO` (
  `IDBAIRRO` INT NOT NULL,
  `BAIRRO` VARCHAR(70) NULL,
  PRIMARY KEY (`IDBAIRRO`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ESTADO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ESTADO` (
  `IDESTADO` INT NOT NULL,
  `ESTADO` VARCHAR(45) NULL,
  `SIGLA` VARCHAR(2) NULL,
  PRIMARY KEY (`IDESTADO`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`CIDADE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`CIDADE` (
  `IDCIDADE` INT NOT NULL,
  `CIDADE` VARCHAR(45) NOT NULL,
  `IDESTADO` INT NULL,
  `ESTADO_IDESTADO` INT NOT NULL,
  CONSTRAINT `fk_CIDADE_ESTADO1`
    FOREIGN KEY (`ESTADO_IDESTADO`)
    REFERENCES `mydb`.`ESTADO` (`IDESTADO`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`CLIENTES`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`CLIENTES` (
  `IDCLIENTES` INT NOT NULL,
  `NOMECLIENTE` VARCHAR(70) NOT NULL,
  `CPF` VARCHAR(11) NULL,
  `ENDERECO_IDENDERECO` INT NOT NULL,
  `BAIRRO_IDBAIRRO` INT NOT NULL,
  `IDCIDADE` INT NULL,
  `SIGLAESTADO` VARCHAR(45) NULL,
  `TELEFONE` VARCHAR(11) NULL,
  `EMAIL` VARCHAR(70) NULL,
  `PONTOREF` VARCHAR(100) NULL,
  PRIMARY KEY (`IDCLIENTES`),
  CONSTRAINT `fk_CLIENTES_ENDERECO`
    FOREIGN KEY (`ENDERECO_IDENDERECO`)
    REFERENCES `mydb`.`ENDERECO` (`IDENDERECO`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_CLIENTES_BAIRRO1`
    FOREIGN KEY (`BAIRRO_IDBAIRRO`)
    REFERENCES `mydb`.`BAIRRO` (`IDBAIRRO`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_CIDADE_IDCIDADE`
    FOREIGN KEY (`IDCIDADE`)
    REFERENCES `mydb`.`CIDADE` (`IDCIDADE`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`UNIDADES`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`UNIDADES` (
  `IDUNIDADE` INT NOT NULL,
  `DESCRICAO` VARCHAR(45) NULL,
  `SIGLA` VARCHAR(5) NULL,
  PRIMARY KEY (`IDUNIDADE`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`PRODUTO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`PRODUTO` (
  `IDPRODUTO` INT NOT NULL,
  `DESCRICAO` VARCHAR(100) NULL,
  `UNIDADES_IDUNIDADE` INT NOT NULL,
  `VALORCOMPRA` DECIMAL(10) NULL,
  `VALORVENDA` DECIMAL(10) NULL,
  PRIMARY KEY (`IDPRODUTO`),
  CONSTRAINT `fk_PRODUTO_UNIDADES1`
    FOREIGN KEY (`UNIDADES_IDUNIDADE`)
    REFERENCES `mydb`.`UNIDADES` (`IDUNIDADE`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ESTOQUE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ESTOQUE` (
  `IDESTOQUE` INT NOT NULL,
  `PRODUTO_IDPRODUTO` INT NOT NULL,
  `QTDE` DECIMAL(10) NULL,
  PRIMARY KEY (`IDESTOQUE`),
  CONSTRAINT `fk_ESTOQUE_PRODUTO1`
    FOREIGN KEY (`PRODUTO_IDPRODUTO`)
    REFERENCES `mydb`.`PRODUTO` (`IDPRODUTO`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`FORMAPAG`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`FORMAPAG` (
  `IDFORMAPAG` INT NOT NULL,
  `DESCRICAO` VARCHAR(60) NULL,
  PRIMARY KEY (`IDFORMAPAG`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`PEDIDO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`PEDIDO` (
  `IDPEDIDO` INT NOT NULL,
  `IDCLIENTE` INT NULL,
  `QTDE` DECIMAL(10) NULL,
  `PRODUTO_IDPRODUTO` INT NOT NULL,
  `DTPEDIDO` DATE NULL,
  `VALORPEDIDO` DECIMAL(10) NULL,
  `FORMAPAG_IDFORMAPAG` INT NOT NULL,
  `CLIENTES_IDCLIENTES` INT NOT NULL,
  PRIMARY KEY (`IDPEDIDO`),
  CONSTRAINT `fk_PEDIDO_PRODUTO1`
    FOREIGN KEY (`PRODUTO_IDPRODUTO`)
    REFERENCES `mydb`.`PRODUTO` (`IDPRODUTO`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PEDIDO_FORMAPAG1`
    FOREIGN KEY (`FORMAPAG_IDFORMAPAG`)
    REFERENCES `mydb`.`FORMAPAG` (`IDFORMAPAG`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PEDIDO_CLIENTES1`
    FOREIGN KEY (`CLIENTES_IDCLIENTES`)
    REFERENCES `mydb`.`CLIENTES` (`IDCLIENTES`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ENTREGA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ENTREGA` (
  `IDENTREGA` INT NOT NULL,
  `IDCLIENTE` INT NULL,
  `PEDIDO_IDPEDIDO` INT NOT NULL,
  `CLIENTES_IDCLIENTES` INT NOT NULL,
  PRIMARY KEY (`IDENTREGA`),
  CONSTRAINT `fk_ENTREGA_PEDIDO1`
    FOREIGN KEY (`PEDIDO_IDPEDIDO`)
    REFERENCES `mydb`.`PEDIDO` (`IDPEDIDO`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ENTREGA_CLIENTES1`
    FOREIGN KEY (`CLIENTES_IDCLIENTES`)
    REFERENCES `mydb`.`CLIENTES` (`IDCLIENTES`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
