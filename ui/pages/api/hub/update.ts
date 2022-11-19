import axios from "axios";
import type { NextApiRequest, NextApiResponse } from "next";
import { HubState, IHubState } from "../../../models/store";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const body = req.body as IHubState;
  try {
    await axios.post("http://127.0.0.1:5000/update", body);
    res.status(200).end();
  } catch (e) {
    console.log(e);
    res.status(500).end();
  }
}
