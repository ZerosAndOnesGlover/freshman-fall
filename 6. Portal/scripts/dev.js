#!/usr/bin/env node
/**
 * Runs the API and the web dev server together, with prefixed output.
 *
 * This exists so the root package has no dependencies at all — `npm run dev`
 * works straight after cloning, without an install step of its own.
 */
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm';

const COLOURS = { api: '\x1b[36m', web: '\x1b[35m', vault: '\x1b[33m' };
const RESET = '\x1b[0m';

const children = [];

function run(name, cwd, args) {
  const child = spawn(npm, args, { cwd: path.join(ROOT, cwd), shell: process.platform === 'win32' });
  const tag = `${COLOURS[name]}[${name}]${RESET} `;

  const pipe = (stream, out) => {
    let buffer = '';
    stream.on('data', (chunk) => {
      buffer += chunk.toString();
      const lines = buffer.split('\n');
      buffer = lines.pop();
      for (const line of lines) out.write(tag + line + '\n');
    });
  };
  pipe(child.stdout, process.stdout);
  pipe(child.stderr, process.stderr);

  child.on('exit', (code) => {
    console.log(`${tag}exited with code ${code}`);
    stop();
    process.exit(code ?? 0);
  });

  children.push(child);
  return child;
}

function stop() {
  for (const c of children) {
    if (!c.killed) c.kill('SIGTERM');
  }
}

for (const signal of ['SIGINT', 'SIGTERM']) {
  process.on(signal, () => { stop(); process.exit(0); });
}

run('api', 'server', ['run', 'dev']);
run('web', 'web', ['run', 'dev']);
// Watches the vault so new lectures, weeks and courses are indexed as they
// are written, without anyone having to remember to re-import.
run('vault', 'server', ['run', 'watch']);
