import Axios from "axios";
import { TemperatureData } from "./temperature";
import { waterLevelData } from "./waterLevel";
import { lightData } from "./light";
import { moistureData } from "./moisture";
import { photoData } from "./photos";

const axios = Axios.create({
  baseURL: "http://localhost:3000",
});

export namespace api {
  export namespace moisture {
    export async function getLatestMoistureLevels(): Promise<moistureData> {
      let resp = await axios<moistureData>("/api/moisture/latest");
      return resp.data;
    }
  }
  export namespace photos {
    export async function getLatestPhotos(): Promise<photoData[]> {
      let resp = await axios<photoData[]>("/api/photos/latest");
      return resp.data;
    }
  }
  export namespace waterLevel {
    export async function getLatestWaterLevel(): Promise<waterLevelData> {
      let resp = await axios<waterLevelData>("/api/waterLevel/latest");
      return resp.data;
    }
  }
  export namespace temperature {
    export async function getLatestTemperature(): Promise<TemperatureData> {
      let resp = await axios<TemperatureData>("/api/weather/temperature");
      return resp.data;
    }
  }
  export namespace light {
    export async function getLatestLuminosity(): Promise<lightData> {
      let resp = await axios<lightData>("/api/weather/sunlight");
      return resp.data;
    }
  }
  export namespace waterLevelSevenDays {
    export async function getLatestWaterLevelSevenDay(): Promise<
      waterLevelData[]
    > {
      let resp = await axios<waterLevelData[]>("/api/water-level/sevenDays");
      return resp.data;
    }
  }
}
