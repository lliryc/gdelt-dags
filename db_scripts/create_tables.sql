-- raw.gkg_raw definition

-- GDELT 2.0 Global Knowledge Graph Codebook (V2.1) (http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf)

-- Drop table

-- DROP TABLE raw.gkg_raw;

-- raw.gkg_raw definition

-- Drop table

-- DROP TABLE raw.gkg_raw;

CREATE TABLE raw.gkg_raw (
	record_id varchar(100) NOT NULL,
	date_label varchar(100) NULL,
	source_collection_id int4 NULL,
	source_common_name varchar(100) NULL,
	document_identifier varchar(100) NULL,
	counts varchar(2000) NULL,
	counts_v2 varchar(2000) NULL,
	themes varchar(5000) NULL,
	themes_enhanced varchar(5000) NULL,
	locations varchar(5000) NULL,
	locations_enhanced varchar(5000) NULL,
	persons varchar(5000) NULL,
	persons_enhanced varchar(5000) NULL,
	organizations varchar(5000) NULL,
	organizations_enhanced varchar(5000) NULL,
	tone varchar(500) NULL,
	dates_enhanced varchar(5000) NULL,
	gcam text NULL,
	sharing_image varchar(500) NULL,
	related_images varchar(5000) NULL,
	social_image_embeds varchar(5000) NULL,
	quotations varchar(5000) NULL,
	all_names varchar(5000) NULL,
	amounts varchar(5000) NULL,
	translation_info varchar(5000) NULL,
	extras_xml text NULL,
	processed bool DEFAULT false NOT NULL,
	CONSTRAINT gkg_raw_pk PRIMARY KEY (record_id)
);
