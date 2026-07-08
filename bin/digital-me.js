#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const packageRoot = path.resolve(__dirname, "..");
const packageJson = require(path.join(packageRoot, "package.json"));
const archivePath = path.join(packageRoot, "digital-me.skill");
const skillName = "digital-me";

function usage() {
  console.log(`Digital Me skill installer v${packageJson.version}

Usage:
  npx --yes github:EthanSMC/digital-me#v${packageJson.version}
  digital-me [--dest <skills-dir>] [--force]

Options:
  --dest <dir>   Skills directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.
  --force        Replace an existing digital-me skill directory.
  --version      Print the installer version.
  --help         Show this help.
`);
}

function parseArgs(argv) {
  const options = {
    dest: process.env.CODEX_HOME
      ? path.join(process.env.CODEX_HOME, "skills")
      : path.join(os.homedir(), ".codex", "skills"),
    force: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") {
      options.help = true;
    } else if (arg === "--") {
      continue;
    } else if (arg === "--version" || arg === "-v") {
      options.version = true;
    } else if (arg === "--force" || arg === "-f") {
      options.force = true;
    } else if (arg === "--dest") {
      const value = argv[i + 1];
      if (!value) {
        throw new Error("--dest requires a directory path.");
      }
      options.dest = path.resolve(value);
      i += 1;
    } else {
      throw new Error(`Unknown option: ${arg}`);
    }
  }

  return options;
}

function run(command, args) {
  const result = spawnSync(command, args, { stdio: "inherit" });
  if (result.error) {
    throw result.error;
  }
  if (result.status !== 0) {
    throw new Error(`${command} exited with status ${result.status}`);
  }
}

function unzipArchive(source, destination) {
  if (process.platform === "win32") {
    run("powershell.exe", [
      "-NoProfile",
      "-Command",
      "Expand-Archive",
      "-LiteralPath",
      source,
      "-DestinationPath",
      destination,
      "-Force",
    ]);
    return;
  }

  run("unzip", ["-q", source, "-d", destination]);
}

function install(options) {
  if (!fs.existsSync(archivePath)) {
    throw new Error(`Missing skill archive: ${archivePath}`);
  }

  const target = path.join(options.dest, skillName);
  if (fs.existsSync(target) && !options.force) {
    throw new Error(
      `${target} already exists. Re-run with --force to replace it.`
    );
  }

  fs.mkdirSync(options.dest, { recursive: true });
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), `${skillName}-`));

  try {
    unzipArchive(archivePath, tmp);
    const skillFile = path.join(tmp, "SKILL.md");
    if (!fs.existsSync(skillFile)) {
      throw new Error("Archive did not contain SKILL.md.");
    }

    if (options.force) {
      fs.rmSync(target, { recursive: true, force: true });
    }
    fs.cpSync(tmp, target, { recursive: true });
  } catch (error) {
    fs.rmSync(tmp, { recursive: true, force: true });
    throw error;
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }

  console.log(`Installed Digital Me to ${target}`);
  console.log("Restart Codex to pick up the skill.");
}

function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) {
      usage();
      return;
    }
    if (options.version) {
      console.log(packageJson.version);
      return;
    }
    install(options);
  } catch (error) {
    console.error(`digital-me: ${error.message}`);
    process.exitCode = 1;
  }
}

main();
