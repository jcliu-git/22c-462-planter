import { Box, CustomTheme, Paper, useTheme } from "@mui/material";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Dispatch, RootState, store } from "../models/store";

export function WaterLevel() {
  const theme = useTheme<CustomTheme>();

  const waterLevelState = useSelector(
    (state: RootState) => state.dashboard.waterLevel
  );
  const controlState = useSelector((state: RootState) => state.control);
  const dispatch = useDispatch<Dispatch>();

  return (
    <Paper
      sx={{
        display: "inline-block",
        padding: theme.spacing(3),
      }}
    >
      <Box
        id="container"
        sx={{
          width: "200px",
          height: "400px",
          margin: theme.spacing(3),
          border: "3px solid black",
          borderTop: "none",
          background: `rgba(0,0,0, 0.5)`,
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-end",
        }}
      >
        <Box
          id="water"
          sx={{
            width: "100%",
            height: `${
              (1 - waterLevelState.distance / controlState.resevoirHeight) * 100
            }%`,
            background: theme.palette.secondary.main,
          }}
        ></Box>
      </Box>
    </Paper>
  );
}
