CREATE TABLE IF NOT EXISTS members (
    id bigserial,
    username varchar not null,
    email varchar not null,
    created_at timestamp DEFAULT now(),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS organizations (
    id bigserial,
    "name" varchar not null,
    email varchar not null,
    "address" varchar not null,
    phone_number varchar,
    created_at timestamp DEFAULT now(),
    updated_at timestamp,
    PRIMARY KEY(id)
);

ALTER TABLE members ADD COLUMN organization_id bigint;
ALTER TABLE members ADD CONSTRAINT fk_organization_id FOREIGN KEY (organization_id) REFERENCES organizations(id);

INSERT INTO organizations (name, email, address) VALUES
('Company 1', 'info@company1.com', 'Company One St. 1'),
('Company 2', 'info@company2.com', 'Company One St. 2'),
('Company 3', 'info@company3.com', 'Company One St. 3'),
('Company 4', 'info@company4.com', 'Company One St. 4');

CREATE TABLE IF NOT EXISTS member_details (
    id bigserial,
    member_id bigint,
    first_name varchar,
    last_name varchar,
    gender char(1),
    country varchar,
    city varchar,
    city_address varchar,
    postal_code int,
    phone_number char,
    updated_at timestamp DEFAULT now(),
    PRIMARY KEY(id),
    FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS country_list (
    id bigserial,
    name varchar NOT NULL,
    code char(2) NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO public.country_list (id,"name",code) VALUES 
(1,'Afghanistan','AF'),
(2,'Ãland Islands','AX'),
(3,'Albania','AL'),
(4,'Algeria','DZ'),
(5,'American Samoa','AS'),
(6,'Andorra','AD'),
(7,'Angola','AO'),
(8,'Anguilla','AI'),
(9,'Antarctica','AQ'),
(10,'Antigua and Barbuda','AG');

INSERT INTO public.country_list (id,"name",code) VALUES 
(11,'Argentina','AR'),
(12,'Armenia','AM'),
(13,'Aruba','AW'),
(14,'Australia','AU'),
(15,'Austria','AT'),
(16,'Azerbaijan','AZ'),
(17,'Bahamas','BS'),
(18,'Bahrain','BH'),
(19,'Bangladesh','BD'),
(20,'Barbados','BB');

INSERT INTO public.country_list (id,"name",code) VALUES 
(21,'Belarus','BY'),
(22,'Belgium','BE'),
(23,'Belize','BZ'),
(24,'Benin','BJ'),
(25,'Bermuda','BM'),
(26,'Bhutan','BT'),
(27,'Bolivia, Plurinational State of','BO'),
(28,'Bonaire, Sint Eustatius and Saba','BQ'),
(29,'Bosnia and Herzegovina','BA'),
(30,'Botswana','BW');

INSERT INTO public.country_list (id,"name",code) VALUES 
(31,'Bouvet Island','BV'),
(32,'Brazil','BR'),
(33,'British Indian Ocean Territory','IO'),
(34,'Brunei Darussalam','BN'),
(35,'Bulgaria','BG'),
(36,'Burkina Faso','BF'),
(37,'Burundi','BI'),
(38,'Cambodia','KH'),
(39,'Cameroon','CM'),
(40,'Canada','CA');

INSERT INTO public.country_list (id,"name",code) VALUES 
(41,'Cape Verde','CV'),
(42,'Cayman Islands','KY'),
(43,'Central African Republic','CF'),
(44,'Chad','TD'),
(45,'Chile','CL'),
(46,'China','CN'),
(47,'Christmas Island','CX'),
(48,'Cocos (Keeling) Islands','CC'),
(49,'Colombia','CO'),
(50,'Comoros','KM');

INSERT INTO public.country_list (id,"name",code) VALUES 
(51,'Congo','CG'),
(52,'Congo, the Democratic Republic of the','CD'),
(53,'Cook Islands','CK'),
(54,'Costa Rica','CR'),
(55,'Côte d''Ivoire','CI'),
(56,'Croatia','HR'),
(57,'Cuba','CU'),
(58,'Curaçao','CW'),
(59,'Cyprus','CY'),
(60,'Czech Republic','CZ');

INSERT INTO public.country_list (id,"name",code) VALUES 
(61,'Denmark','DK'),
(62,'Djibouti','DJ'),
(63,'Dominica','DM'),
(64,'Dominican Republic','DO'),
(65,'Ecuador','EC'),
(66,'Egypt','EG'),
(67,'El Salvador','SV'),
(68,'Equatorial Guinea','GQ'),
(69,'Eritrea','ER'),
(70,'Estonia','EE');

INSERT INTO public.country_list (id,"name",code) VALUES 
(71,'Ethiopia','ET'),
(72,'Falkland Islands (Malvinas)','FK'),
(73,'Faroe Islands','FO'),
(74,'Fiji','FJ'),
(75,'Finland','FI'),
(76,'France','FR'),
(77,'French Guiana','GF'),
(78,'French Polynesia','PF'),
(79,'French Southern Territories','TF'),
(80,'Gabon','GA');

INSERT INTO public.country_list (id,"name",code) VALUES 
(81,'Gambia','GM'),
(82,'Georgia','GE'),
(83,'Germany','DE'),
(84,'Ghana','GH'),
(85,'Gibraltar','GI'),
(86,'Greece','GR'),
(87,'Greenland','GL'),
(88,'Grenada','GD'),
(89,'Guadeloupe','GP'),
(90,'Guam','GU');

INSERT INTO public.country_list (id,"name",code) VALUES 
(91,'Guatemala','GT'),
(92,'Guernsey','GG'),
(93,'Guinea','GN'),
(94,'Guinea-Bissau','GW'),
(95,'Guyana','GY'),
(96,'Haiti','HT'),
(97,'Heard Island and McDonald Islands','HM'),
(98,'Holy See (Vatican City State)','VA'),
(99,'Honduras','HN'),
(100,'Hong Kong','HK');

INSERT INTO public.country_list (id,"name",code) VALUES 
(101,'Hungary','HU'),
(102,'Iceland','IS'),
(103,'India','IN'),
(104,'Indonesia','ID'),
(105,'Iran, Islamic Republic of','IR'),
(106,'Iraq','IQ'),
(107,'Ireland','IE'),
(108,'Isle of Man','IM'),
(109,'Israel','IL'),
(110,'Italy','IT');

INSERT INTO public.country_list (id,"name",code) VALUES 
(111,'Jamaica','JM'),
(112,'Japan','JP'),
(113,'Jersey','JE'),
(114,'Jordan','JO'),
(115,'Kazakhstan','KZ'),
(116,'Kenya','KE'),
(117,'Kiribati','KI'),
(118,'Korea, Democratic People''s Republic of','KP'),
(119,'Korea, Republic of','KR'),
(120,'Kuwait','KW');

INSERT INTO public.country_list (id,"name",code) VALUES 
(121,'Kyrgyzstan','KG'),
(122,'Lao People''s Democratic Republic','LA'),
(123,'Latvia','LV'),
(124,'Lebanon','LB'),
(125,'Lesotho','LS'),
(126,'Liberia','LR'),
(127,'Libya','LY'),
(128,'Liechtenstein','LI'),
(129,'Lithuania','LT'),
(130,'Luxembourg','LU');

INSERT INTO public.country_list (id,"name",code) VALUES 
(131,'Macao','MO'),
(132,'Macedonia, the Former Yugoslav Republic of','MK'),
(133,'Madagascar','MG'),
(134,'Malawi','MW'),
(135,'Malaysia','MY'),
(136,'Maldives','MV'),
(137,'Mali','ML'),
(138,'Malta','MT'),
(139,'Marshall Islands','MH'),
(140,'Martinique','MQ');

INSERT INTO public.country_list (id,"name",code) VALUES 
(141,'Mauritania','MR'),
(142,'Mauritius','MU'),
(143,'Mayotte','YT'),
(144,'Mexico','MX'),
(145,'Micronesia, Federated States of','FM'),
(146,'Moldova, Republic of','MD'),
(147,'Monaco','MC'),
(148,'Mongolia','MN'),
(149,'Montenegro','ME'),
(150,'Montserrat','MS');

INSERT INTO public.country_list (id,"name",code) VALUES 
(151,'Morocco','MA'),
(152,'Mozambique','MZ'),
(153,'Myanmar','MM'),
(154,'Namibia','NA'),
(155,'Nauru','NR'),
(156,'Nepal','NP'),
(157,'Netherlands','NL'),
(158,'New Caledonia','NC'),
(159,'New Zealand','NZ'),
(160,'Nicaragua','NI');

INSERT INTO public.country_list (id,"name",code) VALUES 
(161,'Niger','NE'),
(162,'Nigeria','NG'),
(163,'Niue','NU'),
(164,'Norfolk Island','NF'),
(165,'Northern Mariana Islands','MP'),
(166,'Norway','NO'),
(167,'Oman','OM'),
(168,'Pakistan','PK'),
(169,'Palau','PW'),
(170,'Palestine, State of','PS');

INSERT INTO public.country_list (id,"name",code) VALUES 
(171,'Panama','PA'),
(172,'Papua New Guinea','PG'),
(173,'Paraguay','PY'),
(174,'Peru','PE'),
(175,'Philippines','PH'),
(176,'Pitcairn','PN'),
(177,'Poland','PL'),
(178,'Portugal','PT'),
(179,'Puerto Rico','PR'),
(180,'Qatar','QA');

INSERT INTO public.country_list (id,"name",code) VALUES 
(181,'Réunion','RE'),
(182,'Romania','RO'),
(183,'Russian Federation','RU'),
(184,'Rwanda','RW'),
(185,'Saint Barthélemy','BL'),
(186,'Saint Helena, Ascension and Tristan da Cunha','SH'),
(187,'Saint Kitts and Nevis','KN'),
(188,'Saint Lucia','LC'),
(189,'Saint Martin (French part)','MF'),
(190,'Saint Pierre and Miquelon','PM');

INSERT INTO public.country_list (id,"name",code) VALUES 
(191,'Saint Vincent and the Grenadines','VC'),
(192,'Samoa','WS'),
(193,'San Marino','SM'),
(194,'Sao Tome and Principe','ST'),
(195,'Saudi Arabia','SA'),
(196,'Senegal','SN'),
(197,'Serbia','RS'),
(198,'Seychelles','SC'),
(199,'Sierra Leone','SL'),
(200,'Singapore','SG');

INSERT INTO public.country_list (id,"name",code) VALUES 
(201,'Sint Maarten (Dutch part)','SX'),
(202,'Slovakia','SK'),
(203,'Slovenia','SI'),
(204,'Solomon Islands','SB'),
(205,'Somalia','SO'),
(206,'South Africa','ZA'),
(207,'South Georgia and the South Sandwich Islands','GS'),
(208,'South Sudan','SS'),
(209,'Spain','ES'),
(210,'Sri Lanka','LK');

INSERT INTO public.country_list (id,"name",code) VALUES 
(211,'Sudan','SD'),
(212,'Suriname','SR'),
(213,'Svalbard and Jan Mayen','SJ'),
(214,'Swaziland','SZ'),
(215,'Sweden','SE'),
(216,'Switzerland','CH'),
(217,'Syrian Arab Republic','SY'),
(218,'Taiwan, Province of China','TW'),
(219,'Tajikistan','TJ'),
(220,'Tanzania, United Republic of','TZ');

INSERT INTO public.country_list (id,"name",code) VALUES 
(221,'Thailand','TH'),
(222,'Timor-Leste','TL'),
(223,'Togo','TG'),
(224,'Tokelau','TK'),
(225,'Tonga','TO'),
(226,'Trinidad and Tobago','TT'),
(227,'Tunisia','TN'),
(228,'Turkey','TR'),
(229,'Turkmenistan','TM'),
(230,'Turks and Caicos Islands','TC');

INSERT INTO public.country_list (id,"name",code) VALUES 
(231,'Tuvalu','TV'),
(232,'Uganda','UG'),
(233,'Ukraine','UA'),
(234,'United Arab Emirates','AE'),
(235,'United Kingdom','GB'),
(236,'United States','US'),
(237,'United States Minor Outlying Islands','UM'),
(238,'Uruguay','UY'),
(239,'Uzbekistan','UZ'),
(240,'Vanuatu','VU');

INSERT INTO public.country_list (id,"name",code) VALUES 
(241,'Venezuela, Bolivarian Republic of','VE'),
(242,'Viet Nam','VN'),
(243,'Virgin Islands, British','VG'),
(244,'Virgin Islands, U.S.','VI'),
(245,'Wallis and Futuna','WF'),
(246,'Western Sahara','EH'),
(247,'Yemen','YE'),
(248,'Zambia','ZM'),
(249,'Zimbabwe','ZW');

CREATE TABLE IF NOT EXISTS order_category (
    id serial,
    category_name varchar NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO order_category (category_name) VALUES
('Arts and Crafts'),
('Automotive'),
('Baby'),
('Beauty and Personal Care'),
('Books'),
('Computers'),
('Electronics'),
('Women''s Fashion'),
('Men''s Fashion'),
('Girl''s Fashion'),
('Boys'' Fashion'),
('Health and Household'),
('Home and Kitchen'),
('Industrial and Scientific'),
('Luggage'),
('Pet Supplies'),
('Sports and Outdoors'),
('Tools and Home Improvement'),
('Toys and Games');

CREATE TABLE IF NOT EXISTS order_status (
    id serial,
    status_name varchar NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO order_status(status_name) VALUES
('In a box'),
('Canceled'),
('Shipping'),
('Delivered');

CREATE TABLE IF NOT EXISTS orders (
    id bigserial,
    member_id bigint NOT NULL,
    asin char(10) NOT NULL,
    order_category int NOT NULL,
    price numeric(15, 6) NOT NULL,
    product_title varchar NOT NULL,
    product_short_description varchar,
    product_url varchar NOT NULL,
    product_image varchar NOT NULL,
    ordered_on timestamp NOT NULL,
    product_order_status int,
    PRIMARY KEY(id),
    FOREIGN KEY(order_category) REFERENCES order_category(id),
    FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE CASCADE,
    FOREIGN KEY(product_order_status) REFERENCES order_status(id)
);

CREATE INDEX asin_idx ON orders(asin);
CREATE INDEX order_category_idx ON orders(order_category);
CREATE INDEX product_title_idx ON orders(product_short_description);

ALTER TABLE members
ADD COLUMN phone_token varchar NOT NULL;

CREATE TABLE IF NOT EXISTS notifications (
	id bigserial,
	member_id bigint,
	notification_title varchar not null,
	notification_text varchar not null,
	notification_image_url varchar,
	created_at timestamp DEFAULT now(),
	is_read boolean DEFAULT false,
	PRIMARY KEY(id),
	FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS organization_notifications (
    id bigserial,
    organization_id bigint NOT NULL,
    member_id bigint NOT NULL,
    notification_title varchar not null,
    notification_text varchar not null,
    notification_image_url varchar,
    created_at timestamp DEFAULT now(),
    is_read boolean DEFAULT false,
    PRIMARY KEY(id),
    FOREIGN KEY(organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS organization_deliveries (
    id bigserial,
    organization_id bigint NOT NULL,
    order_id bigint NOT NULL,
    courier_id bigint,
    is_delivered boolean DEFAULT false,
    created_at timestamp DEFAULT now(),
    PRIMARY KEY(id),
    FOREIGN KEY(organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY(courier_id) REFERENCES members(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rpi_devices (
    id bigserial,
    security_key varchar NOT NULL,
    member_id bigint NOT NULL,
    host varchar NOT NULL,
    connected boolean DEFAULT false,
    created_at timestamp DEFAULT now(),
    PRIMARY KEY(id),
    FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE CASCADE,
    CONSTRAINT rpi_member_unique UNIQUE(security_key, member_id)
);

ALTER TABLE rpi_devices ADD COLUMN user_security_key varchar;

CREATE TABLE IF NOT EXISTS box_locking (
    id bigserial,
    member_id bigint,
    locked boolean DEFAULT true,
    PRIMARY KEY(id),
    FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE CASCADE
);

-- insert box_locking for member
INSERT INTO box_locking (member_id) VALUES (33);

ALTER TABLE box_locking ADD COLUMN dismantle boolean DEFAULT false;
ALTER TABLE box_locking ADD COLUMN expanding_value int DEFAULT 0;