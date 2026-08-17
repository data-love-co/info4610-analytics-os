#!/usr/bin/env node
// setup.mjs — cross-platform onboarding entry point for Analytics OS.
//
// Run once after cloning:
//   node 0_System/bootstrap/setup.mjs
//
// What it does:
//   1. Creates CLAUDE.md → AGENTS.md symlink (Mac/Linux) or a generated copy (Windows fallback)
//   2. Runs non-fatal readiness checks: node version, git, python
//   3. Prints next steps
//
// Safe to re-run: CLAUDE.md is recreated each time (idempotent). No persistent state.
// Uses node:fs, node:path, node:url only — no shell-isms, no child_process.

import { existsSync, readFileSync, writeFileSync, symlinkSync, unlinkSync } from 'node:fs';
import { join, dirname, delimiter } from 'node:path';
// node:url is required for cross-platform file:// → OS path conversion.
// import.meta.dirname is not available on the Node 18 floor; fileURLToPath is.
import { fileURLToPath } from 'node:url';

// ---------------------------------------------------------------------------
// 1. Resolve repo root
// ---------------------------------------------------------------------------
const __filename = fileURLToPath(import.meta.url);
const __dirname  = dirname(__filename);
// bootstrap/ is at <repo-root>/0_System/bootstrap/
const REPO_ROOT  = join(__dirname, '..', '..');

const agentsPath = join(REPO_ROOT, 'AGENTS.md');
const claudePath = join(REPO_ROOT, 'CLAUDE.md');

// ---------------------------------------------------------------------------
// 2. Create CLAUDE.md — symlink on Mac/Linux, generated copy on Windows
// ---------------------------------------------------------------------------
if (!existsSync(agentsPath)) {
  console.error('✗ AGENTS.md not found — cannot create CLAUDE.md');
  process.exit(1);
}

// Remove any existing CLAUDE.md (file or symlink) so re-runs are idempotent.
if (existsSync(claudePath)) {
  unlinkSync(claudePath);
}

const platform = process.platform; // 'darwin' | 'win32' | 'linux'

if (platform !== 'win32') {
  // Mac / Linux: create a real symlink CLAUDE.md → AGENTS.md.
  // Fall back to a copy if symlinkSync throws (e.g. EPERM on unusual mounts).
  try {
    symlinkSync('AGENTS.md', claudePath);
    console.log('✓ CLAUDE.md symlinked to AGENTS.md');
  } catch (err) {
    writeCopy();
    console.log(`✓ CLAUDE.md generated (symlink failed: ${err.code ?? err.message} — copy fallback)`);
  }
} else {
  // Windows: symlink support requires elevated privileges or Developer Mode;
  // skip the attempt and go straight to the copy.
  writeCopy();
  console.log('✓ CLAUDE.md generated (Windows copy fallback)');
}

// ---------------------------------------------------------------------------
// 3. Non-fatal readiness checks (warn only — nothing exits on failure)
// ---------------------------------------------------------------------------

// Node version: must be >= 18 for this setup script.
const nodeVersion = process.versions.node; // e.g. "20.11.0"
const nodeMajor   = parseInt(nodeVersion.split('.')[0], 10);
if (nodeMajor >= 18) {
  console.log(`✓ Node ${nodeVersion}`);
} else {
  console.warn(`⚠ Node ${nodeVersion} detected — Node 18+ is required for this setup script.`);
  printNodeInstallHint();
}

// git and python: probe PATH for the binaries, no subprocess.
const pathDirs = (process.env.PATH || '').split(delimiter);

checkBinary('git', ['git', 'git.exe'], () => {
  console.warn('⚠ git not found in PATH.');
  if (platform === 'win32') {
    console.warn('  Install: winget install --id Git.Git -e --source winget');
    console.warn('  Then open a NEW terminal so PATH refreshes.');
  } else if (platform === 'darwin') {
    console.warn('  Install: brew install git   (or xcode-select --install)');
  } else {
    console.warn('  Install: sudo apt install git   (or your distro package manager)');
  }
});

checkBinary('python', ['python3', 'python', 'python.exe', 'python3.exe'], () => {
  console.warn('⚠ python not found in PATH — optional.');
  console.warn('  Only needed for the file converter and the sample-data generator.');
  if (platform === 'win32') {
    console.warn('  Install: winget install --id Python.Python.3.12 -e --source winget');
  } else if (platform === 'darwin') {
    console.warn('  Install: brew install python');
  } else {
    console.warn('  Install: sudo apt install python3');
  }
});

// ---------------------------------------------------------------------------
// 4. Next steps
// ---------------------------------------------------------------------------
console.log(`
Setup complete. Next:
  • Open the repo in your agent (Claude Code, etc.) — it reads CLAUDE.md automatically.
  • Say "get me started" to run the bootstrap interview.
  • Drop your data into 5_Library/sources/raw/, then say "ingest my data".
    No data you're allowed to use? Use 5_Library/sample-data/ instead — that's what it's for.
  • Then say "help me frame my decision" — that's where the real work starts.`);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Write a generated copy of AGENTS.md to claudePath.
 * Used as a Windows fallback (and non-Windows EPERM fallback).
 */
function writeCopy() {
  const agentsContent = readFileSync(agentsPath, 'utf8');
  const claudeContent =
    '<!-- GENERATED FROM AGENTS.md by 0_System/bootstrap/setup.mjs — DO NOT EDIT. -->\n' +
    '<!-- Edit AGENTS.md and re-run setup.mjs instead. -->\n' +
    '\n' +
    agentsContent;
  writeFileSync(claudePath, claudeContent, 'utf8');
}

/**
 * Scan PATH for any of the given file names.
 * Pure fs — no subprocess.
 */
function checkBinary(label, names, onMissing) {
  const found = pathDirs.some(dir =>
    names.some(name => existsSync(join(dir, name)))
  );
  if (found) {
    console.log(`✓ ${label} found`);
  } else {
    onMissing();
  }
}

function printNodeInstallHint() {
  if (platform === 'win32') {
    console.warn('  Install: winget install --id OpenJS.NodeJS.LTS -e --source winget');
    console.warn('  Then open a NEW terminal so PATH refreshes.');
  } else if (platform === 'darwin') {
    console.warn('  Install: brew install node');
  } else {
    console.warn('  Install: https://nodejs.org/en/download  (use LTS)');
  }
}
