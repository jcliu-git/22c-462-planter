import { createContext } from "react";
import { Socket } from "./socket";

export interface ICleverGardenContext {
  socket: Socket;
}

export const CleverGardenContext = createContext({} as ICleverGardenContext);
