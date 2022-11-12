import { useTheme } from "@mui/material";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Subscription } from "rxjs";
import { temperatureData } from "../models/temperature";
import { Dispatch, RootState, store } from "../models/store";

export function TemperatureSensor() {
  const theme = useTheme();

  const temperature = useSelector((state: RootState) => state.temperature);
  const dispatch = useDispatch<Dispatch>();

  return (
    <div>
      <h1>Temperature</h1>
      <h2>{temperature.celsius}</h2>
    </div>
  );
}