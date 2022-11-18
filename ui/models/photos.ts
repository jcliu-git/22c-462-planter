import { createModel } from "@rematch/core";
import { uniqBy, uniqWith } from "lodash";
import { RootModel } from ".";
import { api } from "./api";

export interface photoData {
  filepath: string;
  timestamp: string;
  width: number;
  height: number;
}

export const photos = createModel<RootModel>()({
  state: [] as photoData[], // initial state
  reducers: {
    // handle state changes with pure functions
    add(state, payload: photoData[]) {
      return uniqWith(
        [...state, ...payload],
        (a, b) => a.filepath == b.filepath
      );
    },
  },
  effects: (dispatch) => ({
    // handle state changes with impure functions.
    // use async/await for async actions
    async fetchLatestPhotos() {
      try {
        let photos = await api.photos.getLatestPhotos();
        dispatch.photos.add(photos);
      } catch (e) {
        console.log(e);
      }
    },
  }),
});
