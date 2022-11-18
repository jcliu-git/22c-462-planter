// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import database from "../../../models/database";
import { waterLevelData } from "../../../models/waterLevel";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<waterLevelData[]>
) {
  try {
    let currentDay = new Date().toISOString().replace(/T.*/, "");
    let sevenDaysAgo_ = new Date();
    sevenDaysAgo_.setDate(sevenDaysAgo_.getDate() - 7);
    let sevenDaysAgo = sevenDaysAgo_.toISOString().replace(/T.*/, ""); //get the date only

    let result = await database.query<waterLevelData>(
      "select * from water_level where date(timestamp) between '" +
        sevenDaysAgo +
        "' AND '" +
        currentDay +
        "';"
    );
    res.status(200).json(result.rows);
  } catch (e) {
    res.status(500).end();
  }
}
