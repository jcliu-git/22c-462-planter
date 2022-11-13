// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import database from "../../../models/database";
import { moistureData } from "../../../models/moisture";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<moistureData>
) {
  try {
    let result = await database.query<moistureData>(
      "select * from moisture_level order by id desc limit 1"
    );
    let data = result.rows[0];
    res.status(200).json(data);
  } catch (e) {
    res.status(500).end();
  }
}
