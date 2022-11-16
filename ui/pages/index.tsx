import { once } from "lodash";
import Head from "next/head";
import MoistureSensors from "../components/moistureSensors";
import Slideshow from "../components/slideshow";
import Slider from "../components/slider";
import { WaterConsumption } from "../components/waterConsumption";
import { WaterLevel } from "../components/waterLevel";
import { Scheduler } from "../models/scheduler";
import { store } from "../models/store";
import styles from "../styles/Home.module.css";
import { Grid, Theme, useTheme } from "@mui/material";
import React from "react";
import { TemperatureSensor } from "../components/temperature";
import { LightSensor } from "../components/light";

let scheduler = new Scheduler();

scheduler.addRoutines(
  store.dispatch.waterLevel.fetchLatestWaterLevelLevels,
  store.dispatch.moisture.fetchLatestMoistureLevels,
  store.dispatch.temperature.fetchLatestTemperature,
  store.dispatch.photos.fetchLatestPhotos,
  store.dispatch.light.fetchLatestLight
);

scheduler.start();

store.dispatch.moisture.fetchLatestMoistureLevels();
store.dispatch.waterLevel.fetchLatestWaterLevelLevels();
store.dispatch.photos.fetchLatestPhotos();
store.dispatch.temperature.fetchLatestTemperature();
store.dispatch.light.fetchLatestLight();

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Mobile Garden</title>
        <meta name="description" content="Mobile Garden" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Grid container>
        <Grid item xl={12}>
          <Grid container direction="column">
            <Grid item xl={12}>
              <p>Temperature + Light</p>
              <TemperatureSensor />
              <LightSensor />
            </Grid>
            <Grid item xl={12}>
              <p>Current Water Level</p>
              <WaterLevel />
            </Grid>
            <Grid item xl={12}>
              <p>Moisture Level Controls</p>
              <Slider />
            </Grid>
            <Grid item xl={12}>
              <p>Moisture Level</p>
              <MoistureSensors />
            </Grid>
          </Grid>
        </Grid>
        <Grid item xl={12}>
          <Grid container direction="column"></Grid>
          <Grid item xl={12}>
            <h1 className={styles.hello}>Mobile Garden</h1>
          </Grid>
          <Grid item xl={12}>
            <p>Plant Visitors</p>
            <Slideshow />
          </Grid>
          <Grid item xl={12}>
            <p>Daily Water Consumption</p>
            <WaterConsumption />
          </Grid>
        </Grid>
      </Grid>
    </div>
  );
}
