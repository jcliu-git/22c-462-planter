import {
  createModel,
  init,
  RematchDispatch,
  RematchRootState,
} from "@rematch/core";
import { Models } from "@rematch/core";
import { api } from "./api";

interface DrawerState {
  open: boolean;
}

function DrawerState(open?: boolean): DrawerState {
  return {
    open: open || false,
  };
}

export const drawerState = createModel<RootModel>()({
  state: DrawerState(),
  reducers: {
    toggle(state) {
      return {
        ...state,
        open: !state.open,
      };
    },
    open(state) {
      return {
        ...state,
        open: true,
      };
    },
    close(state) {
      return {
        ...state,
        open: false,
      };
    },
  },
  effects: (dispatch) => ({}),
});

export interface ILightData {
  timestamp: string;
  luminosity: number;
}

export function LightData(data?: ILightData): ILightData {
  return (
    data || {
      timestamp: new Date().toISOString(),
      luminosity: 0,
    }
  );
}

export interface IMoistureData {
  timestamp: string;
  sensor1: number;
  sensor2: number;
  sensor3: number;
  sensor4: number;
  sensor5: number;
  sensor6: number;
  sensor7: number;
  sensor8: number;
}

export function MoistureData(data?: IMoistureData): IMoistureData {
  return (
    data || {
      timestamp: new Date().toISOString(),
      sensor1: 0,
      sensor2: 0,
      sensor3: 0,
      sensor4: 0,
      sensor5: 0,
      sensor6: 0,
      sensor7: 0,
      sensor8: 0,
    }
  );
}

export interface IPhotoData {
  filepath: string;
  timestamp: string;
  width: number;
  height: number;
}

export function PhotoData(data?: IPhotoData): IPhotoData {
  return (
    data || {
      filepath: "",
      timestamp: new Date().toISOString(),
      width: 0,
      height: 0,
    }
  );
}

export interface ITemperatureData {
  timestamp: string;
  temperature: number;
}

export function TemperatureData(data?: ITemperatureData): ITemperatureData {
  return (
    data || {
      timestamp: new Date().toISOString(),
      temperature: 0,
    }
  );
}

export interface IWaterLevelData {
  timestamp: string;
  distance: number;
}

export function WaterLevelData(data?: IWaterLevelData): IWaterLevelData {
  return (
    data || {
      timestamp: new Date().toISOString(),
      distance: 0,
    }
  );
}

export interface IDashboardState {
  light: ILightData;
  moisture: IMoistureData;
  photos: IPhotoData[];
  temperature: ITemperatureData;
  waterLevel: IWaterLevelData;
}

export function DashboardState(data?: IDashboardState): IDashboardState {
  return (
    data || {
      light: LightData(),
      moisture: MoistureData(),
      photos: [],
      temperature: TemperatureData(),
      waterLevel: WaterLevelData(),
    }
  );
}

export const dashboardState = createModel<RootModel>()({
  state: DashboardState(),
  reducers: {
    replace(state, payload: any) {
      return payload;
    },
  },
  effects: (dispatch) => ({
    async fetchLatest() {
      try {
        let data = await api.dashboard.fetchLatest();
        dispatch.dashboard.replace(data);
      } catch (e) {
        console.log(e);
      }
    },
  }),
});

export interface IControlState {
  planterEnabled: boolean;
  hydroponicEnabled: boolean;
  dryThreshold: number;
  flowTime: number;
  calibrating: boolean;
  resevoirHeight: number;
  emptyResevoirHeight: number;
  fullResevoirHeight: number;
}

export function ControlState(data?: IControlState): IControlState {
  return (
    data || {
      planterEnabled: false,
      hydroponicEnabled: false,
      dryThreshold: 30,
      flowTime: 10,
      calibrating: false,
      resevoirHeight: 60,
      emptyResevoirHeight: 60,
      fullResevoirHeight: 0,
    }
  );
}

export const controlState = createModel<RootModel>()({
  state: ControlState(),
  reducers: {
    togglePlanter(state) {
      return {
        ...state,
        planterEnabled: !state.planterEnabled,
      };
    },
    toggleHydroponic(state) {
      return {
        ...state,
        hydroponicEnabled: !state.hydroponicEnabled,
      };
    },
    setDryThreshold(state, payload: number) {
      return {
        ...state,
        dryThreshold: payload,
      };
    },
    setFlowTime(state, payload: number) {
      return {
        ...state,
        flowTime: payload,
      };
    },
    toggleCalibration(state, currentHeight: number) {
      // when calibration starts, set the empty resevoir height

      return {
        ...state,
        emptyResevoirHeight: state.calibrating
          ? state.emptyResevoirHeight
          : currentHeight,
        fullResevoirHeight: state.calibrating
          ? currentHeight
          : state.fullResevoirHeight,
        calibrating: !state.calibrating,
      };
    },
  },
  effects: (dispatch) => ({}),
});

export interface ServerState {
  dashboard: IDashboardState,
  control: IControlState
}

export interface RootModel extends Models<RootModel> {
  dashboard: typeof dashboardState;
  drawer: typeof drawerState;
  control: typeof controlState;
}

export const models: RootModel = {
  dashboard: dashboardState,
  drawer: drawerState,
  control: controlState,
};

export const store = init({
  models,
});

export type Store = typeof store;
export type Dispatch = RematchDispatch<RootModel>;
export type RootState = RematchRootState<RootModel>;
