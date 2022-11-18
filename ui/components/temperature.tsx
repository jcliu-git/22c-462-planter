import { useTheme } from "@mui/material";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Dispatch, RootState, store } from "../models/store";

export function TemperatureSensor() {
  const theme = useTheme();

  const state = useSelector((state: RootState) => state.dashboard.temperature);
  const dispatch = useDispatch<Dispatch>();

  // console.log(temperature);

  return (
    <div>
      <h1>Temperature</h1>
      <h2>{state.temperature.toFixed(2)}</h2>
    </div>
  );
}
