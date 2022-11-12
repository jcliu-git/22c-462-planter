import { useTheme } from "@mui/material";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Subscription } from "rxjs";
import { Dispatch, RootState, store } from "../models/store";
import { waterLevelData } from "../models/waterLevel";

export function WaterLevel() {
  const theme = useTheme();

  const waterLevel = useSelector((state: RootState) => state.waterLevel);
  const dispatch = useDispatch<Dispatch>();


  return (
    <div>
      <h1>Water Level</h1>
      <h2>{waterLevel.level}</h2>
    </div>
  );
}
