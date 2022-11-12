import { createModel } from "@rematch/core";
import { RootModel } from ".";
import { api } from "./api";

export interface waterLevelData {
  timestamp: string;
  level: number;
}

export const waterLevel = createModel<RootModel>()({
  state: {
    timestamp: new Date().toISOString(),
    level: 0,
  } as waterLevelData, // initial state
  reducers: {
    // handle state changes with pure functions
    replace(state, payload: waterLevelData) {
      return payload;
    },
  },
  effects: (dispatch) => ({
    // handle state changes with impure functions.
    // use async/await for async actions
    async fetchLatestWaterLevelLevels() {
      let levels = await api.waterLevel.getLatestWaterLevel();
      dispatch.waterLevel.replace(levels);
    },
  }),
});
