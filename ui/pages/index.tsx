import Head from "next/head";
import MoistureSensors from "../components/moistureSensors";
import Slideshow from "../components/slideshow";
import Slider from "../components/slider";
import { WaterConsumption } from "../components/waterConsumption";
import { WaterLevel } from "../components/waterLevel";
import styles from "../styles/Home.module.css";
import { Grid } from "@mui/material";
import React from "react";
import { TemperatureSensor } from "../components/temperature";
import { LightSensor } from "../components/light";
import useSWR from "swr";
import { useDispatch } from "react-redux";
import { Dispatch } from "../models/store";

export default function Dashboard() {
  const dispatch = useDispatch<Dispatch>();
  useSWR(dispatch.dashboard.fetchLatest, {
    refreshInterval: 5000,
  });
  return (
    <div className={styles.container}>
      <Head>
        <title>Mobile Garden</title>
        <meta name="description" content="Mobile Garden" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Grid container>
        <Grid item xs={12} sm={12} md={6}>
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
        <Grid item xs={12} sm={12} md={6}>
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
