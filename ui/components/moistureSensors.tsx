import { Grid, Theme, useTheme } from "@mui/material";
import { Box } from "@mui/system";
import { range } from "lodash";
import React from "react";
import { Subscription } from "rxjs";
import { moistureData, store } from "../models/store";
import { calcColor } from "../util/color";

let moistureDataSubscription: Subscription | null = null;

function adjustNormalizedSensorValue(
  max: number,
  min: number,
  value: number
): number {
  return (max - min) * value + min;
}

export function MoistureSensors(): JSX.Element {
  const theme = useTheme<Theme>();
  const [moisture, setMoisture] = React.useState(store.moistureData.value);

  React.useEffect(() => {
    if (!moistureDataSubscription) {
      moistureDataSubscription = store.moistureData.subscribe((data) => {
        setMoisture(data);
      });
    }
  });

  const max = 500;
  const min = 180;

  const {
    sensor_1,
    sensor_2,
    sensor_3,
    sensor_4,
    sensor_5,
    sensor_6,
    sensor_7,
    sensor_8,
  } = moisture;

  const sensors = [
    sensor_1,
    sensor_2,
    sensor_3,
    sensor_4,
    sensor_5,
    sensor_6,
    sensor_7,
    sensor_8,
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
