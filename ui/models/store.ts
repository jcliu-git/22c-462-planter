import {
  createModel,
  init,
  RematchDispatch,
  RematchRootState,
} from "@rematch/core";
import { Models } from "@rematch/core";
import { uniq } from "lodash";
import { useEffect } from "react";
import { api } from "./api";
import { Socket } from "./socket";

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
  fahrenheit: number;
}

export function TemperatureData(data?: ITemperatureData): ITemperatureData {
  return (
    data || {
      timestamp: new Date().toISOString(),
      fahrenheit: 0,
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

export interface WaterConsumptionByDay {
  [key: string]: number;
}

export interface IDashboardState {
  light: ILightData;
  moisture: IMoistureData;
  photos: IPhotoData[];
  temperature: ITemperatureData;
  waterLevel: IWaterLevelData;
  waterConsumptionByDay: WaterConsumptionByDay;
}

export function DashboardState(data?: IDashboardState): IDashboardState {
  return (
    data || {
      light: LightData(),
      moisture: MoistureData(),
      photos: [],
      temperature: TemperatureData(),
      waterLevel: WaterLevelData(),
      waterConsumptionByDay: {},
    }
  );
}

// export const dashboardState = createModel<RootModel>()({
//   state: DashboardState(),
//   reducers: {
//     replace(state, payload: any) {
//       return payload;
//     },
//     setWaterLevel(state, payload: IWaterLevelData) {
//       return {
//         ...state,
//         waterLevel: payload,
//       };
//     },
//   },
//   effects: (dispatch) => ({
//     async fetchLatest() {
//       try {
//         let data = await api.dashboard.fetchLatest();
//         dispatch.dashboard.replace(data);
//       } catch (e) {
//         console.log(e);
//       }
//     },
//     async fetchWaterLevel() {
//       try {
//         let data = await api.dashboard.waterLevel.fetchLatest();
//         dispatch.dashboard.setWaterLevel(data);
//       } catch (e) {
//         console.log(e);
//       }
//     },
//   }),
// });

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
      resevoirHeight: 5000,
      emptyResevoirHeight: 5000,
      fullResevoirHeight: 0,
    }
  );
}

// export const controlState = createModel<RootModel>()({
//   state: ControlState(),
//   reducers: {
//     togglePlanter(state) {
//       let newState = {
//         ...state,
//         planterEnabled: !state.planterEnabled,
//       };
//       api.control.update(newState);
//       return newState;
//     },
//     toggleHydroponic(state) {
//       let newState = {
//         ...state,
//         hydroponicEnabled: !state.hydroponicEnabled,
//       };
//       api.control.update(newState);
//       return newState;
//     },
//     setDryThreshold(state, payload: number) {
//       let newState = {
//         ...state,
//         dryThreshold: payload,
//       };
//       api.control.update(newState);
//       return newState;
//     },
//     setFlowTime(state, payload: number) {
//       let newState = {
//         ...state,
//         flowTime: payload,
//       };
//       api.control.update(newState);
//       return newState;
//     },
//     toggleCalibration(state, currentHeight: number) {
//       // when calibration starts, set the empty resevoir height

//       let newState = {
//         ...state,
//         emptyResevoirHeight: state.calibrating
//           ? state.emptyResevoirHeight
//           : currentHeight,
//         fullResevoirHeight: state.calibrating
//           ? currentHeight
//           : state.fullResevoirHeight,
//         calibrating: !state.calibrating,
//       };
//       return newState;
//     },
//     replace(state, payload: any) {
//       if (typeof payload.calibrating == "undefined") {
//         payload.calibrating = state.calibrating;
//       }
//       return payload;
//     },
//   },
//   effects: (dispatch) => ({
//     async fetchLatest() {
//       try {
//         let data = await api.control.fetch();
//         let state = store.getState();
//         data.calibrating = state.control.calibrating;
//         dispatch.control.replace(data);
//       } catch (e) {
//         console.log(e);
//       }
//     },
//   }),
// });

