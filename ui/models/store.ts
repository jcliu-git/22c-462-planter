import {
  createModel,
  init,
  RematchDispatch,
  RematchRootState,
} from "@rematch/core";
import { Models } from "@rematch/core";
import _, { last, once, range, uniq } from "lodash";
import { useEffect } from "react";
import { api } from "./api";
import { socket } from "./socket";

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
      luminosity: 10000,
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
      sensor1: Math.random() * (500 - 100) + 100,
      sensor2: Math.random() * (500 - 100) + 100,
      sensor3: Math.random() * (500 - 100) + 100,
      sensor4: Math.random() * (500 - 100) + 100,
      sensor5: Math.random() * (500 - 100) + 100,
      sensor6: Math.random() * (500 - 100) + 100,
      sensor7: Math.random() * (500 - 100) + 100,
      sensor8: Math.random() * (500 - 100) + 100,
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

export interface IPhotoGalleryState {
  photos: {
    timelapse: IPhotoData[];
    visitors: IPhotoData[];
  };
}

export const photoGalleryState = createModel<RootModel>()({
  state: {
    photos: {
      timelapse: [],
      visitors: [],
    },
  } as IPhotoGalleryState,
  reducers: {
    replace(state, payload: IPhotoGalleryState) {
      return payload;
    },
  },
  effects: (dispatch) => ({
    async fetch() {
      let [timelapse, visitors] = await Promise.all([
        api.camera.timelapseUrls(),
        api.camera.visitorUrls(),
      ]);

      const state = store.getState();

      dispatch.gallery.replace({
        photos: {
          timelapse: _.chain(state.gallery.photos.timelapse)
            .concat(timelapse)
            .uniqBy((p) => p.timestamp)
            .sortBy((p) => p.timestamp)
            .value(),
          visitors: _.chain(state.gallery.photos.visitors)
            .concat(visitors)
            .uniqBy((p) => p.timestamp)
            .sortBy((p) => p.timestamp)
            .value(),
        },
      });
    },
  }),
});

export interface ITemperatureData {
  timestamp: string;
  fahrenheit: number;
}

export function TemperatureData(data?: ITemperatureData): ITemperatureData {
  return (
    data || {
      timestamp: new Date().toISOString(),
      fahrenheit: 95,
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
      distance: 5,
    }
  );
}

export interface WaterConsumptionByDay {
  //date : litres consumed on that day
  date: string;
  litres: number;
}

export interface IDashboardState {
  light: ILightData;
  moisture: IMoistureData;
  photos: IPhotoData[];
  temperature: ITemperatureData;
  waterLevel: IWaterLevelData;
}

export interface SystemPulse {
  timestamp: string;
  averageMoisture: number;
  light: number;
  temperature: number;
  waterLevel: number;
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
      resevoirHeight: 20,
      emptyResevoirHeight: 20,
      fullResevoirHeight: 0,
    }
  );
}

export interface IAnalyticsState {
  waterConsumptionByDay: WaterConsumptionByDay[];
  systemPulse: SystemPulse[];
}

export function AnalyticsState(data?: IAnalyticsState): IAnalyticsState {
  return (
    data || {
      waterConsumptionByDay: [
        { date: "19", litres: 194 },
        { date: "20", litres: 237 },
        { date: "21", litres: 317 },
        { date: "22", litres: 169 },
        { date: "23", litres: 120 },
        { date: "24", litres: 413 },
        { date: "25", litres: 195 },
        { date: "26", litres: 0 },
      ],
      systemPulse: range(60).map((_) => {
        return {
          timestamp: new Date().toISOString(),
          averageMoisture: Math.round(Math.random() * 100),
          light: Math.round(Math.random() * 100),
          temperature: Math.round(Math.random() * 100),
          waterLevel: Math.round(Math.random() * 100),
        };
      }),
    }
  );
}

export const analyticsState = createModel<RootModel>()({
  state: AnalyticsState(),
  reducers: {
    replace(state, payload: IAnalyticsState) {
      return payload;
    },
  },
  effects: (dispatch) => ({
    async fetch() {
      let analytics = await api.analytics.fetch();
      dispatch.analytics.replace(analytics);
    },
  }),
});

export const hubState = createModel<RootModel>()({
  state: {
    control: ControlState(),
    dashboard: DashboardState(),
    websocketConnected: false,
  } as IHubState,
  reducers: {
    replace(state, payload: IHubState) {
      return payload;
    },
    togglePlanter(state) {
      let newState: IHubState = {
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
      let newState: IHubState = {
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
      let newState: IHubState = {
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
      let newState: IHubState = {
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

      let empty: number = state.control.calibrating
        ? state.control.emptyResevoirHeight
        : currentHeight;
      let full = state.control.calibrating
        ? currentHeight
        : state.control.fullResevoirHeight;

      let height = state.control.calibrating
        ? empty - full
        : state.control.resevoirHeight;

      let newState: IHubState = {
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
    websocketConnected(state) {
      return {
        ...state,
        websocketConnected: true,
      };
    },
    websocketDisconnected(state) {
      return {
        ...state,
        websocketConnected: false,
      };
    },
  },
  effects: (dispatch) => ({
    async fetch() {
      try {
        // only fetch if we are not connected to the websocket
        const state = store.getState();
        if (state.hub.websocketConnected) {
          return;
        }
        let data = await api.hub.fetch();
        data.dashboard.photos = state.hub.dashboard.photos;
        dispatch.hub.replace(data);
      } catch (e) {
        console.log(e);
      }
    },
  }),
});

export interface RootModel extends Models<RootModel> {
  drawer: typeof drawerState;
  hub: typeof hubState;
  gallery: typeof photoGalleryState;
  analytics: typeof analyticsState;
}

export const models: RootModel = {
  drawer: drawerState,
  hub: hubState,
  gallery: photoGalleryState,
  analytics: analyticsState,
};

export interface IHubState {
  dashboard: IDashboardState;
  control: IControlState;
  // this is only true for the local hub
  // using this to determine whether to show the
  // control panel
  websocketConnected: boolean;
}

export const store = init({
  models,
});

export const initStore = once(async function () {
  if (typeof window !== "undefined") {
    try {
      await Promise.all([
        store.dispatch.gallery.fetch(),
        store.dispatch.analytics.fetch(),
        store.dispatch.hub.fetch(),
      ]);
    } catch (e) {
      console.error(e);
    }
    setInterval(() => {
      try {
        store.dispatch.gallery.fetch();
        store.dispatch.analytics.fetch();
        if (!store.getState().hub.websocketConnected) {
          store.dispatch.hub.fetch();
        }
      } catch (e) {
        console.error(e);
      }
    }, 5 * 60 * 1000);
  }
});

export type Store = typeof store;
export type Dispatch = RematchDispatch<RootModel>;
export type RootState = RematchRootState<RootModel>;
