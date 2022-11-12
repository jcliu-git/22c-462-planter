import { BehaviorSubject } from "rxjs";
import { api } from "./api";

export interface moistureData {
  timestamp: string;
  sensor_1: number;
  sensor_2: number;
  sensor_3: number;
  sensor_4: number;
  sensor_5: number;
  sensor_6: number;
  sensor_7: number;
  sensor_8: number;
}

export interface photoData {
  filepath: string;
  width: number;
  height: number;
}

export function randomSensorData() {
  return {
    timestamp: new Date().toISOString(),
    sensor_1: Math.random() * 320 + 180,
    sensor_2: Math.random() * 320 + 180,
    sensor_3: Math.random() * 320 + 180,
    sensor_4: Math.random() * 320 + 180,
    sensor_5: Math.random() * 320 + 180,
    sensor_6: Math.random() * 320 + 180,
    sensor_7: Math.random() * 320 + 180,
    sensor_8: Math.random() * 320 + 180,
  };
}

class Store {
  moistureData = new BehaviorSubject<moistureData>({
    timestamp: new Date().toISOString(),
    sensor_1: 0,
    sensor_2: 0,
    sensor_3: 0,
    sensor_4: 0,
    sensor_5: 0,
    sensor_6: 0,
    sensor_7: 0,
    sensor_8: 0,
  });
  photoData = new BehaviorSubject<photoData[]>([]);
}

setInterval(() => {
  api.moisture.getLatestMoistureLevels().then((data) => {
    store.moistureData.next(data);
  });
}, 100000);

export const store = new Store();
