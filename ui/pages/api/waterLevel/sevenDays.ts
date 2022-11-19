// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import { groupBy } from "lodash";
import type { NextApiRequest, NextApiResponse } from "next";
import database from "../../../models/database";
import { IWaterLevelData, WaterConsumptionByDay } from "../../../models/store";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<WaterConsumptionByDay>
) {
  try {
    let currentDay = new Date().toISOString().replace(/T.*/, "");
    let sevenDaysAgo_ = new Date();
    sevenDaysAgo_.setDate(sevenDaysAgo_.getDate() - 7);
    let sevenDaysAgo = sevenDaysAgo_.toISOString().replace(/T.*/, ""); //get the date only

    let result = await database.query<IWaterLevelData>(
      "select * from water_level where date(timestamp) between '" +
        sevenDaysAgo +
        "' AND '" +
        currentDay +
        "';"
    );

    let rowsByDate = groupBy(result.rows, (row) => {
      return new Date(row.timestamp).getDay();
    });

    let data = Object.keys(rowsByDate).reduce((acc, key) => {
      let rows = rowsByDate[key];
      let consumption = 0;

      for (let i = 1; i < rows.length - 1; i++) {
        if (rows[i].distance > rows[i - 1].distance) {
          consumption += rows[i].distance - rows[i - 1].distance;
        }
      }

      acc[key] = consumption;

      return acc;
    }, {} as WaterConsumptionByDay);
    res.status(200).json(data);
  } catch (e) {
    res.status(500).end();
  }
}
