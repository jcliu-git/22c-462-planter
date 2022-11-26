import { Box, CustomTheme, Paper, Typography, useTheme } from "@mui/material";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Dispatch, RootState, store } from "../models/store";

export function WaterLevel() {
  const theme = useTheme<CustomTheme>();

  const waterLevelState = useSelector(
    (state: RootState) => state.hub.dashboard.waterLevel
  );
  const controlState = useSelector((state: RootState) => state.hub.control);
  const dispatch = useDispatch<Dispatch>();

  let waterLevelPercent = 0;
  if (controlState.resevoirHeight != 0) {
    waterLevelPercent =
      ((controlState.emptyResevoirHeight - waterLevelState.distance) /
        controlState.resevoirHeight) *
      100;
  }

  if (waterLevelPercent < 0) {
    waterLevelPercent = 0;
  }

  if (waterLevelPercent > 100) {
    waterLevelPercent = 100;
  }

  return (
    <Paper
      sx={{
        display: "block",
        padding: theme.spacing(3),
      }}
    >
      <Typography variant="h6" sx={{ marginBottom: theme.spacing(1) }}>
        Resevoir Water Level
      </Typography>
      <Box
        id="container"
        sx={{
          height: "100px",
          border: "3px solid black",
          background: `rgba(0,0,0, 0.5)`,
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-end",
          position: "relative",
        }}
      >
        <Typography
          display="block"
          position="absolute"
          top="50%"
          left="50%"
          sx={{
            color: "white",
            fontSize: "1.5rem",
            fontWeight: "bold",
            transform: "translate(-50%, -50%)",
          }}
        >
          {Math.round(waterLevelPercent)}%
        </Typography>
        <Box
          id="water"
          sx={{
            height: "100%",
            width: `${waterLevelPercent}%`,
            background: theme.palette.secondary.main,
          }}
        ></Box>
      </Box>
    </Paper>
  );
}
