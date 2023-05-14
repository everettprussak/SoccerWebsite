-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (x86_64)
--
-- Host: localhost    Database: application
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `coach`
--

DROP TABLE IF EXISTS `coach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coach` (
  `coachID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `wins` int DEFAULT NULL,
  `active` int DEFAULT NULL,
  PRIMARY KEY (`coachID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coach`
--

LOCK TABLES `coach` WRITE;
/*!40000 ALTER TABLE `coach` DISABLE KEYS */;
INSERT INTO `coach` VALUES (1,'Lionel Scaloni',6,1),(2,'Graham Arnold',7,1),(3,'Roberto Martínez',2,1),(4,'Tite',3,1),(5,'Rigobert Song',0,1),(6,'John Herdman',4,1),(7,'Luis Fernando Suárez',0,1),(8,'Zlatko Dalic',0,1),(9,'Kasper Hjulmand',0,1),(10,'Gustavo Alfaro',2,1);
/*!40000 ALTER TABLE `coach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game` (
  `gameID` int NOT NULL AUTO_INCREMENT,
  `homeID` int NOT NULL,
  `awayID` int NOT NULL,
  `homeScore` int DEFAULT NULL,
  `awayScore` int DEFAULT NULL,
  PRIMARY KEY (`gameID`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `game` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
INSERT INTO `game` VALUES (1,1,2,5,1),(2,1,3,3,0),(3,1,4,2,4),(4,1,5,2,1),(5,1,6,2,3),(6,1,7,2,0),(7,1,8,5,0),(8,1,9,4,2),(9,1,10,4,5),(10,2,1,4,3),(11,2,3,2,0),(12,2,4,1,2),(13,2,5,2,0),(14,2,6,1,2),(15,2,7,5,3),(16,2,8,2,0),(17,2,9,3,0),(18,2,10,2,0),(19,3,9,4,2),(20,3,7,2,1),(21,3,4,1,4),(22,6,4,3,1),(23,6,10,7,0),(24,10,8,4,0);
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goal`
--

DROP TABLE IF EXISTS `goal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goal` (
  `goalID` int NOT NULL AUTO_INCREMENT,
  `playerID` int NOT NULL,
  `gameID` int NOT NULL,
  PRIMARY KEY (`goalID`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goal`
--

LOCK TABLES `goal` WRITE;
/*!40000 ALTER TABLE `goal` DISABLE KEYS */;
INSERT INTO `goal` VALUES (1,1,1),(2,2,1),(3,28,1),(4,1,1),(5,1,2),(6,11,2),(7,1,2),(8,81,3),(9,1,3),(10,2,3),(11,81,3),(12,83,3),(13,81,3),(14,1,4),(15,9,4),(16,106,4),(17,10,5),(18,138,5),(19,154,5),(20,132,5),(21,1,5),(22,3,6),(23,6,6),(24,1,7),(25,1,7),(26,1,7),(27,1,7),(28,5,7),(29,8,8),(30,2,8),(31,3,8),(32,1,8),(33,209,8),(34,213,8),(35,20,9),(36,16,9),(37,1,9),(38,240,9),(39,240,9),(40,240,9),(41,240,9),(42,240,9),(43,1,9),(44,28,10),(45,28,10),(46,4,10),(47,1,10),(48,27,10),(49,36,10),(50,1,10),(51,28,11),(52,41,11),(53,85,12),(54,89,12),(55,27,12),(56,27,13),(57,28,13),(58,30,14),(59,142,14),(60,145,14),(61,29,15),(62,30,15),(63,28,15),(64,180,15),(65,175,15),(66,180,15),(67,28,15),(68,28,15),(69,29,16),(70,28,16),(71,30,17),(72,36,17),(73,35,17),(74,28,18),(75,31,18),(76,55,19),(77,53,19),(78,55,19),(79,209,19),(80,214,19),(81,53,19),(82,55,20),(83,59,20),(84,180,20),(85,61,21),(86,81,21),(87,81,21),(88,81,21),(89,81,21),(90,131,22),(91,146,22),(92,81,22),(93,131,22),(94,132,23),(95,132,23),(96,132,23),(97,131,23),(98,132,23),(99,142,23),(100,133,23),(101,240,24),(102,236,24),(103,252,24),(104,235,24),(105,16,1),(106,1,1);
/*!40000 ALTER TABLE `goal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `player`
--

DROP TABLE IF EXISTS `player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player` (
  `playerID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `age` int NOT NULL,
  `position` varchar(25) NOT NULL,
  `goals` int DEFAULT NULL,
  `teamID` int DEFAULT NULL,
  PRIMARY KEY (`playerID`)
) ENGINE=InnoDB AUTO_INCREMENT=261 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player`
--

LOCK TABLES `player` WRITE;
/*!40000 ALTER TABLE `player` DISABLE KEYS */;
INSERT INTO `player` VALUES (1,'Lionel Messi',35,'RW',17,1),(2,'Lautaro Martínez',25,'ST',3,1),(3,'Paulo Dybala',29,'SUB',2,1),(4,'Marcos Acuña',31,'LB',1,1),(5,'Ángel Di María',35,'LW',1,1),(6,'Alejandro Gómez',35,'CM',1,1),(7,'Emiliano Martínez',30,'GK',NULL,1),(8,'Rodrigo Javier De Paul',28,'CM',1,1),(9,'Cristian Romero',24,'CB',1,1),(10,'Lisandro Martínez',25,'SUB',1,1),(11,'Gerónimo Rulli',30,'SUB',1,1),(12,'Guido Rodríguez',29,'SUB',NULL,1),(13,'Nicolás Otamendi',35,'CB',NULL,1),(14,'Nicolás Tagliafico',30,'SUB',NULL,1),(15,'Enzo Fernández',22,'SUB',NULL,1),(16,'Nicolás González',25,'SUB',2,1),(17,'Leandro Paredes',28,'CDM',NULL,1),(18,'Joaquín Correa',28,'SUB',NULL,1),(19,'Julián Álvarez',23,'SUB',NULL,1),(20,'Juan Foyth',25,'RES',1,1),(21,'Gonzalo Montiel',26,'SUB',NULL,1),(22,'Franco Armani',36,'SUB',NULL,1),(23,'Nahuel Molina',25,'RB',NULL,1),(24,'Exequiel Palacios',24,'RES',NULL,1),(25,'Alexis Mac Allister',24,'RES',NULL,1),(26,'Germán Pezzella',31,'SUB',NULL,1),(27,'Mathew Ryan',31,'GK',3,2),(28,'Jamie Maclaren',29,'ST',10,2),(29,'Aaron Mooy',32,'CDM',2,2),(30,'Craig Goodwin',31,'LM',3,2),(31,'Harry Souttar',24,'CB',1,2),(32,'Miloš Degenek',28,'CB',NULL,2),(33,'Jackson Irvine',30,'CDM',NULL,2),(34,'Martin Boyle',29,'RM',NULL,2),(35,'Riley McGree',24,'SUB',1,2),(36,'Cameron Devlin',24,'SUB',2,2),(37,'Mathew Leckie',32,'SUB',NULL,2),(38,'Kye Rowles',24,'SUB',NULL,2),(39,'Ajdin Hrustić',26,'CAM',NULL,2),(40,'Awer Mabil',27,'SUB',NULL,2),(41,'Fran Karačić',26,'SUB',1,2),(42,'Jason Cummings',27,'SUB',NULL,2),(43,'Aziz Behich',32,'LB',NULL,2),(44,'Nathaniel Atkinson',23,'RB',NULL,2),(45,'Mitchell Duke',32,'SUB',NULL,2),(46,'Danny Vukovic',38,'SUB',NULL,2),(47,'Bailey Wright',30,'RES',NULL,2),(48,'Keanu Baccus',24,'SUB',NULL,2),(49,'Joel King',22,'RES',NULL,2),(50,'Thomas Deng',26,'SUB',NULL,2),(51,'Andrew Redmayne',34,'SUB',NULL,2),(52,'Garang Kuol',18,'RES',NULL,2),(53,'Kevin De Bruyne',31,'RF',2,3),(54,'Thibaut Courtois',30,'GK',NULL,3),(55,'Romelu Lukaku',29,'ST',3,3),(56,'Yannick Carrasco',29,'LM',NULL,3),(57,'Youri Tielemans',25,'CM',NULL,3),(58,'Koen Casteels',30,'SUB',NULL,3),(59,'Eden Hazard',32,'LF',1,3),(60,'Dries Mertens',35,'SUB',NULL,3),(61,'Toby Alderweireld',34,'CB',1,3),(62,'Simon Mignolet',35,'SUB',NULL,3),(63,'Jan Vertonghen',35,'CB',NULL,3),(64,'Hans Vanaken',30,'SUB',NULL,3),(65,'Leandro Trossard',28,'SUB',NULL,3),(66,'Axel Witsel',34,'SUB',NULL,3),(67,'Thorgan Hazard',30,'SUB',NULL,3),(68,'Charles De KetelaereB',22,'SUB',NULL,3),(69,'Wout Faes',25,'SUB',NULL,3),(70,'Timothy Castagne',27,'RES',NULL,3),(71,'Thomas Meunier',31,'RM',NULL,3),(72,'Michy Batshuayi',29,'SUB',NULL,3),(73,'Arthur Theate',22,'RES',NULL,3),(74,'Leander Dendoncker',28,'SUB',NULL,3),(75,'Jérémy Doku',20,'RES',NULL,3),(76,'Amadou Onana',21,'CM',NULL,3),(77,'Loïs Openda',23,'SUB',NULL,3),(78,'Zeno Debast',19,'CB',NULL,3),(79,'Ederson Santana de Moraes',29,'SUB',NULL,4),(80,'Alisson Ramses Becker',30,'GK',NULL,4),(81,'Neymar da Silva Santos Jr',31,'ST',8,4),(82,'Carlos Henrique Venancio Casimiro',31,'CM',NULL,4),(83,'Marcos Aoás Corrêa',28,'CB',1,4),(84,'Vinícius José de Oliveira Júnior',22,'Lw',NULL,4),(85,'Thiago Emiliano da Silva',38,'CB',1,4),(86,'Fábio Henrique Tavares',29,'SUB',NULL,4),(87,'Éder Gabriel Militão',25,'SUB',NULL,4),(88,'Gabriel Fernando de Jesus',26,'SUB',NULL,4),(89,'Weverton Pereira da Silva',35,'RES',1,4),(90,'Bruno Guimarães Moura',25,'SUB',NULL,4),(91,'Gleison Bremer Silva Nascimento',26,'RES',NULL,4),(92,'Raphael Dias Belloli',26,'RW',NULL,4),(93,'Antony Matheus dos Santos',23,'SUB',NULL,4),(94,'Lucas Tolentino Lima',25,'CAM',NULL,4),(95,'Rodrygo Silva de Goes',22,'SUB',NULL,4),(96,'Richarlison de Andrade',25,'SUB',NULL,4),(97,'Danilo Luiz da Silva',31,'RB',NULL,4),(98,'Pedro Guilherme Abreu dos Santos',25,'SUB',NULL,4),(99,'Alex Sandro Lobo Silva',32,'LB',NULL,4),(100,'Frederico de Paula Santos',30,'CM',NULL,4),(101,'Alex Nicolao Telles',30,'SUB',NULL,4),(102,'Éverton Augusto de Barros Ribeiro',34,'SUB',NULL,4),(103,'Gabriel Teodoro Martinelli Silva',21,'RES',NULL,4),(104,'Daniel Alves da Silva',39,'SUB',NULL,4),(105,'André Onana',27,'GK',NULL,5),(106,'André-Franck Zambo Anguissa',27,'CDM',1,5),(107,'Karl Toko Ekambi',30,'LM',NULL,5),(108,'Eric Maxim Choupo-Moting',34,'ST',NULL,5),(109,'Nicolas Moumi Ngamaleu',28,'SUB',NULL,5),(110,'Bryan Mbeumo',23,'SUB',NULL,5),(111,'Jean-Pierre Nsame',29,'SUB',NULL,5),(112,'Vincent Aboubakar',31,'ST',NULL,5),(113,'Georges-Kévin Nkoudou Mbida',28,'SUB',NULL,5),(114,'Nicolas Nkoulou',33,'CB',NULL,5),(115,'Christian Bassogog',27,'RES',NULL,5),(116,'Jean-Charles Castelletto',28,'CB',NULL,5),(117,'Pierre Kunde',27,'SUB',NULL,5),(118,'Martin Hongla',25,'RM',NULL,5),(119,'Olivier Ntcham',27,'SUB',NULL,5),(120,'Christopher Wooh',21,'SUB',NULL,5),(121,'Enzo Ebosse',24,'LB',NULL,5),(122,'Nouhou Tolo',25,'SUB',NULL,5),(123,'Collins Fai',30,'RB',NULL,5),(124,'Samuel Oum Gouet',25,'CDM',NULL,5),(125,'Gaël Ondoua',27,'SUB',NULL,5),(126,'Devis Epassy',30,'SUB',NULL,5),(127,'Simon Ngapandouetnbu',20,'SUB',NULL,5),(128,'Olivier Mbaizo',25,'SUB',NULL,5),(129,'Jerome Ngom Mbekeli',24,'RES',NULL,5),(130,'Souaibou Marou',22,'RES',NULL,5),(131,'Alphonso Davies',22,'LM',3,6),(132,'Jonathan David',23,'ST',5,6),(133,'Stephen Antunes Eustáquio',26,'CDM',1,6),(134,'Milan Borjan',35,'GK',NULL,6),(135,'Jonathan Osorio',30,'CAM',NULL,6),(136,'Cyle Larin',28,'SUB',NULL,6),(137,'Iké Ugbo',24,'SUB',NULL,6),(138,'Tajon Buchanan',24,'RM',1,6),(139,'Atiba Hutchinson',40,'CDM',NULL,6),(140,'Richie Laryea',28,'SUB',NULL,6),(141,'Dayne St Clair',25,'SUB',NULL,6),(142,'Kamal Miller',25,'CB',2,6),(143,'Alistair Johnston',24,'RB',NULL,6),(144,'Lucas Cavallini',30,'SUB',NULL,6),(145,'Junior Hoilett',32,'SUB',1,6),(146,'Samuel Piette',28,'SUB',1,6),(147,'Sam Adekugbe',28,'LB',NULL,6),(148,'Steven de Sousa Vitória',36,'CB',NULL,6),(149,'Mark-Anthony Kaye',28,'SUB',NULL,6),(150,'Liam Millar',23,'SUB',NULL,6),(151,'Joel Waterman',27,'RES',NULL,6),(152,'David Wotherspoon',33,'SUB',NULL,6),(153,'Ismaël Koné',20,'RES',NULL,6),(154,'James Pantemis',26,'SUB',1,6),(155,'Derek Cornelius',25,'SUB',NULL,6),(156,'Liam Fraser',25,'RES',NULL,6),(157,'Keylor Navas',36,'GK',NULL,7),(158,'Bryan Ruiz',37,'SUB',NULL,7),(159,'Óscar Esau Duarte Gaitán',33,'CB',NULL,7),(160,'Joel Campbell',30,'ST',NULL,7),(161,'Celso Borges',34,'CM',NULL,7),(162,'Keysher Fuller',28,'RB',NULL,7),(163,'Yeltsin Tejeda',31,'CM',NULL,7),(164,'Kendall Waston',35,'SUB',NULL,7),(165,'Juan Pablo Vargas',27,'SUB',NULL,7),(166,'Ronald Matarrita',28,'SUB',NULL,7),(167,'Gerson Torres',25,'RM',NULL,7),(168,'Francisco Calvo',30,'B',NULL,7),(169,'Esteban Alvarado',33,'SUB',NULL,7),(170,'Bryan Oviedo',33,'LB',NULL,7),(171,'Anthony Contreras',23,'ST',NULL,7),(172,'Johan Venegas',34,'SUB',NULL,7),(173,'Jewison Bennette',18,'LM',NULL,7),(174,'Daniel Chacón',22,'SUB',NULL,7),(175,'Brandon Aguilera',19,'RES',1,7),(176,'Douglas López',24,'SUB',NULL,7),(177,'Youstin Salas',26,'SUB',NULL,7),(178,'Carlos Manuel Martínez Castro',24,'RES',NULL,7),(179,'Patrick Gilmar Sequeira',24,'SUB',NULL,7),(180,'Álvaro Zamora',21,'SUB',3,7),(181,'Anthony Hernández',29,'SUB',NULL,7),(182,'Roan Wilson',20,'RES',NULL,7),(183,'Luka Modrić',37,'CM',NULL,8),(184,'Marcelo Brozović',30,'DM',NULL,8),(185,'Mateo Kovačić',28,'CM',NULL,8),(186,'Ivan Perišić',34,'LM',NULL,8),(187,'Andrej Kramarić',31,'ST',NULL,8),(188,'Joško Gvardiol',21,'CB',NULL,8),(189,'Mario Pašalić',28,'RM',NULL,8),(190,'Lovro Majer',25,'SUB',NULL,8),(191,'Dominik Livaković',28,'GK',NULL,8),(192,'Borna Sosa',25,'LB',NULL,8),(193,'Nikola Vlašić',25,'SUB',NULL,8),(194,'Dejan Lovren',33,'CB',NULL,8),(195,'Mislav Oršić',30,'SUB',NULL,8),(196,'Marko Livaja',29,'SUB',NULL,8),(197,'Josip Šutalo',23,'SUB',NULL,8),(198,'Kristijan Jakić',25,'SUB',NULL,8),(199,'Domagoj Vida',33,'SUB',NULL,8),(200,'Ante Budimir',31,'RES',NULL,8),(201,'Josip Juranović',27,'RB',NULL,8),(202,'Bruno Petković',28,'RES',NULL,8),(203,'Luka Sučić',20,'RES',NULL,8),(204,'Martin Erlić',25,'SUB',NULL,8),(205,'Ivo Grbić',27,'SUB',NULL,8),(206,'Ivica Ivušić',28,'SUB',NULL,8),(207,'Borna Barišić',30,'SUB',NULL,8),(208,'Josip Stanišić',23,'SUB',NULL,8),(209,'Pierre-Emile Højbjerg',27,'CM',2,9),(210,'Christian Eriksen',31,'CAM',NULL,9),(211,'Kasper Schmeichel',36,'GK',NULL,9),(212,'Andreas Christensen',27,'CB',NULL,9),(213,'Simon Kjær',34,'CB',1,9),(214,'Thomas Delaney',31,'CM',1,9),(215,'Daniel Wass',33,'RB',NULL,9),(216,'Alexander Bah',25,'SUB',NULL,9),(217,'Joachim Andersen',26,'SUB',NULL,9),(218,'Rasmus Kristensen',25,'SUB',NULL,9),(219,'Kasper Dolberg',25,'ST',NULL,9),(220,'Yussuf Poulsen',28,'SUB',NULL,9),(221,'Martin Braithwaite',31,'SUB',NULL,9),(222,'Mikkel Damsgaard',22,'Lw',NULL,9),(223,'Jesper Lindstrøm',23,'SUB',NULL,9),(224,'Andreas Skov Olsen',23,'RW',NULL,9),(225,'Jonas WindD',24,'SUB',NULL,9),(226,'Frederik Riis Rønnow',30,'RES',NULL,9),(227,'Christian Nørgaard',29,'SUB',NULL,9),(228,'Victor Nelsson',24,'RES',NULL,9),(229,'Joakim Mæhle',25,'LB',NULL,9),(230,'Mathias Jensen',27,'SUB',NULL,9),(231,'Andreas Cornelius',30,'SUB',NULL,9),(232,'Jens Stryger Larsen',32,'SUB',NULL,9),(233,'Robert Skov',26,'RES',NULL,9),(234,'Oliver Christensen',24,'SUB',NULL,9),(235,'Pervis Estupiñán',25,'LB',1,10),(236,'Piero Hincapié',21,'CB',1,10),(237,'Gonzalo Plata',22,'RM',NULL,10),(238,'Ángel Israel Mena Delgado',35,'CAM',NULL,10),(239,'Felix Torres',26,'CB',NULL,10),(240,'Enner Valencia',33,'ST',6,10),(241,'Michael Estrada',27,'SUB',NULL,10),(242,'Alexander Dominguez',35,'GK',NULL,10),(243,'Robert Arboleda',31,'SUB',NULL,10),(244,'Moisés Caicedo',21,'CDM',NULL,10),(245,'José Cifuentes',24,'SUB',NULL,10),(246,'Carlos Gruezo',28,'CDM',NULL,10),(247,'Romario Ibarra',28,'LM',NULL,10),(248,'Ayrton Preciado',28,'SUB',NULL,10),(249,'Hernán Ismael Galíndez',36,'SUB',NULL,10),(250,'Moisés Ramírez',22,'SUB',NULL,10),(251,'Diego Palacios',23,'SUB',NULL,10),(252,'William Pacho',21,'SUB',1,10),(253,'Jackson Porozo',22,'RES',NULL,10),(254,'Sebastían Méndez',45,'SUB',NULL,10),(255,'Ángelo Preciado',25,'RB',NULL,10),(256,'Xavier Arreaga',28,'SUB',NULL,10),(257,'Jeremy Sarmiento',20,'SUB',NULL,10),(258,'Kevin Rodríguez',23,'RES',NULL,10),(259,'Djorkaeff Reasco',24,'RES',NULL,10),(260,'Alan Franco',26,'SUB',NULL,10);
/*!40000 ALTER TABLE `player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teams` (
  `teamID` int NOT NULL AUTO_INCREMENT,
  `teamName` varchar(50) NOT NULL,
  `teamCity` varchar(50) NOT NULL,
  `totalGoals` int DEFAULT NULL,
  `wins` int DEFAULT NULL,
  `losses` int DEFAULT NULL,
  `coachID` int DEFAULT NULL,
  PRIMARY KEY (`teamID`),
  UNIQUE KEY `teamName` (`teamName`),
  KEY `team_index` (`teamName`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
INSERT INTO `teams` VALUES (1,'Argentina','Buenos Aires',32,6,4,1),(2,'Australia','Melbourne',23,7,3,2),(3,'Belgium','Tubize',7,2,3,3),(4,'Brazil','Teresópolis',11,3,1,4),(5,'Cameroon','Mbankomo',1,0,2,5),(6,'Canada','Toronto',15,4,0,6),(7,'Costa Rica','San José',4,0,3,7),(8,'Croatia','Al Rayyan',0,0,3,8),(9,'Denmark','Indre Østerbro',4,0,3,9),(10,'Ecuador','Sangolqui',9,2,2,10);
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-14 11:06:22
