import axios from "axios";
import { result } from "lodash";
import { socket } from "./socket";
import { IAnalyticsState, IHubState, IPhotoData } from "./store";

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
      let [waterLevel, moisture, light, temperature] = await Promise.all([
        axios.get("/api/hub/waterLevel"),
        axios.get("/api/hub/moisture"),
        axios.get("/api/hub/light"),
        axios.get("/api/hub/temperature"),
      ]).then((results) => results.map((r) => r.data));

      return {
        dashboard: {
          waterLevel,
          moisture,
          light,
          temperature,
          photos: [],
        },
        control: {
          planterEnabled: false,
          hydroponicEnabled: false,
          dryThreshold: 0,
          flowTime: 0,
          calibrating: false,
          resevoirHeight: 0,
          emptyResevoirHeight: 0,
          fullResevoirHeight: 0,
        },
        websocketConnected: false,
      };
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
    export async function timelapseUrls(): Promise<IPhotoData[]> {
      let result = await axios.get("/api/photos/timelapse");
      return result.data;
    }
    export async function visitorUrls(): Promise<IPhotoData[]> {
      let result = await axios.get("/api/photos/visitors");
      return result.data;
    }
  }
  export namespace analytics {
    export async function fetch(): Promise<IAnalyticsState> {
      let result = await axios.get("/api/analytics");
      return result.data;
    }
  }
}
