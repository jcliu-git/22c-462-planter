import { AzureFunction, Context, HttpRequest } from "@azure/functions";
import { Client } from "pg";

const httpTrigger: AzureFunction = async function (
  context: Context,
  req: HttpRequest
): Promise<void> {
  try {
    const client = new Client({
      connectionString: process.env.POSTGRES_CONNECTION_STRING,
    });
    await client.connect();

    const [periodic, motion] = await Promise.all([
      client.query("SELECT * FROM photos where phototype = 'periodic'"),
      client.query("SELECT * FROM photos where phototype = 'motion'"),
    ]).then((results) => results.map((r) => r.rows));

    context.res = {
      status: 200,
      body: {
        periodic,
        motion,
      },
    };

    await client.end();
  } catch (e) {
    console.error(e);
    context.res = {
      status: 500,
      e,
    };
  }
};

export default httpTrigger;
