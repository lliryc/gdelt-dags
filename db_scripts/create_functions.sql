CREATE FUNCTION raw_content_search_trigger() RETURNS trigger AS $$
begin
  new.tsv_content :=
    setweight(to_tsvector(coalesce(new.extras_xml, '')), 'A') ||
    setweight(to_tsvector(coalesce(new.all_names, '')), 'B') ||
    setweight(to_tsvector(coalesce(new.themes_enhanced, '')), 'C');
  return new;
end
$$ LANGUAGE plpgsql;