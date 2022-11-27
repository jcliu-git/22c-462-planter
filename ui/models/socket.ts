import { max } from "lodash";
import { IHubState, store, Store } from "./store";

export class Socket {
  private socket?: WebSocket;
  private reconnectInterval?: ReturnType<typeof setInterval>;
  private port: number;
  constructor(port: number = 5000) {
    this.port = port;
    this.reconnectInterval = setInterval(() => this.connect(), 1000);
  }
  async onMessage(message: any) {
    const state: IHubState = JSON.parse(message.data);
    state.websocketConnected = true;
    store.dispatch.hub.replace(state);
  }
  async connect(retryTimeout = 1000) {
    if (typeof window !== "undefined") {
      try {
        this.socket = new WebSocket(`ws://localhost:${this.port}`);

        await new Promise((resolve) =>
          this.socket?.addEventListener("open", resolve)
        );

        console.log("websocket connected");
        clearInterval(this.reconnectInterval);
        store.dispatch.hub.websocketConnected();

        this.socket?.addEventListener("message", this.onMessage);
        this.socket?.addEventListener("error", (e) => {
          console.log(e);
          this.socket = undefined;
          clearInterval(this.reconnectInterval);
          this.reconnectInterval = setInterval(() => this.connect(), 1000);
          store.dispatch.hub.websocketDisconnected();
        });
        this.socket?.addEventListener("close", (e) => {
          console.log(e);
          this.socket = undefined;
          clearInterval(this.reconnectInterval);
          this.reconnectInterval = setInterval(() => this.connect(), 1000);
          store.dispatch.hub.websocketDisconnected();
        });
      } catch (e) {}
    }
  }
  async waitForConnection() {
    if (this.socket?.readyState === 1) {
      return;
    } else {
      await new Promise((resolve) => setTimeout(resolve, 1000));

      await this.waitForConnection();
    }
  }
  async send(message: any) {
    if (typeof window !== "undefined") {
      if (!this.socket) {
        return;
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
}

export const socket = new Socket();
