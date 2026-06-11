import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dirname = path.dirname(fileURLToPath(import.meta.url));
const sampleWorkspaceRoot = path.resolve(dirname, "../sample_workspace");

export default defineConfig({
  plugins: [
    react(),
    {
      name: "cg-varw-sample-workspace",
      configureServer(server) {
        server.middlewares.use("/sample_workspace", (req, res, next) => {
          const requestPath = decodeURIComponent((req.url ?? "/").split("?")[0]);
          const filePath = path.resolve(sampleWorkspaceRoot, `.${requestPath}`);

          if (!filePath.startsWith(sampleWorkspaceRoot)) {
            res.statusCode = 403;
            res.end("Forbidden");
            return;
          }

          fs.stat(filePath, (statError, stat) => {
            if (statError || !stat.isFile()) {
              next();
              return;
            }

            if (filePath.endsWith(".wav")) res.setHeader("Content-Type", "audio/wav");
            if (filePath.endsWith(".json")) res.setHeader("Content-Type", "application/json");
            if (filePath.endsWith(".md")) res.setHeader("Content-Type", "text/markdown; charset=utf-8");
            fs.createReadStream(filePath).on("error", next).pipe(res);
          });
        });
      },
    },
  ],
});
