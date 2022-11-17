import { useTheme } from "@mui/material";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Subscription } from "rxjs";
import { lightData } from "../models/light";
import { Dispatch, RootState, store } from "../models/store";

export function LightSensor() {
  const theme = useTheme();

  const light = useSelector((state: RootState) => state.light);
  const dispatch = useDispatch<Dispatch>();
  console.log(light);
  return (
    <div>
      <h1>Luminosity</h1>
      <h2>{light.value}</h2>
    </div>
  );
}
