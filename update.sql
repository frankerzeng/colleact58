use py58;
DROP TABLE IF EXISTS shop;
CREATE TABLE `shop`(
    `ID` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(255) DEFAULT "" COMMENT "店名",
    PRIMARY KEY (`ID`)
)COMMENT "结果表"

use py58;
DROP TABLE IF EXISTS faxingshi_link;
CREATE TABLE `faxingshi_link`(
    `ID` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
    `link` varchar(255) DEFAULT "" COMMENT "店名",
    `status` tinyint(3) DEFAULT 0 COMMENT "状态0：未使用，1：已使用",
    PRIMARY KEY (`ID`)
)COMMENT "链接表"


use py58;
DROP TABLE IF EXISTS list_link;
CREATE TABLE `list_link`(
    `ID` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
    `link` varchar(255) DEFAULT "" COMMENT "店名",
    `country` varchar(255) DEFAULT "" COMMENT "地区",
    `page` int(10) DEFAULT 0 COMMENT "页码",
    `status` tinyint(3) DEFAULT 0 COMMENT "状态0：未使用，1：已使用",
    PRIMARY KEY (`ID`)
)COMMENT "列表页链接"

delete from list_link