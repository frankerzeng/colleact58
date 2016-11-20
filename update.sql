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
)COMMENT "列表页链接";

DROP TABLE IF EXISTS shop_detail;
CREATE TABLE `shop_detail`(
    `ID` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
    `city` varchar(255) DEFAULT "" COMMENT "城市",
    `city_jp` varchar(255) DEFAULT "" COMMENT "城市简拼",
    `area` varchar(255) DEFAULT "" COMMENT "区域",
    `category` varchar(255) DEFAULT "" COMMENT "职位",
    `category_qp` varchar(255) DEFAULT "" COMMENT "职位全拼",
    `name` varchar(255) DEFAULT "" COMMENT "商家名称",
    `contact` varchar(100) DEFAULT "" COMMENT "联系人",
    `email` varchar(100) DEFAULT "" COMMENT "电子邮箱",
    `phone1` varchar(200) DEFAULT "" COMMENT "联系电话1",
    `phone2` varchar(20) DEFAULT "" COMMENT "联系电话2",
    `phone1_result` varchar(20) DEFAULT "" COMMENT "联系电话1识别后",
    `qq` varchar(30) DEFAULT "" COMMENT "QQ",
    `addr` varchar(255) DEFAULT "" COMMENT "联系地址",
    `service_area` varchar(255) DEFAULT 0 COMMENT "服务区域",
    `qy_link` varchar(512) DEFAULT "" COMMENT "企业网站链接",
    PRIMARY KEY (`ID`)
)COMMENT "商家详情";

DROP TABLE IF EXISTS city;
CREATE TABLE `city`(
    `ID` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
    `city` varchar(255) DEFAULT "" COMMENT "城市",
    `city_jp` varchar(255) DEFAULT "" COMMENT "城市简拼",
    `category` varchar(255) DEFAULT "" COMMENT "职位拼音",
    `category_name` varchar(255) DEFAULT "" COMMENT "职位名",
    `status` tinyint(3) DEFAULT 0 COMMENT "状态0：未采集，1：已采集",
    PRIMARY KEY (`ID`)
)COMMENT "全部城市";

DROP TABLE IF EXISTS category;
CREATE TABLE `category`(
    `ID` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
    `category` varchar(255) DEFAULT "" COMMENT "职位",
    `category_name` varchar(255) DEFAULT "" COMMENT "职位中文名",
    PRIMARY KEY (`ID`)
)COMMENT "全部职位";

DROP TABLE IF EXISTS `count_data`;
CREATE TABLE `count_data`(
    `ID` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
    `num` bigint(11) unsigned NOT NULL DEFAULT 0 COMMENT "总数",
    `num_add` bigint(11) unsigned NOT NULL DEFAULT 0 COMMENT "增加数",
    `create_time` bigint(11) unsigned NOT NULL DEFAULT 0 COMMENT "更新时间",
    PRIMARY KEY (`ID`)
)COMMENT "统计";