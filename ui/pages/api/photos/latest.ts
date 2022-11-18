// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import database from "../../../models/database";
import { photoData } from "../../../models/photos";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<photoData[]>
) {
  let result = await database.query<photoData>(
    "select * from photos order by id desc limit 10"
  );
  res.status(200).json(result.rows);
}
