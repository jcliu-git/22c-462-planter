import { useTheme } from "@mui/material";
import React from "react";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import { NonSSRWrapper } from "../util/next";

const data = [
  {
    name: "monday",
    litres: 4000,
  },
  {
    name: "tuesday",
    litres: 6000,
  },
  {
    name: "wednesday",
    litres: 2000,
  },
  {
    name: "thursday",
    litres: 1000,
  },
  {
    name: "friday",
    litres: 500,
  },
];

export function WaterConsumption(): JSX.Element {
  const theme = useTheme();

  return (
    <NonSSRWrapper>
      <BarChart width={730} height={250} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" color="red" label={{ fill: "white" }} />
        <Bar dataKey="litres" fill="#8884d8" />
      </BarChart>
    </NonSSRWrapper>
  );
}
