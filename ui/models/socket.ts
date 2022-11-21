export const message = {
  system: "monitor",
  type: "water_level",
  data: {
    distance: 3,
  },
};

export class Socket {
  private socket?: WebSocket;
  constructor(private port: number = 5000) {}
  async onMessage(message: any) {
    console.log(message);
  }
  async connect() {
    if (typeof window !== "undefined") {
      this.socket = new WebSocket(`ws://localhost:${this.port}`);
      await new Promise((resolve) =>
        this.socket?.addEventListener("open", resolve)
      );
      this.socket?.addEventListener("message", this.onMessage);
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
        this.connect();
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
