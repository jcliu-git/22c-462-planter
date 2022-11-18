// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import { ServerState } from '../../../models/store';
import axios from 'axios';

interface ack {
  updated: boolean;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ack>
) {
  let state = req.body;
  let result = await axios.post<ack>('/update', state, {
    baseURL: "localhost:5000",
  })
  res.status(200).json(result.data)
}
