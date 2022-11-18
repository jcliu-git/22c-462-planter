// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import { range } from "lodash";
import type { NextApiRequest, NextApiResponse } from "next";
import database from "../../../models/database";

interface SunlightData {
  sunlight: number;
  timestamp: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<SunlightData>
) {
  let result = await database.query<SunlightData>(
    `select * from light order by id desc limit 10`
  );
  let data = result.rows;
  res.status(200).json(data[0]);
}
