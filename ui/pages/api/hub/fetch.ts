import axios from "axios";
import type { NextApiRequest, NextApiResponse } from "next";
import { IHubState } from "../../../models/store";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<IHubState>
) {
  try {
    let result = await axios.get("http://127.0.0.1:5000/fetch");
    res.status(200).json(result.data);
  } catch (e) {
    console.log(e);
    res.status(500).end();
  }
}
