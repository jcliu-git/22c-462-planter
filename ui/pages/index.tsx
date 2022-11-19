import Head from "next/head";
import MoistureSensors from "../components/moistureSensors";
import Slideshow from "../components/slideshow";
import { WaterConsumption } from "../components/waterConsumption";
import { WaterLevel } from "../components/waterLevel";
import styles from "../styles/Home.module.css";
import { Box, CustomTheme, Grid, useTheme } from "@mui/material";
import React, { useEffect } from "react";
import { TemperatureSensor } from "../components/temperature";
import { LightSensor } from "../components/light";
import { useDispatch } from "react-redux";
import { Dispatch, RefetchRoutine } from "../models/store";

export default function Dashboard() {
  const dispatch = useDispatch<Dispatch>();
  const theme = useTheme<CustomTheme>();

  useEffect(() => {
    dispatch.refetch.subscribeHub(5000);
    dispatch.refetch.start();
  }, []);

  return (
    <div className={styles.container}>
      <Head>
        <title>Mobile Garden</title>
        <meta name="description" content="Mobile Garden" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Box
        sx={{
          padding: theme.spacing(3),
        }}
      >
        <Grid container spacing={theme.spacing(3)}>
          <Grid
            item
            container
            direction="column"
            spacing={theme.spacing(3)}
            alignItems="center"
            sm={12}
            md={2}
          >
            <Grid item>
              <TemperatureSensor />
              <LightSensor />
            </Grid>
            <Grid item>
              <WaterLevel />
            </Grid>
            <Grid item>
              <p>Moisture Level</p>
              <MoistureSensors />
            </Grid>
          </Grid>
          <Grid
            item
            container
            direction="column"
            sm={12}
            md={10}
            spacing={theme.spacing(3)}
            alignItems="center"
          >
            <Grid item>
              <Slideshow />
            </Grid>
            <Grid
              item
              sx={{
                overflow: "hidden",
              }}
            >
              {/* <WaterConsumption /> */}
            </Grid>
          </Grid>
        </Grid>
      </Box>
    </div>
  );
}
