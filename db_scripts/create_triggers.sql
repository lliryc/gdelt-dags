CREATE TRIGGER gkg_raw_tsv_update BEFORE INSERT OR UPDATE
ON raw.gkg_raw FOR EACH ROW EXECUTE PROCEDURE raw_content_search_trigger();