import { createModel } from "@rematch/core";
import { RootModel } from ".";
import { api } from "./api";

export interface temperatureData {
  timestamp: string;
  celsius: number;
}

export const temperature = createModel<RootModel>()({
  state: {
    timestamp: new Date().toISOString(),
    celsius: 0,
  } as temperatureData, // initial state
  reducers: {
    // handle state changes with pure functions
    replace(state, payload: temperatureData) {
      return payload;
    },
  },
  effects: (dispatch) => ({
    // handle state changes with impure functions.
    // use async/await for async actions
    async fetchLatestPhotos() {
      let temperature = await api.temperature.getLatestTemperature();
      dispatch.temperature.replace(temperature);
    },
  }),
});
