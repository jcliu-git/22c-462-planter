import { Client, Pool } from "pg";


class Database extends Pool {
  connected: boolean = false;
  constructor() {
    super({
      connectionString: process.env.DATABASE_URL,
      ssl: {
        rejectUnauthorized: false,
      },
    });
  }
}

export const database = new Database();

export default database;
