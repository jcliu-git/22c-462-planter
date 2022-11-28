import { AzureFunction, Context, HttpRequest } from "@azure/functions";
import { Client } from "pg";

const httpTrigger: AzureFunction = async function (
  context: Context,
  req: HttpRequest
): Promise<void> {
  let client = new Client({
    connectionString: process.env.POSTGRES_CONNECTION_STRING,
  });
  await client.connect();
  await client.query(
    `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'postgres' AND pid <> pg_backend_pid() AND state in ('idle');`
  );
  context.res = {
    status: 200,
  };
};

export default httpTrigger;
