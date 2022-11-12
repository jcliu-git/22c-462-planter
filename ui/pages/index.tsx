import { once } from "lodash";
import Head from "next/head";
import MoistureSensors from "../components/moistureSensors";
import Slideshow from "../components/slideshow";
import { WaterConsumption } from "../components/waterConsumption";
import { WaterLevel } from "../components/waterLevel";
import { Scheduler } from "../models/scheduler";
import { store } from "../models/store";
import styles from "../styles/Home.module.css";

let scheduler = new Scheduler();

scheduler.addRoutines(
  store.dispatch.waterLevel.fetchLatestWaterLevelLevels,
  store.dispatch.moisture.fetchLatestMoistureLevels,
  store.dispatch.waterLevel.fetchLatestWaterLevelLevels,
  store.dispatch.photos.fetchLatestPhotos
);

scheduler.start();

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Mobile Garden</title>
        <meta name="description" content="Mobile Garden" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <MoistureSensors />
      <WaterConsumption />
      <WaterLevel />
      <Slideshow />
    </div>
  );
}
