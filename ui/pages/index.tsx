import Head from "next/head";
import MoistureSensors from "../components/moistureSensors";
import { WaterConsumption } from "../components/waterConsumption";
import { WaterLevel } from "../components/waterLevel";
import styles from "../styles/Home.module.css";
import { Box, CustomTheme, Grid, useTheme } from "@mui/material";
import React, { useContext, useEffect } from "react";
import { useDispatch } from "react-redux";
import { Dispatch } from "../models/store";
import { TempAndLight } from "../components/tempAndLight";

export default function Dashboard() {
  const dispatch = useDispatch<Dispatch>();
  const theme = useTheme<CustomTheme>();

  return (
    <Box sx={{ padding: theme.spacing(3) }}>
      <Grid container spacing={theme.spacing(3)}>
        <Grid
          item
          container
          spacing={theme.spacing(3)}
          alignItems="stretch"
          xs={12}
        >
          <Grid item xs={12} sm={6} sx={{ display: "block", width: "100%" }}>
            <TempAndLight />
          </Grid>
          <Grid item xs={12} sm={6} sx={{ display: "block", width: "100%" }}>
            <WaterLevel />
          </Grid>
        </Grid>
        <Grid
          item
          container
          xs={12}
          spacing={theme.spacing(3)}
          alignItems="center"
        >
          <Grid item sx={{ display: "block", width: "100%" }}>
            <MoistureSensors />
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
}
