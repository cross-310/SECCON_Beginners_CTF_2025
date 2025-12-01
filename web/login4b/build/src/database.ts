import mysql from "mysql2/promise";
import bcrypt from "bcryptjs";
import { v4 as uuidv4 } from "uuid";

export interface User {
  userid: number;
  username: string;
  password_hash: string;
  reset_token: string | null;
}

class Database {
  private pool: mysql.Pool;
  private initialized: Promise<void>;

  constructor() {
    this.pool = mysql.createPool({
      host: process.env.DB_HOST || "localhost",
      port: parseInt(process.env.DB_PORT || "3306"),
      user: process.env.DB_USER || "root",
      password: process.env.DB_PASSWORD || "rootpassword",
      database: process.env.DB_NAME || "login4b",
      waitForConnections: true,
      connectionLimit: 10,
      queueLimit: 0,
    });
    this.initialized = this.init();
  }

  private async init() {
    try {
      await this.pool.execute(`
        CREATE TABLE IF NOT EXISTS users (
          userid INT AUTO_INCREMENT PRIMARY KEY,
          username VARCHAR(255) UNIQUE NOT NULL,
          password_hash VARCHAR(255) NOT NULL,
          reset_token VARCHAR(255)
        )
      `);

      // Check if admin user exists
      const [rows] = (await this.pool.execute(
        "SELECT COUNT(*) as count FROM users WHERE username = ?",
        ["admin"]
      )) as [any[], mysql.FieldPacket[]];

      if (rows[0].count === 0) {
        const adminHash = bcrypt.hashSync(
          process.env.ADMIN_PASSWORD || "admin_pass",
          10
        );
        await this.pool.execute(
          "INSERT INTO users (username, password_hash) VALUES (?, ?)",
          ["admin", adminHash]
        );
      }
    } catch (error) {
      console.error("Database initialization error:", error);
    }
  }

  async createUser(username: string, password: string): Promise<number> {
    await this.initialized;
    const hashedPassword = bcrypt.hashSync(password, 10);
    const [result] = (await this.pool.execute(
      "INSERT INTO users (username, password_hash) VALUES (?, ?)",
      [username, hashedPassword]
    )) as [mysql.ResultSetHeader, mysql.FieldPacket[]];
    return result.insertId;
  }

  async findUser(username: string): Promise<User | null> {
    await this.initialized;
    const [rows] = (await this.pool.execute(
      "SELECT * FROM users WHERE username = ?",
      [username]
    )) as [User[], mysql.FieldPacket[]];
    return rows[0] || null;
  }

  validatePassword(password: string, hash: string): boolean {
    return bcrypt.compareSync(password, hash);
  }

  async generateResetToken(userid: number): Promise<string> {
    await this.initialized;
    const timestamp = Math.floor(Date.now() / 1000);
    const token = `${timestamp}_${uuidv4()}`;

    await this.pool.execute(
      "UPDATE users SET reset_token = ? WHERE userid = ?",
      [token, userid]
    );
    return token;
  }

  async validateResetTokenByUsername(
    username: string,
    token: string
  ): Promise<boolean> {
    await this.initialized;
    const [rows] = (await this.pool.execute(
      "SELECT COUNT(*) as count FROM users WHERE username = ? AND reset_token = ?",
      [username, token]
    )) as [any[], mysql.FieldPacket[]];
    return rows[0].count > 0;
  }
}

export const db = new Database();
