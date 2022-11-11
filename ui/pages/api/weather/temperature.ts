// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import { range } from "lodash";
import type { NextApiRequest, NextApiResponse } from "next";

interface TemperatureData {
  temperature: number;
  timestamp: string;
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<TemperatureData[]>
) {
  res.status(200).json(
    range(1, 29).map((day) => ({
      temperature: Math.random() * 100,
      timestamp: `2021-08-${day}`,
    }))
  );
}
