-- MySQL dump 10.19  Distrib 10.3.31-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: ge
-- ------------------------------------------------------
-- Server version	10.3.31-MariaDB-0+deb10u1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ge_updates`
--

DROP TABLE IF EXISTS `ge_updates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ge_updates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=394 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `limits`
--

DROP TABLE IF EXISTS `limits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `limits` (
  `id` int(11) NOT NULL,
  `limit` int(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `osb_hist`
--

DROP TABLE IF EXISTS `osb_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `osb_hist` (
  `key` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `id` int(11) NOT NULL,
  `buy_average` int(11) NOT NULL,
  `buy_quantity` int(11) NOT NULL,
  `sell_average` int(11) NOT NULL,
  `sell_quantity` int(11) NOT NULL,
  `overall_average` int(11) NOT NULL,
  `overall_quantity` int(11) NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=660624 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `osb_updates`
--

DROP TABLE IF EXISTS `osb_updates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `osb_updates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12420 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `osrs_hist`
--

DROP TABLE IF EXISTS `osrs_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `osrs_hist` (
  `key` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `id` int(11) NOT NULL,
  `current_trend` varchar(10) NOT NULL,
  `current_price` int(11) NOT NULL,
  `enriched_price` int(11) DEFAULT NULL,
  `enriched_quantity` int(9) DEFAULT NULL,
  `enriched` tinyint(1) DEFAULT 0,
  `today_trend` varchar(10) NOT NULL,
  `today_price` int(11) NOT NULL,
  `30day_trend` varchar(10) NOT NULL,
  `30day_change` decimal(6,2) NOT NULL,
  `90day_trend` varchar(10) NOT NULL,
  `90day_change` decimal(6,2) NOT NULL,
  `180day_trend` varchar(10) NOT NULL,
  `180day_change` decimal(10,2) NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=57063 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `potential`
--

DROP TABLE IF EXISTS `potential`;
/*!50001 DROP VIEW IF EXISTS `potential`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `potential` (
  `name` tinyint NOT NULL,
  `key` tinyint NOT NULL,
  `date` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `buy_average` tinyint NOT NULL,
  `buy_quantity` tinyint NOT NULL,
  `sell_average` tinyint NOT NULL,
  `sell_quantity` tinyint NOT NULL,
  `overall_average` tinyint NOT NULL,
  `overall_quantity` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `potential_6hours`
--

DROP TABLE IF EXISTS `potential_6hours`;
/*!50001 DROP VIEW IF EXISTS `potential_6hours`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `potential_6hours` (
  `name` tinyint NOT NULL,
  `key` tinyint NOT NULL,
  `date` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `buy_average` tinyint NOT NULL,
  `buy_quantity` tinyint NOT NULL,
  `sell_average` tinyint NOT NULL,
  `sell_quantity` tinyint NOT NULL,
  `overall_average` tinyint NOT NULL,
  `overall_quantity` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `potential_9hours`
--

DROP TABLE IF EXISTS `potential_9hours`;
/*!50001 DROP VIEW IF EXISTS `potential_9hours`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `potential_9hours` (
  `name` tinyint NOT NULL,
  `key` tinyint NOT NULL,
  `date` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `buy_average` tinyint NOT NULL,
  `buy_quantity` tinyint NOT NULL,
  `sell_average` tinyint NOT NULL,
  `sell_quantity` tinyint NOT NULL,
  `overall_average` tinyint NOT NULL,
  `overall_quantity` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `potential_wiki`
--

DROP TABLE IF EXISTS `potential_wiki`;
/*!50001 DROP VIEW IF EXISTS `potential_wiki`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `potential_wiki` (
  `name` tinyint NOT NULL,
  `date` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `insta_buy_avg` tinyint NOT NULL,
  `insta_buy_quantity` tinyint NOT NULL,
  `insta_sell_avg` tinyint NOT NULL,
  `insta_sell_quantity` tinyint NOT NULL,
  `rs_date` tinyint NOT NULL,
  `enriched_price` tinyint NOT NULL,
  `enriched_quantity` tinyint NOT NULL,
  `osb_date` tinyint NOT NULL,
  `buy_average` tinyint NOT NULL,
  `buy_quantity` tinyint NOT NULL,
  `sell_average` tinyint NOT NULL,
  `sell_quantity` tinyint NOT NULL,
  `overall_average` tinyint NOT NULL,
  `overall_quantity` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wiki_hist`
--

DROP TABLE IF EXISTS `wiki_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wiki_hist` (
  `key` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `id` int(11) NOT NULL,
  `avgHighPrice` int(11) DEFAULT NULL,
  `highPriceVolume` int(11) DEFAULT NULL,
  `avgLowPrice` int(11) DEFAULT NULL,
  `lowPriceVolume` int(11) DEFAULT NULL,
  `json_timestamp` int(11) DEFAULT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=6715186 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `potential`
--

/*!50001 DROP TABLE IF EXISTS `potential`*/;
/*!50001 DROP VIEW IF EXISTS `potential`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `potential` AS (select `i`.`name` AS `name`,`oh`.`key` AS `key`,`oh`.`date` AS `date`,`oh`.`id` AS `id`,`oh`.`buy_average` AS `buy_average`,`oh`.`buy_quantity` AS `buy_quantity`,`oh`.`sell_average` AS `sell_average`,`oh`.`sell_quantity` AS `sell_quantity`,`oh`.`overall_average` AS `overall_average`,`oh`.`overall_quantity` AS `overall_quantity` from (`osb_hist` `oh` join `items` `i` on(`i`.`id` = `oh`.`id`)) where `oh`.`date` between sysdate() - interval '6' hour and sysdate() and `oh`.`overall_quantity` > 1 and `oh`.`overall_average` > 4000000 and `oh`.`overall_average` < 200000000 order by `i`.`name`,`oh`.`date` desc) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `potential_6hours`
--

/*!50001 DROP TABLE IF EXISTS `potential_6hours`*/;
/*!50001 DROP VIEW IF EXISTS `potential_6hours`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `potential_6hours` AS (select `i`.`name` AS `name`,`oh`.`key` AS `key`,`oh`.`date` AS `date`,`oh`.`id` AS `id`,`oh`.`buy_average` AS `buy_average`,`oh`.`buy_quantity` AS `buy_quantity`,`oh`.`sell_average` AS `sell_average`,`oh`.`sell_quantity` AS `sell_quantity`,`oh`.`overall_average` AS `overall_average`,`oh`.`overall_quantity` AS `overall_quantity` from (`osb_hist` `oh` join `items` `i` on(`i`.`id` = `oh`.`id`)) where `oh`.`date` between sysdate() - interval '6' hour and sysdate() and `oh`.`overall_quantity` > 2 order by `i`.`name`,`oh`.`date` desc) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `potential_9hours`
--

/*!50001 DROP TABLE IF EXISTS `potential_9hours`*/;
/*!50001 DROP VIEW IF EXISTS `potential_9hours`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `potential_9hours` AS (select `i`.`name` AS `name`,`oh`.`key` AS `key`,`oh`.`date` AS `date`,`oh`.`id` AS `id`,`oh`.`buy_average` AS `buy_average`,`oh`.`buy_quantity` AS `buy_quantity`,`oh`.`sell_average` AS `sell_average`,`oh`.`sell_quantity` AS `sell_quantity`,`oh`.`overall_average` AS `overall_average`,`oh`.`overall_quantity` AS `overall_quantity` from (`osb_hist` `oh` join `items` `i` on(`i`.`id` = `oh`.`id`)) where `oh`.`date` between sysdate() - interval '9' hour and sysdate() and `oh`.`overall_quantity` > 2 order by `i`.`name`,`oh`.`date` desc) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `potential_wiki`
--

/*!50001 DROP TABLE IF EXISTS `potential_wiki`*/;
/*!50001 DROP VIEW IF EXISTS `potential_wiki`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `potential_wiki` AS (select `v`.`name` AS `name`,`v`.`date` AS `date`,`v`.`id` AS `id`,`v`.`insta_buy_avg` AS `insta_buy_avg`,`v`.`insta_buy_quantity` AS `insta_buy_quantity`,`v`.`insta_sell_avg` AS `insta_sell_avg`,`v`.`insta_sell_quantity` AS `insta_sell_quantity`,`v`.`rs_date` AS `rs_date`,`v`.`enriched_price` AS `enriched_price`,`v`.`enriched_quantity` AS `enriched_quantity`,`v`.`osb_date` AS `osb_date`,`v`.`buy_average` AS `buy_average`,`v`.`buy_quantity` AS `buy_quantity`,`v`.`sell_average` AS `sell_average`,`v`.`sell_quantity` AS `sell_quantity`,`v`.`overall_average` AS `overall_average`,`v`.`overall_quantity` AS `overall_quantity` from (with wiki as (select `i`.`name` AS `name`,`wh`.`date` AS `date`,`wh`.`id` AS `id`,`wh`.`avgHighPrice` AS `insta_buy_avg`,`wh`.`highPriceVolume` AS `insta_buy_quantity`,`wh`.`avgLowPrice` AS `insta_sell_avg`,`wh`.`lowPriceVolume` AS `insta_sell_quantity` from (`ge`.`wiki_hist` `wh` left join `ge`.`items` `i` on(`i`.`id` = `wh`.`id`)) where `wh`.`date` between sysdate() - interval '3' hour and sysdate() and (`wh`.`avgHighPrice` > 4000000 and `wh`.`avgHighPrice` < 200000000 or `wh`.`avgLowPrice` > 4000000 and `wh`.`avgLowPrice` < 200000000) and `wh`.`highPriceVolume` + `wh`.`lowPriceVolume` > 1), osb as (select `oh`.`key` AS `key`,`oh`.`date` AS `date`,`oh`.`id` AS `id`,`oh`.`buy_average` AS `buy_average`,`oh`.`buy_quantity` AS `buy_quantity`,`oh`.`sell_average` AS `sell_average`,`oh`.`sell_quantity` AS `sell_quantity`,`oh`.`overall_average` AS `overall_average`,`oh`.`overall_quantity` AS `overall_quantity`,row_number() over ( partition by `oh`.`id` order by `oh`.`date` desc) AS `rn` from `ge`.`osb_hist` `oh` where `oh`.`overall_quantity` > 1 and `oh`.`date` between sysdate() - interval '3' hour and sysdate()), osrs as (select `rs`.`key` AS `key`,`rs`.`date` AS `date`,`rs`.`id` AS `id`,`rs`.`current_trend` AS `current_trend`,`rs`.`current_price` AS `current_price`,`rs`.`enriched_price` AS `enriched_price`,`rs`.`enriched_quantity` AS `enriched_quantity`,`rs`.`enriched` AS `enriched`,`rs`.`today_trend` AS `today_trend`,`rs`.`today_price` AS `today_price`,`rs`.`30day_trend` AS `30day_trend`,`rs`.`30day_change` AS `30day_change`,`rs`.`90day_trend` AS `90day_trend`,`rs`.`90day_change` AS `90day_change`,`rs`.`180day_trend` AS `180day_trend`,`rs`.`180day_change` AS `180day_change`,row_number() over ( partition by `rs`.`id` order by `rs`.`date` desc) AS `rn` from `ge`.`osrs_hist` `rs` where `rs`.`enriched` = 1)select `w`.`name` AS `name`,`w`.`date` AS `date`,`w`.`id` AS `id`,`w`.`insta_buy_avg` AS `insta_buy_avg`,`w`.`insta_buy_quantity` AS `insta_buy_quantity`,`w`.`insta_sell_avg` AS `insta_sell_avg`,`w`.`insta_sell_quantity` AS `insta_sell_quantity`,`rs`.`date` AS `rs_date`,`rs`.`enriched_price` AS `enriched_price`,`rs`.`enriched_quantity` AS `enriched_quantity`,`o`.`date` AS `osb_date`,`o`.`buy_average` AS `buy_average`,`o`.`buy_quantity` AS `buy_quantity`,`o`.`sell_average` AS `sell_average`,`o`.`sell_quantity` AS `sell_quantity`,`o`.`overall_average` AS `overall_average`,`o`.`overall_quantity` AS `overall_quantity` from ((`wiki` `w` left join `osb` `o` on(`o`.`id` = `w`.`id`)) left join `osrs` `rs` on(`rs`.`id` = `w`.`id`)) where `rs`.`rn` = 1 and `o`.`rn` = 1 order by `w`.`name`,`w`.`date` desc) `v`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-01 10:41:45
