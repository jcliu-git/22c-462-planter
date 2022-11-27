import { AzureFunction, Context } from "@azure/functions";
import { Client } from "pg";

const timerTrigger: AzureFunction = async function (
  context: Context,
  myTimer: any
): Promise<void> {
  var timeStamp = new Date().toISOString();

  const client = new Client({
    connectionString: process.env.POSTGRES_CONNECTION_STRING,
  });

  await client.connect();

  const result = await client.query(
    `
        DO $$
        DECLARE
        tb_name varchar;
        BEGIN
        FOR tb_name IN SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public' AND tablename NOT LIKE 'z_%'
          LOOP
              EXECUTE 'DELETE FROM ' || tb_name || ' WHERE DATE(timestamp) < CURRENT_DATE - interval ''7 day''';
          END LOOP;
        END$$;
      `
  );

  await client.end();

  context.log("Pruned database", timeStamp);
};

export default timerTrigger;
