import { AzureFunction, Context, HttpRequest } from "@azure/functions";
import { Client } from "pg";

const httpTrigger: AzureFunction = async function (
  context: Context,
  req: HttpRequest
): Promise<void> {
  try {
    let client = new Client({
      connectionString: process.env.POSTGRES_CONNECTION_STRING,
    });
    await client.connect();

    let [light, moisture, temperature, waterLevel] = await Promise.all([
      client.query("select * from light order by timestamp desc limit 1"),
      client.query(
        "select * from moisture_level order by timestamp desc limit 1"
      ),
      client.query("select * from temperature order by timestamp desc limit 1"),
      client.query("select * from water_level order by timestamp desc limit 1"),
    ]).then((results) => results.map((r) => r.rows[0]));

    context.res = {
      status: 200,
      body: {
        dashboard: {
          waterLevel,
          moisture,
          light,
          temperature,
        },
        control: {
          planterEnabled: false,
          hydroponicEnabled: false,
          dryThreshold: 0,
          flowTime: 0,
          calibrating: false,
          resevoirHeight: 0,
          emptyResevoirHeight: 0,
          fullResevoirHeight: 0,
        },
        websocketConnected: false,
      },
    };
    await client.end();
  } catch (e) {
    context.res = {
      status: 500,
      e,
    };
  }
};

export default httpTrigger;
