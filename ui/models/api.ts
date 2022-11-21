import Axios from "axios";
import { socket } from "./socket";
import { IHubState } from "./store";

const axios = Axios.create({
  baseURL: "http://127.0.0.1:5000",
});

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
}
