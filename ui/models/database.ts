import { Client, Pool } from "pg";

class Database extends Pool {
  connected: boolean = false;
  constructor() {
    super({
      host: "ec2-44-209-57-4.compute-1.amazonaws.com",
      database: "da41gg09sivbgs",
      user: "wzgfnyeewdbzlx",
      port: 5432,
      password:
        "68b169eefd466125c85c00c9bf7a28c2a4137ea409591093a62b680eb20af23e",
      ssl: {
        rejectUnauthorized: false,
      },
    });
  }
}

export const database = new Database();

export default database;
