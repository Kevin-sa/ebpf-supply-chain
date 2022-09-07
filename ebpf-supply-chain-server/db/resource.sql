CREATE TABLE `supply_chain_hook_info_socket`
(
    `id`          bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `type`        varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `package`     varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `version`     varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `describe`    varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `comm`        varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `d_addr`      varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `d_port`      int(10) NOT NULL DEFAULT '0' COMMENT '',
    `status`      tinyint(1) NOT NULL DEFAULT 0 COMMENT '处理状态 0:未处理 1：已处理',
    `create_time` bigint(20) NOT NULL DEFAULT 0 COMMENT '',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `supply_chain_hook_info_sys_open`
(
    `id`          bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `type`        varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `package`     varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `version`     varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `describe`    varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `comm`        varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `pid`         bigint(20) NOT NULL DEFAULT 0 COMMENT '',
    `filename`    varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `status`      tinyint(1) NOT NULL DEFAULT 0 COMMENT '处理状态 0:未处理 1：已处理',
    `create_time` bigint(20) NOT NULL DEFAULT 0 COMMENT '',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `supply_chain_hook_info_sys_write`
(
    `id`          bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `type`        varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `package`     varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `version`     varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `describe`    varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `comm`        varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `pid`         bigint(20) NOT NULL DEFAULT 0 COMMENT '',
    `filename`    varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `status`      tinyint(1) NOT NULL DEFAULT 0 COMMENT '处理状态 0:未处理 1：已处理',
    `create_time` bigint(20) NOT NULL DEFAULT 0 COMMENT '',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `supply_chain_hook_info_sys_exec`
(
    `id`          bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `type`        varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `package`     varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `version`     varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `describe`    varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `comm`        varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `pid`         bigint(20) NOT NULL DEFAULT 0 COMMENT '',
    `filename`    varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `status`      tinyint(1) NOT NULL DEFAULT 0 COMMENT '处理状态 0:未处理 1：已处理',
    `create_time` bigint(20) NOT NULL DEFAULT 0 COMMENT '',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `supply_chain_evil_result`
(
    `id`          bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `hook_id`         bigint NOT NULL DEFAULT 0 COMMENT '',
    `hook_type`        varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `rule_name`        varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `package`     varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `version`     varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `describe`    varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `score`       tinyint(3) NOT NULL DEFAULT 0 COMMENT '',
    `hash`        varchar(255) NOT NULL DEFAULT '0' COMMENT '',
    `status`      tinyint(1) NOT NULL DEFAULT 0 COMMENT '告警状态 0：未处理，1：确认 2：误报',
    `create_time` bigint(20) NOT NULL DEFAULT 0 COMMENT '',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;