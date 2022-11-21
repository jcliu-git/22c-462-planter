import { Store } from "./store";

export const message = {
  system: "monitor",
  type: "water_level",
  data: {
    distance: 3,
  },
};

export class Socket {
  private socket?: WebSocket;
  private reconnectInterval?: ReturnType<typeof setInterval>;
  private port: number;
  constructor(port: number = 5000) {
    this.port = port;
    this.reconnectInterval = setInterval(() => this.connect(), 1000);
  }
  async onMessage(message: any) {}
  async connect() {
    if (typeof window !== "undefined") {
      this.socket = new WebSocket(`ws://localhost:${this.port}`);

      await new Promise((resolve) =>
        this.socket?.addEventListener("open", resolve)
      );
      console.log("websocket connected");
      clearInterval(this.reconnectInterval);
      this.socket?.addEventListener("message", this.onMessage);
      this.socket?.addEventListener("error", (e) => {
        console.log(e);
        this.socket = undefined;
        this.onMessage = async (message) => {};
        clearInterval(this.reconnectInterval);
        this.reconnectInterval = setInterval(() => this.connect(), 1000);
      });
      this.socket?.addEventListener("close", (e) => {
        console.log(e);
        this.socket = undefined;
        this.onMessage = async (message) => {};
        clearInterval(this.reconnectInterval);
        this.reconnectInterval = setInterval(() => this.connect(), 1000);
      });
    }
  }
  async waitForConnection(interval = 1000) {
    if (this.socket?.readyState === 1) {
      return;
    } else {
      await new Promise((resolve) => setTimeout(resolve, 1000));

      await this.waitForConnection(interval * 2);
    }
  }
  async send(message: any) {
    if (typeof window !== "undefined") {
      if (!this.socket) {
        await this.connect();
      }
      if (this.socket) {
        try {
          await this.waitForConnection();
          this.socket.send(JSON.stringify(message));
        } catch (e) {
          console.log(e);
        }
      }
    }
  }
  bindToStore(store: Store) {
    this.onMessage = async (message) => {
      store.dispatch.hub.replace(JSON.parse(message.data));
    };
  }
}

export const socket = new Socket();
