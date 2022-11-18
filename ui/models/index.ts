import { Models } from "@rematch/core";
import { light } from "./light";
import { moisture } from "./moisture";
import { photos } from "./photos";
import { temperature } from "./temperature";
import { waterLevel } from "./waterLevel";

export interface RootModel extends Models<RootModel> {
  moisture: typeof moisture;
  photos: typeof photos;
  waterLevel: typeof waterLevel;
  light: typeof light;
  temperature: typeof temperature;
}

export const models: RootModel = {
  moisture,
  photos,
  light,
  temperature,
  waterLevel,
};
