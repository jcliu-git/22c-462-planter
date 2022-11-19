import { Card, CardContent, Typography, useTheme } from "@mui/material";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Dispatch, RootState, store } from "../models/store";

export function TemperatureSensor() {
  const theme = useTheme();

  const state = useSelector(
    (state: RootState) => state.hub.dashboard.temperature
  );

  // console.log(temperature);

  return (
    <Card sx={{ display: "inline-block", padding: theme.spacing(3) }}>
      <Typography variant="h3" component="span">
        {state.fahrenheit.toFixed(2)}
      </Typography>
      <Typography variant="h6" component="sup" sx={{ verticalAlign: "top" }}>
        °F
      </Typography>
    </Card>
  );
}
