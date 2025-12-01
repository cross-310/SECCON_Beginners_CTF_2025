import express, { Request, Response } from "express";
import session from "express-session";
import path from "path";
import { db } from "./database";

declare module "express-session" {
  interface SessionData {
    userId?: number;
    username?: string;
  }
}

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "../public")));

app.use(
  session({
    secret:
      process.env.SESSION_SECRET || "your-secret-key-change-in-production",
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false, maxAge: 24 * 60 * 60 * 1000 },
  })
);

app.post("/api/register", async (req: Request, res: Response) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) {
      return res.status(400).json({ error: "Username and password required" });
    }

    const existingUser = await db.findUser(username);
    if (existingUser) {
      return res.status(400).json({ error: "Username already exists" });
    }

    const userId = await db.createUser(username, password);
    req.session.userId = userId;
    req.session.username = username;

    res.json({ success: true, message: "Registration successful" });
  } catch (error) {
    res.status(500).json({ error: "Registration failed" });
  }
});

app.post("/api/login", async (req: Request, res: Response) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) {
      return res.status(400).json({ error: "Username and password required" });
    }

    const user = await db.findUser(username);
    if (!user || !db.validatePassword(password, user.password_hash)) {
      return res.status(401).json({ error: "Invalid credentials" });
    }

    req.session.userId = user.userid;
    req.session.username = user.username;

    res.json({ success: true, message: "Login successful" });
  } catch (error) {
    res.status(500).json({ error: "Login failed" });
  }
});

app.post("/api/logout", (req: Request, res: Response) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({ error: "Logout failed" });
    }
    res.json({ success: true, message: "Logout successful" });
  });
});

app.post("/api/reset-request", async (req: Request, res: Response) => {
  try {
    const { username } = req.body;

    if (!username) {
      return res.status(400).json({ error: "Username is required" });
    }

    const user = await db.findUser(username);
    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    await db.generateResetToken(user.userid);

    // TODO: send email to admin
    res.json({
      success: true,
      message:
        "Reset token has been generated. Please contact the administrator for the token.",
    });
  } catch (error) {
    console.error("Error generating reset token:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/api/reset-password", async (req: Request, res: Response) => {
  try {
    const { username, token, newPassword } = req.body;
    if (!username || !token || !newPassword) {
      return res
        .status(400)
        .json({ error: "Username, token, and new password are required" });
    }

    const isValid = await db.validateResetTokenByUsername(username, token);

    if (!isValid) {
      return res.status(400).json({ error: "Invalid token" });
    }

    // TODO: implement
    // await db.updatePasswordByUsername(username, newPassword);

    // TODO: remove this
    const user = await db.findUser(username);
    if (!user) {
      return res.status(401).json({ error: "Invalid username" });
    }
    req.session.userId = user.userid;
    req.session.username = user.username;

    res.json({
      success: true,
      message: `The function to update the password is not implemented, so I will set you the ${user.username}'s session`,
    });
  } catch (error) {
    console.error("Password reset error:", error);
    res.status(500).json({ error: "Reset failed" });
  }
});

app.get("/api/get_flag", (req: Request, res: Response) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: "Not authenticated" });
  }

  if (req.session.username === "admin") {
    res.json({ flag: process.env.FLAG || "ctf4B{**REDACTED**}" });
  } else {
    res.json({ message: "Hello user! Only admin can see the flag." });
  }
});

app.get("/api/status", (req: Request, res: Response) => {
  if (req.session.userId) {
    res.json({
      authenticated: true,
      username: req.session.username,
      isAdmin: req.session.username === "admin",
    });
  } else {
    res.json({ authenticated: false });
  }
});

app.get("*", (req: Request, res: Response) => {
  res.sendFile(path.join(__dirname, "../public/index.html"));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
