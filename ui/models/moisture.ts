import { createModel } from "@rematch/core";
import { RootModel } from ".";
import { api } from "./api";

export interface moistureData {
  timestamp: string;
  sensor_1: number;
  sensor_2: number;
  sensor_3: number;
  sensor_4: number;
  sensor_5: number;
  sensor_6: number;
  sensor_7: number;
  sensor_8: number;
}

export const moisture = createModel<RootModel>()({
  state: {
    timestamp: new Date().toISOString(),
    sensor_1: 0,
    sensor_2: 0,
    sensor_3: 0,
    sensor_4: 0,
    sensor_5: 0,
    sensor_6: 0,
    sensor_7: 0,
    sensor_8: 0,
  } as moistureData, // initial state
  reducers: {
    // handle state changes with pure functions
    replace(state, payload: moistureData) {
      return payload;
    },
  },
  effects: (dispatch) => ({
    // handle state changes with impure functions.
    // use async/await for async actions
    async fetchLatestMoistureLevels() {
      let levels = await api.moisture.getLatestMoistureLevels();
      dispatch.replace(levels);
    },
  }),
});
