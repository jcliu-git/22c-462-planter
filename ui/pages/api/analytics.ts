// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import _ from "lodash";
import type { NextApiRequest, NextApiResponse } from "next";
import { Client } from "pg";

interface pulse {
  hour: number;
  waterLevel: number;
  moisture: number;
  light: number;
  temperature: number;
}

function smooth(data: any[], key: string, windowSize: number) {
  return _.map(data, (d, i) => {
    if (i < windowSize) {
      return d;
    }
    const window = _.slice(data, i - windowSize, i);
    const values = _.map(window, (w) => w[key]);
    const avg = _.sum(values) / values.length;
    return {
      ...d,
      [key]: avg,
    };
  });
}

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
        rows = smooth(rows, "distance", 5);
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

    let water_level = await client.query(
      "select * from water_level where timestamp > now() - interval '1 day'"
    );
    // get data from moisture/light/temp/water level from last 24 hours
    // group by hour and get average of each value for that hour
    let water_level_by_hour = _.chain(water_level.rows)
      .groupBy((row) => new Date(row.timestamp).getHours())
      .map((rows, hour) => {
        let waterLevel = _.meanBy(rows, (row) => row.distance);
        return {
          hour,
          waterLevel,
        };
      })
      .value();

    let moisture = await client.query(
      "select * from moisture_level where timestamp > now() - interval '1 day'"
    );

    let moisture_by_hour = _.chain(moisture.rows)
      .groupBy((row) => new Date(row.timestamp).getHours())
      .map((rows, hour) => {
        let moisture = _.meanBy(rows, (row) =>
          _.mean([
            row.sensor1,
            row.sensor2,
            row.sensor3,
            row.sensor4,
            row.sensor5,
            row.sensor6,
            row.sensor7,
            row.sensor8,
          ])
        );
        return {
          hour,
          moisture,
        };
      })
      .value();

    let light = await client.query(
      "select * from light where timestamp > now() - interval '1 day'"
    );

    let light_by_hour = _.chain(light.rows)
      .groupBy((row) => new Date(row.timestamp).getHours())
      .map((rows, hour) => {
        let light = _.meanBy(rows, (row) => row.luminosity);
        return {
          hour,
          light,
        };
      })
      .value();

    let temp = await client.query(
      "select * from temperature where timestamp > now() - interval '1 day'"
    );

    let temp_by_hour = _.chain(temp.rows)
      .groupBy((row) => new Date(row.timestamp).getHours())
      .map((rows, hour) => {
        let temperature = _.meanBy(rows, (row) => row.fahrenheit);
        return {
          hour,
          temperature,
        };
      })
      .value();

    let systemPulse = _.reduce(
      _.range(24),
      (acc, hour) => {
        let datum = {} as pulse;

        datum.hour = hour;
        datum.waterLevel = (
          _.find(water_level_by_hour, (row) => parseInt(row.hour) == hour) || {
            waterLevel: 0,
          }
        ).waterLevel;

        datum.moisture = (
          _.find(moisture_by_hour, (row) => parseInt(row.hour) == hour) || {
            moisture: 0,
          }
        ).moisture;

        datum.light = (
          _.find(light_by_hour, (row) => parseInt(row.hour) == hour) || {
            light: 0,
          }
        ).light;

        datum.temperature = (
          _.find(temp_by_hour, (row) => parseInt(row.hour) == hour) || {
            temperature: 0,
          }
        ).temperature;

        acc.push(datum);
        return acc;
      },
      [] as pulse[]
    );

    res.status(200).json({
      waterConsumptionByDay,
      systemPulse,
    });

    await client.end();
  } catch (e) {
    console.log(e);
    res.status(500).end();
  }
}
