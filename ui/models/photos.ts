import { createModel } from "@rematch/core";
import { RootModel } from ".";
import { api } from "./api";

export interface photoData {
  filepath: string;
  width: number;
  height: number;
}

export const photos = createModel<RootModel>()({
  state: [] as photoData[], // initial state
  reducers: {
    // handle state changes with pure functions
    add(state, payload: photoData[]) {
      return [...state, ...payload];
    },
  },
  effects: (dispatch) => ({
    // handle state changes with impure functions.
    // use async/await for async actions
    async fetchLatestPhotos() {
      let photos = await api.photos.getLatestPhotos();
      dispatch.photos.add(photos);
    },
  }),
});
