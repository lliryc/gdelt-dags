-- raw.gkg_raw definition

-- GDELT 2.0 Global Knowledge Graph Codebook (V2.1) (http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf)

-- raw.gkg_raw definition

-- Drop table

-- DROP TABLE raw.gkg_raw;

-- raw.gkg_raw definition

-- GDELT 2.0 Global Knowledge Graph Codebook (V2.1) (http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf)

-- raw.gkg_raw definition

-- Drop table

-- DROP TABLE raw.gkg_raw;

CREATE TABLE raw.gkg_raw (
	record_uuid uuid DEFAULT gen_random_uuid() NOT NULL,
	record_id varchar(100) NOT NULL,
	date_label varchar(100) NULL,
	source_collection_id int4 NULL,
	source_common_name varchar(1000) NULL,
	document_identifier varchar(1000) NULL,
	counts text NULL,
	counts_v2 text NULL,
	themes text NULL,
	themes_enhanced text NULL,
	locations text NULL,
	locations_enhanced text NULL,
	persons text NULL,
	persons_enhanced text NULL,
	organizations text NULL,
	organizations_enhanced text NULL,
	tone varchar(1000) NULL,
	dates_enhanced text NULL,
	gcam text NULL,
	sharing_image varchar(1000) NULL,
	related_images text NULL,
	social_image_embeds text NULL,
	social_video_embeds text NULL,
	quotations text NULL,
	all_names text NULL,
	amounts text NULL,
	translation_info text NULL,
	extras_xml text NULL,
	date_dt timestamp NOT NULL,
	trans_type  varchar(50) NOT NULL,
	tsv_content tsvector null,
	created timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	modified timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	processed bool DEFAULT false NOT null,
	CONSTRAINT gkg_raw_pk PRIMARY KEY (record_uuid, date_dt)
) PARTITION BY RANGE (date_dt);

-- Create the archive partition for all data before 2024-01-01
CREATE TABLE raw.gkg_raw_archive PARTITION OF raw.gkg_raw
    FOR VALUES FROM (MINVALUE) TO ('2024-01-01');

-- Create monthly partitions from 2024-01-01 to 2026-02-01
DO $$
DECLARE
    start_date DATE := '2024-01-01';
    end_date DATE := '2026-02-01';
    current_partition_date DATE := start_date;
BEGIN
    WHILE current_partition_date < end_date LOOP
        EXECUTE format(
            'CREATE TABLE raw.gkg_raw_%s PARTITION OF raw.gkg_raw
            FOR VALUES FROM (%L) TO (%L)',
            to_char(current_partition_date, 'YYYYMM'),
            current_partition_date,
            current_partition_date + INTERVAL '1 month'
        );
        current_partition_date := current_partition_date + INTERVAL '1 month';
    END LOOP;
END $$;

CREATE INDEX gkg_raw_created_idx ON raw.gkg_raw USING btree (created);
CREATE INDEX gkg_raw_date_dt_idx ON raw.gkg_raw USING btree (date_dt);

CREATE TRIGGER gkg_raw_tsv_update BEFORE INSERT OR UPDATE
ON raw.gkg_raw FOR EACH ROW EXECUTE PROCEDURE raw_content_search_trigger();