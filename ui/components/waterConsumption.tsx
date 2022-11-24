import { CustomTheme, Typography, useTheme } from "@mui/material";
import { Box } from "@mui/system";
import _ from "lodash";
import React from "react";
import { useSelector } from "react-redux";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Label,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";
import { RootState } from "../models/store";

interface waterConsumptionDatum {
  name: string;
  litres: number;
}

export function WaterConsumption(): JSX.Element {
  const theme = useTheme<CustomTheme>();
  const state = useSelector(
    (state: RootState) => state.hub.analytics.waterConsumptionByDay
  );

  const data = _.chain(state)
    .keys()
    .sort()
    .reduce((acc, key, index) => {
      acc.push({
        name: index == 6 ? "Today" : `${6 - index}`,
        litres: state[key],
      });
      return acc;
    }, [] as waterConsumptionDatum[])
    .value();

  return (
    <Box
      sx={{
        display: "flex",
        flexFlow: "column nowrap",
        alignItems: "center",
        justifyContent: "center",
        width: "100%",
        height: "100%",
      }}
    >
      <Typography>Water Consumption</Typography>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          margin={{
            top: 20,
            right: 20,
            bottom: 20,
            left: 20,
          }}
          data={data}
          title="Water Consumption"
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke={theme.palette.light.main}
          />
          <XAxis
            dataKey="name"
            tick={{ fill: theme.palette.light.main }}
            label={{
              value: "Days Ago",
              fill: theme.palette.light.main,
              position: "bottom",
            }}
          />
          <YAxis
            dataKey="litres"
            tick={{ fill: theme.palette.light.main }}
            label={{
              value: "Litres",
              fill: theme.palette.light.main,
              angle: -90,
              position: "insideLeft",
            }}
          />
          <Bar dataKey="litres" fill={theme.palette.secondary.main} />
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
}
