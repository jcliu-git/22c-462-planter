import { createModel } from "@rematch/core";
import { RootModel } from ".";
import { api } from "./api";

export interface moistureData {
  timestamp: string;
  sensor1: number;
  sensor2: number;
  sensor3: number;
  sensor4: number;
  sensor5: number;
  sensor6: number;
  sensor7: number;
  sensor8: number;
}

export const moisture = createModel<RootModel>()({
  state: {
    timestamp: new Date().toISOString(),
    sensor1: 0,
    sensor2: 0,
    sensor3: 0,
    sensor4: 0,
    sensor5: 0,
    sensor6: 0,
    sensor7: 0,
    sensor8: 0,
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
      dispatch.moisture.replace(levels);
    },
  }),
});
