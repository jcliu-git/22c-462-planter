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
  baseURL: "http://localhost:3000",
});

export namespace api {
  export namespace hub {
    export async function fetch(): Promise<IHubState> {
      let result = await axios.get("/api/hub/fetch");
      return result.data;
    }

    export async function update(state: IHubState): Promise<void> {
      await axios.post("/api/hub/update", state);
    }
  }
  // export namespace control {
  //   export async function fetch(): Promise<IControlState> {
  //     let res = await axios<IControlState>("/api/control/fetch");
  //     return res.data;
  //   }
  //   export async function update(state: IControlState): Promise<boolean> {
  //     await axios.post("/api/control/update", state);
  //     return true;
  //   }
  // }

  // export namespace dashboard {
  //   export async function fetchLatest(): Promise<IDashboardState> {
  //     let data = DashboardState();
  //     await Promise.all([
  //       axios<ILightData>("/api/light/latest").then((res) => {
  //         data.light = res.data;
  //       }),
  //       axios<IMoistureData>("/api/moisture/latest").then((res) => {
  //         data.moisture = res.data;
  //       }),
  //       axios<ITemperatureData>("/api/temperature/latest").then((res) => {
  //         data.temperature = res.data;
  //       }),
  //       axios<IWaterLevelData>("/api/waterLevel/latest").then((res) => {
  //         data.waterLevel = res.data;
  //       }),
  //       axios<IPhotoData[]>("/api/photos/latest").then((res) => {
  //         data.photos = res.data;
  //       }),
  //       axios<WaterConsumptionByDay>("/api/waterLevel/sevenDays").then(
  //         (res) => {
  //           data.waterConsumptionByDay = res.data;
  //         }
  //       ),
  //     ]);

  //     return data;
  //   }
  //   export namespace waterLevel {
  //     export async function fetchLatest(): Promise<IWaterLevelData> {
  //       let res = await axios<IWaterLevelData>("/api/waterLevel/latest");
  //       return res.data;
  //     }
  //   }
  // }
}
