import type { NextApiRequest, NextApiResponse } from "next";
import { IHubState } from "../../../models/store";
import { Client } from "pg";

// this route is used to fetch the current state of the hub
// without connection to it via websockets

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<IHubState>
) {
  try {
    const client = new Client({
      connectionString: process.env.AZURE_PG_URI,
      // ssl: {
      //   rejectUnauthorized: false,
      // },
    });
    await client.connect();
    let [waterLevel, moisture, light, temperature] = await Promise.all([
      client.query("select * from water_level order by timestamp desc limit 1"),
      client.query(
        "select * from moisture_level order by timestamp desc limit 1"
      ),
      client.query("select * from light order by timestamp desc limit 1"),
      client.query("select * from temperature order by timestamp desc limit 1"),
    ]).then((results) => results.map((r) => r.rows[0]));

    let result: IHubState = {
      dashboard: {
        waterLevel: {
          timestamp: waterLevel.timestamp,
          distance: waterLevel.distance,
        },
        moisture: {
          timestamp: moisture.timestamp,
          sensor1: moisture.sensor1,
          sensor2: moisture.sensor2,
          sensor3: moisture.sensor3,
          sensor4: moisture.sensor4,
          sensor5: moisture.sensor5,
          sensor6: moisture.sensor6,
          sensor7: moisture.sensor7,
          sensor8: moisture.sensor8,
        },
        light: {
          timestamp: light.timestamp,
          luminosity: light.luminosity,
        },
        temperature: {
          timestamp: temperature.timestamp,
          fahrenheit: temperature.fahrenheit,
        },
        photos: [],
      },
      control: {
        planterEnabled: false,
        hydroponicEnabled: false,
        dryThreshold: 0,
        flowTime: 0,
        calibrating: false,
        resevoirHeight: 0,
        emptyResevoirHeight: 0,
        fullResevoirHeight: 0,
      },
      websocketConnected: false,
    };

    res.status(200).json(result);
  } catch (e) {
    console.log(e);
    res.status(500).end();
  }
}