export const hubState = createModel<RootModel>()({
  state: {
    control: ControlState(),
    dashboard: DashboardState(),
  } as IHubState,
  reducers: {
    replace(state, payload: IHubState) {
      return payload;
    },
    togglePlanter(state) {
      let newState = {
        ...state,
        control: {
          ...state.control,
          planterEnabled: !state.control.planterEnabled,
        },
      };
      api.hub.update(newState);
      return newState;
    },
    toggleHydroponic(state) {
      let newState = {
        ...state,
        control: {
          ...state.control,
          hydroponicEnabled: !state.control.hydroponicEnabled,
        },
      };
      api.hub.update(newState);
      return newState;
    },
    setDryThreshold(state, payload: number) {
      let newState = {
        ...state,
        control: {
          ...state.control,
          dryThreshold: payload,
        },
      };
      api.hub.update(newState);
      return newState;
    },
    setFlowTime(state, payload: number) {
      let newState = {
        ...state,
        control: {
          ...state.control,
          flowTime: payload,
        },
      };
      api.hub.update(newState);
      return newState;
    },
    toggleCalibration(state, currentHeight: number) {
      // when calibration starts, set the empty resevoir height

      let empty = state.control.calibrating
        ? state.control.emptyResevoirHeight
        : currentHeight;
      let full = state.control.calibrating
        ? currentHeight
        : state.control.fullResevoirHeight;

      let height = state.control.calibrating
        ? empty - full
        : state.control.resevoirHeight;

      let newState = {
        ...state,
        control: {
          ...state.control,
          emptyResevoirHeight: empty,
          fullResevoirHeight: full,
          resevoirHeight: height,
          calibrating: !state.control.calibrating,
        },
      };
      api.hub.update(newState);
      return newState;
    },
  },
  effects: (dispatch) => ({
    async fetch() {
      try {
        let data = await api.hub.fetch();
        dispatch.hub.replace(data);
      } catch (e) {
        console.log(e);
      }
    },
  }),
});

export interface RefetchRoutines {
  calibrating: number;
  hub: number;
  running: boolean;
  scheduled: RefetchRoutine[];
}

export enum RefetchRoutine {
  Calibrating = "calibrating",
  Hub = "hub",
}

export const refetchState = createModel<RootModel>()({
  state: {
    calibrating: 0,
    hub: 0,
    running: false,
    scheduled: [],
  } as RefetchRoutines,
  reducers: {
    subscribeHub(state, payload: number) {
      // 0 = no subscription

      return {
        ...state,
        hub: payload,
      };
    },

    schedule(state, payload: RefetchRoutine) {
      return {
        ...state,
        scheduled: uniq([...state.scheduled, payload]),
      };
    },
    unschedule(state, payload: RefetchRoutine) {
      return {
        ...state,
        scheduled: state.scheduled.filter((routine) => routine != payload),
      };
    },

    setRunning(state, payload: boolean) {
      return {
        ...state,
        running: payload,
      };
    },
  },
  effects: (dispatch) => ({
    tick() {
      let state = store.getState();

      if (
        state.refetch.hub &&
        !state.refetch.scheduled.includes(RefetchRoutine.Hub)
      ) {
        dispatch.hub.fetch();
        dispatch.refetch.schedule(RefetchRoutine.Hub);
        setTimeout(() => {
          dispatch.refetch.unschedule(RefetchRoutine.Hub);
        }, state.refetch.hub);
      }

      if (state.refetch.running) {
        setTimeout(dispatch.refetch.tick, 1000);
      }
    },
    start() {
      if (store.getState().refetch.running) {
        return;
      }
      dispatch.refetch.setRunning(true);
      dispatch.refetch.tick();
    },
    stop() {
      dispatch.refetch.setRunning(false);
    },
  }),
});

export interface RootModel extends Models<RootModel> {
  // dashboard: typeof dashboardState;
  drawer: typeof drawerState;
  hub: typeof hubState;
  // control: typeof controlState;
  refetch: typeof refetchState;
}

export const models: RootModel = {
  // dashboard: dashboardState,
  drawer: drawerState,
  hub: hubState,
  // control: controlState,
  refetch: refetchState,
};

export interface IHubState {
  dashboard: IDashboardState;
  control: IControlState;
}

export function HubState(): IHubState {
  return {
    dashboard: DashboardState(),
    control: ControlState(),
  };
}

export const store = init({
  models,
});

export const socket = new Socket();

if (typeof window !== "undefined") {
  socket.bindToStore(store);
  socket.connect();
}

export type Store = typeof store;
export type Dispatch = RematchDispatch<RootModel>;
export type RootState = RematchRootState<RootModel>;
