import { graphile_middleware } from "./graphile.ts";

import express from "express";

const app = express();

app.use(graphile_middleware());

export function run_server() {
  const port = process.env.PORT || 3000;

  app.listen(port, () => {
    console.log(`listening on port ${port}`);
  });
}
