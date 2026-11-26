// Thursday Echo — the news-image entry for 26 November 2026.
// Node 22, standard library only. draw.py renders entry.png and ships
// beside this file; this program only copies it to the grader's output
// directory, so both runs write the same bytes.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const image = join(root, "entry.png");
const target = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

if (!existsSync(image)) {
  throw new Error("entry.png is missing next to main.ts");
}

mkdirSync(target, { recursive: true });
copyFileSync(image, join(target, "entry.png"));
const sourceBytes = statSync(image).size;
const bytes = statSync(join(target, "entry.png")).size;
if (bytes !== sourceBytes) {
  throw new Error("copied entry.png (" + bytes + " bytes) does not match " +
    "the source (" + sourceBytes + " bytes)");
}
console.log("wrote entry.png (" + bytes + " bytes) to " + target);
