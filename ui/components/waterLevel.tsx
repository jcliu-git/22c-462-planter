import { Box, CustomTheme, Paper, Typography, useTheme } from "@mui/material";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Dispatch, RootState, store } from "../models/store";
import Image from '../public/wave.png';
import Particles, { ISourceOptions } from "react-tsparticles";

export function WaterLevel() {
  const theme = useTheme<CustomTheme>();
  const options: ISourceOptions = {
    background: {
      color: "#0d47a1",
    },
    interactivity: {
      events: {
        onClick: {
          enable: true,
          mode: "push",
        },
        onHover: {
          enable: true,
          mode: "repulse",
        },
        resize: true,
      },
      modes: {
        bubble: {
          distance: 400,
          duration: 2,
          opacity: 0.8,
          size: 40,
        },
        push: {
          quantity: 4,
        },
        repulse: {
          distance: 200,
          duration: 0.4,
        },
      },
    },
    particles: {
      color: {
        value: "#ffffff",
      },
      links: {
        color: "#ffffff",
        distance: 150,
        enable: true,
        opacity: 0.5,
        width: 1,
      },
      collisions: {
        enable: true,
      },
      move: {
        direction: "none",
        enable: true,
        outMode: "bounce",
        random: false,
        speed: 6,
        straight: false,
      },
      number: {
        density: {
          enable: true,
          value_area: 800,
        },
        value: 80,
      },
      opacity: {
        value: 0.5,
      },
      shape: {
        type: "circle",
      },
      size: {
        random: true,
        value: 5,
      },
    },
  };
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
      <Particles options={options} />;
    </Paper>
  );
}
