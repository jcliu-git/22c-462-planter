import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  res.status(200).send(process.env.AZURE_PG_URI?.slice(0, 10));
}
