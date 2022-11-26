// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import _ from "lodash";
import type { NextApiRequest, NextApiResponse } from "next";
import { Client } from "pg";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const client = new Client({
      connectionString: process.env.AZURE_PG_URI,
      // ssl: {
      //   rejectUnauthorized: false,
      // },
    });
    await client.connect();
    let result = await client.query(
      "select * from water_level where timestamp > now() - interval '7 day'"
    );
    // let waterConsumptionByDay = {};
    let waterConsumptionByDay = _.chain(result.rows)
      .groupBy((row) => new Date(row.timestamp).getDate())
      .map((rows, date) => {
        let litres = 0;
        for (let i = 1; i < rows.length; i++) {
          let prev = rows[i - 1];
          let curr = rows[i];
          if (curr.distance > prev.distance) {
            litres += curr.distance - prev.distance;
          }
        }
        return {
          date,
          litres,
        };
      });
    res.status(200).json({
      waterConsumptionByDay,
      systemPulse: [],
    });
  } catch (e) {
    console.log(e);
    res.status(500).end();
  }
}
