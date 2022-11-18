import { createModel } from "@rematch/core";
import { RootModel } from ".";
import { api } from "./api";

export interface lightData {
  timestamp: string;
  value: number;
}

export const light = createModel<RootModel>()({
  state: {
    timestamp: new Date().toISOString(),
    value: 0,
  } as lightData, // initial state
  reducers: {
    // handle state changes with pure functions
    replace(state, payload: lightData) {
      return payload;
    },
  },
  effects: (dispatch) => ({
    // handle state changes with impure functions.
    // use async/await for async actions
    async fetchLatestLight() {
      try {
        let light = await api.light.getLatestLuminosity();
        dispatch.light.replace(light);
      } catch (e) {
        console.log(e);
      }
    },
  }),
});
