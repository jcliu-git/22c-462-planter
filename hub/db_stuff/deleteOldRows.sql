DO $$
DECLARE
tb_name varchar;
BEGIN
FOR tb_name IN SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public' AND tablename NOT LIKE 'z_%'
	LOOP
	    EXECUTE 'DELETE FROM ' || tb_name || ' WHERE DATE(timestamp) < CURRENT_DATE - interval ''7 day''';
	END LOOP;
END$$;