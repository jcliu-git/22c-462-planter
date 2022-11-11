// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import pg from 'pg'
import database from '../../models/database'

// type Data = {
//   name: string
// }

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  let result = await database.query("select * from moisture_level");
  res.status(200).json(result.rows)
}
