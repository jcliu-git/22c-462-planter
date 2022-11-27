import type { NextApiRequest, NextApiResponse } from "next";
import { ITemperatureData } from "../../../models/store";
import { Client } from "pg";

const client = new Client({
  connectionString: process.env.AZURE_PG_URI,
  // ssl: {
  //   rejectUnauthorized: false,
  // },
});

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ITemperatureData>
) {
  try {
    await client.connect();

    let result = await client
      .query("select * from temperature order by timestamp desc limit 1")
      .then((result) => result.rows[0]);

    res.status(200).json(result);
  } catch (e) {
    console.log(e);
    res.status(500).end();
  } finally {
    await client.end();
  }
}
