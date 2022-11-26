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
import { RootState, WaterConsumptionByDay } from "../models/store";

export function WaterConsumption(): JSX.Element {
  const theme = useTheme<CustomTheme>();
  const state = useSelector(
    (state: RootState) => state.analytics.waterConsumptionByDay
  );

  const today = new Date().getDate();

  const data = _.chain(state)
    .sort((a, b) => parseInt(a.date) - parseInt(b.date))
    .reduce((acc, datum) => {
      acc.push({
        date:
          parseInt(datum.date) == today
            ? "Today"
            : `${today - parseInt(datum.date)}`,
        litres: datum.litres,
      });
      return acc;
    }, [] as WaterConsumptionByDay[])
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
            dataKey="date"
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
