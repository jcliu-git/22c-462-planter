import { useTheme } from "@mui/material";
import React from "react";
import { useSelector } from "react-redux";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import { RootState } from "../models/store";
import { NonSSRWrapper } from "../util/next";
import useSWR from "swr";

export function WaterConsumption(): JSX.Element {
  const theme = useTheme();
  const state = useSelector(
    (state: RootState) => state.dashboard.waterConsumptionByDay
  );

  const data = [
    {
      name: "6 days ago",
      litres: state[0] || 0,
    },
    {
      name: "5 days ago",
      litres: state[1] || 0,
    },
    {
      name: "4 days ago",
      litres: state[2] || 0,
    },
    {
      name: "3 days ago",
      litres: state[3] || 0,
    },
    {
      name: "2 days ago",
      litres: state[4] || 0,
    },
    {
      name: "1 days ago",
      litres: state[5] || 0,
    },
    {
      name: "today",
      litres: state[6] || 0,
    },
  ];

  return (
    <BarChart width={730} height={250} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" color="red" label={{ fill: "white" }} />
      <Bar dataKey="litres" fill="#8884d8" />
    </BarChart>
  );
}
