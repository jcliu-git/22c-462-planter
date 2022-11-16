export class Scheduler {
  intervalId: number | undefined;
  routines: (() => void)[] = [];
  constructor(public updateInterval: number = 1000) {}
  addRoutines(...routines: (() => void)[]) {
    for (let routine of routines) {
      // if (this.routines.includes(routine)) {
      //   continue;
      // }
      this.routines.push(routine);
    }
  }
  tick() {
    this.routines.forEach((handler) => {
      try {
        handler();
      } catch (e) {
        console.error(e);
      }
    });
  }
  stop() {
    if (typeof this.intervalId !== "undefined") {
      clearInterval(this.intervalId);
      this.intervalId = undefined;
    }
  }
  start() {
    if (typeof window === "undefined") {
      return;
    }
    this.stop();
    this.tick();
    this.intervalId = window.setInterval(
      this.tick.bind(this),
      this.updateInterval
    );
  }
  clearRoutines() {
    this.routines = [];
  }
}
