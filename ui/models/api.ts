import { moistureData, photoData } from "./store";
import axios from "axios";

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
}
