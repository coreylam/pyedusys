-- MySQL dump 10.16  Distrib 10.1.28-MariaDB, for Win32 (AMD64)
--
-- Host: localhost    Database: db_education
-- ------------------------------------------------------
-- Server version	10.1.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course` (
  `coursenum` varchar(10) CHARACTER SET utf8 NOT NULL,
  `name` varchar(32) CHARACTER SET utf8 NOT NULL,
  `lessonnum` int(10) NOT NULL,
  `starttime` date DEFAULT NULL,
  `endtime` date DEFAULT NULL,
  PRIMARY KEY (`coursenum`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES ('C0001','语文',36,'2017-01-01','2017-03-01'),('C0002','数学',72,'2017-01-02','2017-09-02'),('C0003','美术',36,'2018-03-24','2018-06-24');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `learn`
--

DROP TABLE IF EXISTS `learn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `learn` (
  `studentnum` varchar(10) CHARACTER SET utf8 NOT NULL,
  `coursenum` varchar(10) CHARACTER SET utf8 NOT NULL,
  `learnid` varchar(10) CHARACTER SET utf8 NOT NULL,
  `bookln` int(32) NOT NULL,
  `finishln` int(32) NOT NULL,
  `lackln` int(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `learn`
--

LOCK TABLES `learn` WRITE;
/*!40000 ALTER TABLE `learn` DISABLE KEYS */;
INSERT INTO `learn` VALUES ('S0002','C0002','L00020002',10,0,0),('S0002','C0001','L00020001',10,0,1),('S0110','C0002','L01100002',30,0,0),('S1110','C0002','L11100002',11,0,0),('S1110','C0001','L11100001',11,0,0),('S0009','C0001','L00090001',36,11,11),('S0009','C0002','L00090002',36,1,1),('S0008','C0001','L00080001',36,0,0),('S0002','C0003','L00020003',12,0,0);
/*!40000 ALTER TABLE `learn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `management`
--

DROP TABLE IF EXISTS `management`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `management` (
  `account` varchar(32) CHARACTER SET utf8 NOT NULL,
  `password` varchar(32) CHARACTER SET utf8 NOT NULL,
  `accountlevel` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `management`
--

LOCK TABLES `management` WRITE;
/*!40000 ALTER TABLE `management` DISABLE KEYS */;
INSERT INTO `management` VALUES ('admin','root',0),('root','admin',0);
/*!40000 ALTER TABLE `management` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signup`
--

DROP TABLE IF EXISTS `signup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `signup` (
  `ID` varchar(10) CHARACTER SET utf8 NOT NULL,
  `StudentNO` varchar(10) CHARACTER SET utf8 NOT NULL,
  `CourseNO` varchar(10) CHARACTER SET utf8 NOT NULL,
  `DisCount` int(8) NOT NULL,
  `RealCharge` int(8) NOT NULL,
  KEY `ID` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signup`
--

LOCK TABLES `signup` WRITE;
/*!40000 ALTER TABLE `signup` DISABLE KEYS */;
/*!40000 ALTER TABLE `signup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `studentnum` varchar(10) CHARACTER SET utf8 NOT NULL,
  `name` varchar(10) CHARACTER SET utf8 NOT NULL,
  `gender` char(8) CHARACTER SET utf8 NOT NULL,
  `phone` varchar(18) CHARACTER SET utf8 NOT NULL,
  `pname` varchar(10) CHARACTER SET utf8 NOT NULL,
  `lessonnum` int(32) NOT NULL,
  `accountnum` int(32) NOT NULL,
  `age` int(32) NOT NULL,
  PRIMARY KEY (`studentnum`) USING BTREE,
  KEY `studentnum` (`studentnum`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('S0002','小红','女','123123123','阿斯蒂芬',68,0,9),('S0003','小王','男','111000222','老王',0,1,11),('S0008','史蒂夫','女','123123123','斯蒂芬',34,3000,8),('S0009','张三','男','111231231','张三丰',1114,1000,9);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher` (
  `teachernum` varchar(10) CHARACTER SET utf8 NOT NULL,
  `name` varchar(10) CHARACTER SET utf8 NOT NULL,
  `gender` char(8) CHARACTER SET utf8 NOT NULL,
  `phone` varchar(18) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`teachernum`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES ('T0001','小刘','女','113311231'),('T0002','旺旺','男','111111222');
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-24 21:24:47
