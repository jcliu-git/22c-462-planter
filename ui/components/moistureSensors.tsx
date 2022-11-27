import { Card, Grid, Theme, Typography, useTheme } from "@mui/material";
import { Box } from "@mui/system";
import { range } from "lodash";
import React from "react";
import { Subscription } from "rxjs";
import { Dispatch, RootState, store } from "../models/store";
import { calcColor } from "../util/color";
import { useSelector, useDispatch } from "react-redux";
import { mix } from "tinycolor2";

export function MoistureSensors(): JSX.Element {
  const theme = useTheme<Theme>();

  const moisture = useSelector(
    (state: RootState) => state.hub.dashboard.moisture
  );
  const dispatch = useDispatch<Dispatch>();

  const max = 500;
  const min = 180;

  const {
    sensor1,
    sensor2,
    sensor3,
    sensor4,
    sensor5,
    sensor6,
    sensor7,
    sensor8,
  } = moisture;

  let sensors = [
    sensor1,
    sensor2,
    sensor3,
    sensor4,
    sensor5,
    sensor6,
    sensor7,
    sensor8,
  ];

  return (
    <Card
      sx={{
        padding: theme.spacing(3),
        display: "block",
        width: "100%",
      }}
    >
      <Grid
        container
        spacing={3}
        wrap="nowrap"
        justifyContent="space-between"
        alignItems="center"
        sx={{
          marginBottom: theme.spacing(3),
        }}
      >
        <Grid item xs={6}>
          <Typography variant="h6" sx={{ marginBottom: theme.spacing(1) }}>
            Moisture Sensor Readings
          </Typography>
        </Grid>
        <Grid item xs={6}>
          <Grid
            container
            justifyContent="space-between"
            wrap="nowrap"
            sx={{ mb: theme.spacing(1) }}
          >
            <Grid item>
              <Typography variant="body2">Dry</Typography>
            </Grid>
            <Grid item>
              <Typography variant="body2">Wet</Typography>
            </Grid>
          </Grid>
          <Box
            sx={{
              height: theme.spacing(2),
              background:
                "linear-gradient(90deg, rgba(106,62,55,1) 0%, rgba(57,147,221,1) 100%)",
            }}
          />
        </Grid>
      </Grid>
      <Grid container spacing={1}>
        <Grid item xs={12}>
          <Box
            sx={{
              display: "flex",
              flexFlow: "row wrap",
              justifyContent: "space-between",
            }}
          >
            {range(4).map((index) => (
              <Box
                key={index}
                sx={{
                  padding: theme.spacing(1),
                }}
              >
                <Box
                  sx={{
                    borderRadius: "100%",
                    width: "32px",
                    height: "32px",
                    backgroundColor: mix(
                      "#6A3E37",
                      "#3993DD",
                      ((sensors[index] - min) / (max - min)) * 100
                    ).toHexString(),
                  }}
                ></Box>
              </Box>
            ))}
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Box
            sx={{
              display: "flex",
              flexFlow: "row wrap",
              justifyContent: "space-between",
            }}
          >
            {range(4, 8).map((index) => {
              let moisturePercent =
                ((sensors[index] - min) / (max - min)) * 100;
              if (moisturePercent > 100) {
                moisturePercent = 100;
              }
              if (moisturePercent < 0) {
                moisturePercent = 0;
              }
              return (
                <Box
                  key={index}
                  sx={{
                    padding: theme.spacing(1),
                  }}
                >
                  <Box
                    sx={{
                      borderRadius: "100%",
                      width: "32px",
                      height: "32px",
                      backgroundColor: mix("#6A3E37", "#3993DD").toHexString(),
                    }}
                  ></Box>
                </Box>
              );
            })}
          </Box>
        </Grid>
      </Grid>
    </Card>
  );
}

export default MoistureSensors;
