import { useTheme } from "@mui/material";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Subscription } from "rxjs";
import { Dispatch, RootState, store } from "../models/store";

export function WaterLevel() {
  const theme = useTheme();

  const state = useSelector((state: RootState) => state.dashboard.waterLevel);
  const dispatch = useDispatch<Dispatch>();

  return (
    <div>
      <h1>Water Level</h1>
      <h2>{state.distance}</h2>
    </div>
  );
}
