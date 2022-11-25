import axios from "axios";
import { socket } from "./socket";
import { IHubState, IPhotoData } from "./store";

export namespace api {
  export namespace hub {
    export async function fetch(): Promise<IHubState> {
      let result = await axios.get("/fetch");
      return result.data;
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
}
