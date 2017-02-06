DROP TABLE IF EXISTS energy_logs;
DROP TABLE IF EXISTS activity_logs;

DROP TABLE IF EXISTS rules_access;
DROP TABLE IF EXISTS devices_access;

DROP TABLE IF EXISTS rule_sections;
DROP TABLE IF EXISTS rules;

DROP TABLE IF EXISTS devices;

DROP TABLE IF EXISTS users;


DROP TABLE IF EXISTS access_levels;
CREATE TABLE access_levels
(
id					int NOT NULL AUTO_INCREMENT,
level_name			varchar(255),
PRIMARY KEY (id)
);

DROP TABLE IF EXISTS user_groups;
CREATE TABLE user_groups
(
id					int NOT NULL AUTO_INCREMENT,
group_name			varchar(255),
PRIMARY KEY (id)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
id					int NOT NULL AUTO_INCREMENT,
group_id			int NOT NULL,
email				varchar(255),
nickname			varchar(255) NOT NULL,
creation_date		date NOT NULL,
last_activity_date	date NOT NULL,
PRIMARY KEY (id)
,FOREIGN KEY (group_id) REFERENCES user_groups(id)
);

DROP TABLE IF EXISTS device_types;
CREATE TABLE device_types
(
id					int NOT NULL AUTO_INCREMENT,
type_name			varchar(255),
PRIMARY KEY (id)
);

DROP TABLE IF EXISTS devices;
CREATE TABLE devices
(
id					int NOT NULL AUTO_INCREMENT,
type_id				int NOT NULL,
device_name			varchar(255),
owner_id			int NOT NULL,
creation_date		date NOT NULL,
last_activity_date	date NOT NULL,
PRIMARY KEY (id)
,FOREIGN KEY (type_id) REFERENCES device_types(id)
,FOREIGN KEY (owner_id) REFERENCES users(id)
);

DROP TABLE IF EXISTS devices_access;
CREATE TABLE devices_access
(
id					int NOT NULL AUTO_INCREMENT,
user_id				int NOT NULL,
device_id			int NOT NULL,
access_level		int NOT NULL,
creation_date		date NOT NULL,
PRIMARY KEY (id)
,FOREIGN KEY (user_id) REFERENCES users(id)
,FOREIGN KEY (device_id) REFERENCES devices(id)
,FOREIGN KEY (access_level) REFERENCES access_levels(id)
);


DROP TABLE IF EXISTS rule_parameters;
CREATE TABLE rule_parameters
(
id					int NOT NULL AUTO_INCREMENT,
parameter_name		varchar(255),
PRIMARY KEY (id)
);

DROP TABLE IF EXISTS rule_types;
CREATE TABLE rule_types
(
id					int NOT NULL AUTO_INCREMENT,
type_name			varchar(255),
PRIMARY KEY (id)
);

DROP TABLE IF EXISTS rules;
CREATE TABLE rules
(
id					int NOT NULL AUTO_INCREMENT,
type_id				int NOT NULL,
device_id			int NOT NULL,
owner_id			int NOT NULL,
creation_date		date NOT NULL,
modify_date			date NOT NULL,
sync_date			date NOT NULL,
PRIMARY KEY (id),
FOREIGN KEY (type_id) REFERENCES rule_types(id)
,FOREIGN KEY (device_id) REFERENCES devices(id)
,FOREIGN KEY (owner_id) REFERENCES users(id)
);

DROP TABLE IF EXISTS rule_sections;
CREATE TABLE rule_sections
(
id					int NOT NULL AUTO_INCREMENT,
rule_id				int NOT NULL,
parameter_id		int NOT NULL,
body				varchar(255),
PRIMARY KEY (id)
,FOREIGN KEY (rule_id) REFERENCES rules(id)
,FOREIGN KEY (parameter_id) REFERENCES rule_parameters(id)
);

DROP TABLE IF EXISTS rules_access;
CREATE TABLE rules_access
(
id					int NOT NULL AUTO_INCREMENT,
user_id				int NOT NULL,
rule_id				int NOT NULL,
access_level		int NOT NULL,
creation_date		date NOT NULL,
PRIMARY KEY (id)
,FOREIGN KEY (user_id) REFERENCES users(id)
,FOREIGN KEY (rule_id) REFERENCES rules(id)
,FOREIGN KEY (access_level) REFERENCES access_levels(id)
);

DROP TABLE IF EXISTS activity_types;
CREATE TABLE activity_types
(
id					int NOT NULL AUTO_INCREMENT,
type_name			varchar(255),
PRIMARY KEY (id)
);

DROP TABLE IF EXISTS activity_logs;
CREATE TABLE activity_logs
(
id					int NOT NULL AUTO_INCREMENT,
type_id				int NOT NULL,
user_id				int NOT NULL,
device_id			int NOT NULL,
metadata			varchar(255),
creation_date		date NOT NULL,
PRIMARY KEY (id)
,FOREIGN KEY (type_id) REFERENCES activity_types(id)
,FOREIGN KEY (user_id) REFERENCES users(id)
,FOREIGN KEY (device_id) REFERENCES devices(id)
);

DROP TABLE IF EXISTS energy_types;
CREATE TABLE energy_types
(
id					int NOT NULL AUTO_INCREMENT,
type_name			varchar(255),
PRIMARY KEY (id)
);

DROP TABLE IF EXISTS energy_logs;
CREATE TABLE energy_logs
(
id					int NOT NULL AUTO_INCREMENT,
type_id				int NOT NULL,
device_id			int NOT NULL,
energy_value		float NOT NULL,
metadata			varchar(255),	
creation_date		date NOT NULL,
PRIMARY KEY (id)
,FOREIGN KEY (device_id) REFERENCES devices(id)
,FOREIGN KEY (type_id) REFERENCES energy_types(id)
);