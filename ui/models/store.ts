import { init, RematchDispatch, RematchRootState } from "@rematch/core";
import { models, RootModel } from ".";

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

export const store = init({
  models,
});

export type Store = typeof store;
export type Dispatch = RematchDispatch<RootModel>;
export type RootState = RematchRootState<RootModel>;
