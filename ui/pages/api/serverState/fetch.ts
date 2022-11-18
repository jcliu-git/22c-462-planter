// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import { ServerState } from '../../../models/store';
import axios from 'axios';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ServerState>
) {
  let result = await axios<ServerState>('/fetch', {
    baseURL: "localhost:5000",
  })
  res.status(200).json(result.data)
}
