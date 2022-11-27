import type { NextApiRequest, NextApiResponse } from "next";
import { Client } from "pg";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const client = new Client({
      connectionString: process.env.AZURE_PG_URI,
      // ssl: {
      //   rejectUnauthorized: false,
      // },
    });
    await client.connect();

    const result = await client.query(
      "SELECT * FROM photos where phototype = 'periodic'"
    );

    res.status(200).json(result.rows);
  } catch (e) {
    console.log(e);
    res.status(500).end();
  }
}
