// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import pg from "pg";
import database from "../../../models/database";

// type Data = {
//   name: string
// }

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  let currentDay = new Date().toISOString();
  let sevenDaysAgo_ = new Date();
  sevenDaysAgo_.setDate(sevenDaysAgo_.getDate() - 7);
  let sevenDaysAgo = sevenDaysAgo_.toISOString();
  let result = await database.query(
    "select SUM(value) from water_level where date(timestamp) between '" +
      currentDay +
      "' AND '" +
      sevenDaysAgo +
      "'"
  );

  res.status(200).json(result.rows);
}
