import { Card, Grid, Theme, Typography, useTheme } from "@mui/material";
import { Box } from "@mui/system";
import { range } from "lodash";
import React from "react";
import { Subscription } from "rxjs";
import { Dispatch, RootState, store } from "../models/store";
import { calcColor } from "../util/color";
import { useSelector, useDispatch } from "react-redux";

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

  const sensors = [
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
      <Typography variant="h6" sx={{ marginBottom: theme.spacing(1) }}>
        Moisture Sensor Readings
      </Typography>
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
                  padding: theme.spacing(3),
                }}
              >
                <Box
                  sx={{
                    borderRadius: "100%",
                    width: "32px",
                    height: "32px",
                    backgroundColor: calcColor(min, max, sensors[index]),
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
            {range(4, 8).map((index) => (
              // </Grid>
              <Box
                key={index}
                sx={{
                  padding: theme.spacing(3),
                }}
              >
                <Box
                  sx={{
                    borderRadius: "100%",
                    width: "32px",
                    height: "32px",
                    backgroundColor: calcColor(min, max, sensors[index]),
                  }}
                ></Box>
              </Box>
            ))}
          </Box>
        </Grid>
      </Grid>
    </Card>
  );
}

export default MoistureSensors;
