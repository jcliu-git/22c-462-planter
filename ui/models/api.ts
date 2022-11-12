import axios from "axios";
import { temperatureData } from "./temperature";
import { waterLevelData } from "./waterLevel";
import { lightData } from "./light";
import { moistureData } from "./moisture";
import { photoData } from "./photos";

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
      let resp = await axios<waterLevelData>("/api/water-level/latest");
      return resp.data;
    }
  }
  export namespace temperature {
    export async function getLatestTemperature(): Promise<temperatureData> {
      let resp = await axios<temperatureData>("/api/temperature/latest");
      return resp.data;
    }
  }
  export namespace light {
    export async function getLatestLuminosity(): Promise<lightData> {
      let resp = await axios<lightData>("/api/light/latest");
      return resp.data;
    }
  }
}
