// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import { range } from "lodash";
import type { NextApiRequest, NextApiResponse } from "next";
import database from "../../../models/database";
import { TemperatureData } from "../../../models/temperature";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<TemperatureData>
) {
  let result = await database.query<TemperatureData>(
    `select * from temperature order by id desc limit 10`
  );
  let data = result.rows;
  res.status(200).json(data[0]);
}
