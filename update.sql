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
    `link` varchar(512) DEFAULT "" COMMENT "链接",
    `qy_link` varchar(512) DEFAULT "" COMMENT "企业网站链接",
    `name` varchar(255) DEFAULT "" COMMENT "店名",
    `country` varchar(255) DEFAULT "" COMMENT "地区",
    `page` int(10) DEFAULT 0 COMMENT "页码",
    `status` tinyint(3) DEFAULT 0 COMMENT "状态0：未使用，1：已使用",
    PRIMARY KEY (`ID`)
)COMMENT "列表页链接"

delete from list_link

DROP TABLE IF EXISTS shop_detail;
CREATE TABLE `shop_detail`(
    `ID` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(255) DEFAULT "" COMMENT "商家名称",
    `contact` varchar(30) DEFAULT "" COMMENT "联系人",
    `email` varchar(30) DEFAULT "" COMMENT "电子邮箱",
    `phone` varchar(20) DEFAULT "" COMMENT "联系电话",
    `phone2` varchar(20) DEFAULT "" COMMENT "联系电话2",
    `qq` varchar(30) DEFAULT "" COMMENT "QQ",
    `addr` varchar(255) DEFAULT "" COMMENT "联系地址",
    `service_area` varchar(255) DEFAULT 0 COMMENT "服务区域",
    `qy_link` varchar(512) DEFAULT "" COMMENT "企业网站链接",
    PRIMARY KEY (`ID`)
)COMMENT "商家详情"