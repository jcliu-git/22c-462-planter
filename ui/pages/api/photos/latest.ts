// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import pg from "pg";
import database from "../../../models/database";
import { photoData } from "../../../models/store";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<photoData[]>
) {
  let result = await database.query<photoData>(
    "select * from picture order by id desc limit 10"
  );
  res.status(200).json(result.rows);
}
