import pkg from "openapi-typescript-codegen";
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";

const { generateApi } = pkg;
const __dirname = dirname(fileURLToPath(import.meta.url));

async function generate() {
  await generateApi({
    input: resolve(__dirname, "../openapi.json"),
    output: "./src/api",
    httpClient: "axios",
  });
}

generate();
