// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import database from "../../../models/database";
import { moistureData } from "../../../models/moisture";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<moistureData>
) {
  try {
    // let result = await database.query(
    //   "select * from moisture_level order by id desc limit 1"
    // );
    // let data = result.rows[0];
    // res.status(200).json(data);
    res.status(200).json({
      timestamp: (new Date()).toISOString(),
      sensor1: 150,
      sensor2: 620,
      sensor3: 620,
      sensor4: 290,
      sensor5: 710,
      sensor6: 500,
      sensor7: 333,
      sensor8: 620,
    })
  } catch (e) {
    res.status(500).end();
  }
}
