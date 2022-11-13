// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import database from "../../../models/database";
import { waterLevelData } from "../../../models/waterLevel";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<waterLevelData>
) {
  try {
    let result = await database.query<waterLevelData>(
      "select * from water_level order by id desc limit 1"
    );
    res.status(200).json(result.rows[0]);
  } catch (e) {
    res.status(500).end();
  }
}
