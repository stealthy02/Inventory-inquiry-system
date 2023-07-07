-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: billing_details
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cg_name_price`
--

DROP TABLE IF EXISTS `cg_name_price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cg_name_price` (
  `gname` varchar(20) NOT NULL,
  `cname` varchar(20) NOT NULL,
  `cg_price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`gname`,`cname`),
  CONSTRAINT `cg_name_price_ibfk_1` FOREIGN KEY (`gname`) REFERENCES `goods` (`gname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='客户商品价格';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cg_name_price`
--

LOCK TABLES `cg_name_price` WRITE;
/*!40000 ALTER TABLE `cg_name_price` DISABLE KEYS */;
/*!40000 ALTER TABLE `cg_name_price` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `go`
--

DROP TABLE IF EXISTS `go`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `go` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gname` varchar(20) NOT NULL,
  `cname` varchar(20) NOT NULL,
  `g_price` decimal(10,2) NOT NULL,
  `inv_price` decimal(10,2) NOT NULL,
  `g_qty_num` int NOT NULL,
  `g_qty_weight` decimal(10,4) NOT NULL,
  `g_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gname` (`gname`,`cname`),
  CONSTRAINT `go_ibfk_1` FOREIGN KEY (`gname`, `cname`) REFERENCES `cg_name_price` (`gname`, `cname`),
  CONSTRAINT `go_ibfk_2` FOREIGN KEY (`gname`) REFERENCES `goods` (`gname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='商品订单';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `go`
--

LOCK TABLES `go` WRITE;
/*!40000 ALTER TABLE `go` DISABLE KEYS */;
/*!40000 ALTER TABLE `go` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods`
--

DROP TABLE IF EXISTS `goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goods` (
  `gname` varchar(40) NOT NULL,
  `gtype` varchar(20) NOT NULL,
  `ply` decimal(10,4) NOT NULL,
  `width` decimal(10,4) NOT NULL,
  `inv_price` decimal(10,2) NOT NULL,
  `inv_qty_num` int NOT NULL,
  `inv_qty_weight` decimal(10,4) NOT NULL,
  PRIMARY KEY (`gname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='商品信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods`
--

LOCK TABLES `goods` WRITE;
/*!40000 ALTER TABLE `goods` DISABLE KEYS */;
/*!40000 ALTER TABLE `goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `po`
--

DROP TABLE IF EXISTS `po`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `po` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sname` varchar(20) NOT NULL,
  `gname` varchar(20) NOT NULL,
  `p_price` decimal(10,2) NOT NULL,
  `p_qty_num` int NOT NULL,
  `p_qty_weight` decimal(10,4) NOT NULL,
  `p_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sname` (`sname`),
  KEY `gname` (`gname`),
  CONSTRAINT `po_ibfk_1` FOREIGN KEY (`sname`) REFERENCES `supplier` (`sname`),
  CONSTRAINT `po_ibfk_2` FOREIGN KEY (`gname`) REFERENCES `goods` (`gname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='采购订单';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `po`
--

LOCK TABLES `po` WRITE;
/*!40000 ALTER TABLE `po` DISABLE KEYS */;
/*!40000 ALTER TABLE `po` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier` (
  `sname` varchar(20) NOT NULL,
  PRIMARY KEY (`sname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='供货商';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier`
--

LOCK TABLES `supplier` WRITE;
/*!40000 ALTER TABLE `supplier` DISABLE KEYS */;
/*!40000 ALTER TABLE `supplier` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-05 19:12:31
