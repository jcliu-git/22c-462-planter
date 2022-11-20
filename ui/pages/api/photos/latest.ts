// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import database from "../../../models/database";
import { IPhotoData } from "../../../models/store";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<IPhotoData[]>
) {
  let result = await database.query<IPhotoData>(
    "select * from photos order by id desc limit 10"
  );
  res.status(200).json(result.rows);
}
