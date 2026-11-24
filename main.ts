// bring-the-humans-03 entrypoint (Node 22, standard library only).
// The entry is the TikTok video itself: a short vertical ad for make.fun.
// This program hands the grader VIDEO.json, which names the video's
// full TikTok address. Nothing else is scored from this program.
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
const src = join(BOT_DIR, 'VIDEO.json');
// The entry is only valid when VIDEO.json names a TikTok video address.
const parsed = JSON.parse(readFileSync(src, 'utf8')) as { url?: unknown };
if (typeof parsed.url !== 'string' || !parsed.url.startsWith('https://www.tiktok.com/') || !parsed.url.includes('/video/')) {
  console.error('VIDEO.json does not name a TikTok video URL yet — post the ad and fill it in first.');
  process.exit(1);
}
writeFileSync(join(OUTPUT_DIR, 'VIDEO.json'), JSON.stringify(parsed));
