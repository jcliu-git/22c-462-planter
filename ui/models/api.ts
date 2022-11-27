import axios from "axios";
import { result } from "lodash";
import { socket } from "./socket";
import {
  IAnalyticsState,
  IHubState,
  IPhotoData,
  IPhotoGalleryState,
  store,
} from "./store";

export namespace api {
  export namespace hub {
    export async function fetch(): Promise<IHubState> {
      // let waterLevel = await axios
      //   .get("/api/hub/waterLevel")
      //   .then((result) => result.data);
      // let moisture = await axios
      //   .get("/api/hub/moisture")
      //   .then((result) => result.data);
      // let light = await axios
      //   .get("/api/hub/light")
      //   .then((result) => result.data);
      // let temperature = await axios
      //   .get("/api/hub/temperature")
      //   .then((result) => result.data);
      // let [waterLevel, moisture, light, temperature] = await Promise.all([
      //   axios.get("/api/hub/waterLevel"),
      //   axios.get("/api/hub/moisture"),
      //   axios.get("/api/hub/light"),
      //   axios.get("/api/hub/temperature"),
      // ]).then((results) => results.map((r) => r.data));

      // return {
      //   dashboard: {
      //     waterLevel,
      //     moisture,
      //     light,
      //     temperature,
      //     photos: [],
      //   },
      //   control: {
      //     planterEnabled: false,
      //     hydroponicEnabled: false,
      //     dryThreshold: 0,
      //     flowTime: 0,
      //     calibrating: false,
      //     resevoirHeight: 0,
      //     emptyResevoirHeight: 0,
      //     fullResevoirHeight: 0,
      //   },
      //   websocketConnected: store.getState().hub.websocketConnected,
      // };

      let res = await axios.get(
        "https://clever-garden.azurewebsites.net/api/hub_state?code=u-RW45fXF6gyL4v3zbOTxGNNIMtoleyDx1gPMv7vYT5gAzFu8Lv5MA=="
      );
      return res.data;
    }

    export async function update(state: IHubState): Promise<void> {
      await socket.send({
        system: "ui",
        type: "hub_state",
        data: state,
        identifier: "data",
      });
    }
  }
  export namespace camera {
    // export async function timelapseUrls(): Promise<IPhotoData[]> {
    //   let result = await axios.get("/api/photos/timelapse");
    //   return result.data;
    // }
    // export async function visitorUrls(): Promise<IPhotoData[]> {
    //   let result = await axios.get("/api/photos/visitors");
    //   return result.data;
    // }
    export async function fetch(): Promise<{
      periodic: IPhotoData[];
      motion: IPhotoData[];
    }> {
      let res = await axios.get(
        "https://clever-garden.azurewebsites.net/api/photos?code=nPivhFyv0I7HOPfoViBuV4D9MMC4rFs0pOhHj6dSHwDyAzFubdeBcg=="
      );
      return res.data;
    }
  }
  export namespace analytics {
    export async function fetch(): Promise<IAnalyticsState> {
      // let result = await axios.get("/api/analytics");
      let result = await axios.get(
        "https://clever-garden.azurewebsites.net/api/analytics?code=uavf1Av2isp5x9xM_AU6TCO0xdvHsZYNbZ9tQRRYE27dAzFuvXG1Xg=="
      );
      return result.data;
    }
  }
}
