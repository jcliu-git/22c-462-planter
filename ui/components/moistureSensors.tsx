import { Grid, Theme, useTheme } from "@mui/material";
import { Box } from "@mui/system";
import { range } from "lodash";
import React from "react";
import { Subscription } from "rxjs";
import { Dispatch, RootState, store } from "../models/store";
import { calcColor } from "../util/color";
import { useSelector, useDispatch } from "react-redux";

function adjustNormalizedSensorValue(
  max: number,
  min: number,
  value: number
): number {
  return (max - min) * value + min;
}

export function MoistureSensors(): JSX.Element {
  const theme = useTheme<Theme>();

  const moisture = useSelector((state: RootState) => state.moisture);
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
    <Box sx={{ display: "flex", width: "350px", flexFlow: "row wrap" }}>
      {range(8).map((index) => (
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
              backgroundColor: calcColor(
                min,
                max,
                adjustNormalizedSensorValue(max, min, sensors[index])
              ),
            }}
          ></Box>
        </Box>
      ))}
    </Box>
  );
}

export default MoistureSensors;
