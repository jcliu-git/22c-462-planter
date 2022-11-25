// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs/promises";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const files = await fs.readdir("./public/camera/motion");

    res.status(200).json(
      files.map((f) => ({
        filepath: `/camera/motion/${f}`,
        timestamp: f.split(".")[0],
        width: 780,
        height: 240,
      }))
    );
  } catch (e) {
    console.log(e);
    res.status(500).end();
  }
}
