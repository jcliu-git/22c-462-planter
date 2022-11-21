import { Client, Pool } from "pg";

class Database extends Pool {
  connected: boolean = false;
  constructor() {
    super({
      host: "db",
      database: "garden",
      user: "postgres",
      port: 5432,
      password: "postgres",
      // ssl: {
      //   rejectUnauthorized: false,
      // },
    });
  }
}

export const database = new Database();

export default database;
