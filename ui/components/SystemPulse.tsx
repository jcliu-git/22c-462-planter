import { useTheme, CustomTheme, Box } from "@mui/material";
import { RootState } from "../models/store";
import { useSelector } from "react-redux";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export enum SystemPulseType {
  AverageMoisture = "averageMoisture",
  Light = "light",
  Temperature = "temperature",
  WaterLevel = "waterLevel",
}

export function SystemPulse({ types }: { types: SystemPulseType[] }) {
  const theme = useTheme<CustomTheme>();
  let pulse = useSelector((state: RootState) => state.analytics.systemPulse);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart
        data={pulse}
        width={500}
        height={300}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        {/* <CartesianGrid strokeDasharray="3 3" fill="#051923" stroke={theme.palette.light} /> */}
        <XAxis dataKey="hour" display="none" />
        {/* <YAxis yAxisId="left" />
        <YAxis yAxisId="right" orientation="right" /> */}
        <Tooltip
          contentStyle={{
            backgroundColor: theme.palette.dark.main,
          }}
        />
        <Legend fill="#051923" />
        {types.map((type) => {
          switch (type) {
            case SystemPulseType.AverageMoisture:
              return (
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="mositure"
                  stroke={theme.palette.secondary.main}
                  key="mositure"
                  activeDot={{ r: 8 }}
                />
              );
            case SystemPulseType.Light:
              return (
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="light"
                  stroke={theme.palette.primary.main}
                  key="light"
                />
              );
            case SystemPulseType.Temperature:
              return (
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="temperature"
                  stroke="#ff6392"
                  key="temperature"
                />
              );
            case SystemPulseType.WaterLevel:
              return (
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="waterLevel"
                  stroke={theme.palette.light.main}
                  key="waterLevel"
                />
              );
          }
        })}
      </LineChart>
    </ResponsiveContainer>
  );
}
