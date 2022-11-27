import type { NextApiRequest, NextApiResponse } from "next";
import { IMoistureData } from "../../../models/store";
import { Client } from "pg";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<IMoistureData>
) {
  const client = new Client({
    connectionString: process.env.AZURE_PG_URI,
    // ssl: {
    //   rejectUnauthorized: false,
    // },
  });
  try {
    await client.connect();

    let result = await client
      .query("select * from moisture_level order by timestamp desc limit 1")
      .then((result) => result.rows[0]);

    res.status(200).json(result);
  } catch (e) {
    console.log(e);
    res.status(500).end();
  } finally {
    await client.end();
  }
}
