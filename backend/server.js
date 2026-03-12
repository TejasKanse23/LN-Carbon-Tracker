import express from "express";
import cors from "cors";
import dotenv from "dotenv";

import carbonRoutes from "./src/routes.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors({ origin: "*" }));
app.use(express.json());

// Routes
app.use("/api/carbon", carbonRoutes);

// Health Endpoint
app.get("/api/health", (req, res) => {
    res.json({ status: "ok", message: "Carbon Intelligence Engine Active" });
});

app.listen(PORT, () => {
    console.log(`✅ Carbon Intelligence Engine running on port ${PORT}`);
});
