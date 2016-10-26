use py58;
DROP TABLE IF EXISTS shop;
CREATE TABLE `shop`(
    `ID` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(255) DEFAULT "" COMMENT "店名",
    PRIMARY KEY (`ID`)
)COMMENT "结果表"