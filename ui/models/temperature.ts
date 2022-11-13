import { createModel } from "@rematch/core";
import { RootModel } from ".";
import { api } from "./api";

export interface TemperatureData {
  timestamp: string;
  value: number;
}

export const temperature = createModel<RootModel>()({
  state: {
    timestamp: new Date().toISOString(),
    value: 0,
  } as TemperatureData, // initial state
  reducers: {
    // handle state changes with pure functions
    replace(state, payload: TemperatureData) {
      return payload;
    },
  },
  effects: (dispatch) => ({
    // handle state changes with impure functions.
    // use async/await for async actions
    async fetchLatestTemperature() {
      try {
        let temperature = await api.temperature.getLatestTemperature();
        dispatch.temperature.replace(temperature);
      } catch (e) {
        console.log(e);
      }
    },
  }),
});
