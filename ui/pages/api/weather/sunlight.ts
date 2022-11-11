// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import { range } from "lodash";
import type { NextApiRequest, NextApiResponse } from "next";

interface SunlightData {
  sunlight: number;
  timestamp: string;
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<SunlightData[]>
) {
  res.status(200).json(
    range(1, 29).map((day) => ({
      sunlight: Math.random() * 100,
      timestamp: `2021-08-${day}`,
    }))
  );
}
