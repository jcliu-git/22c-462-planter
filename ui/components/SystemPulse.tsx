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
  let pulse = useSelector(
    (state: RootState) => state.hub.analytics.systemPulse
  );

  // pulse = pulse.map((p) => {
  //   p.timestamp = new Date(p.timestamp).toLocaleTimeString();
  //   return p;
  // });

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
        <XAxis dataKey="timestamp" display="none" />
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
                  dataKey="averageMoisture"
                  stroke={theme.palette.secondary.main}
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
                />
              );
            case SystemPulseType.Temperature:
              return (
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="temperature"
                  stroke="#ff6392"
                />
              );
            case SystemPulseType.WaterLevel:
              return (
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="waterLevel"
                  stroke={theme.palette.light.main}
                />
              );
          }
        })}
      </LineChart>
    </ResponsiveContainer>
  );
}
