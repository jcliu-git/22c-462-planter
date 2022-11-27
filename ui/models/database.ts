import { Client, Pool } from "pg";

class Database extends Pool {
  connected: boolean = false;
  constructor(connectionString?: string) {
    super({
      connectionString,
      // ssl: {
      //   rejectUnauthorized: false,
      // },
    });
  }
}

export const database = new Database(process.env.AZURE_PG_URI);
