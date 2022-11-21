import Axios from "axios";
import {
  DashboardState,
  IDashboardState,
  ILightData,
  IMoistureData,
  IPhotoData,
  ITemperatureData,
  IWaterLevelData,
  WaterConsumptionByDay,
  IControlState,
  HubState,
  IHubState,
} from "./store";

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
      await axios.post("/update", state);
    }
  }
}
