import * as core from "@actions/core";
import * as exec from "@actions/exec";

async function run(): Promise<void> {
  try {
    const token = core.getInput("token");
    const repoList: string[] = JSON.parse(core.getInput("repo-list"));
    const regex = /^(.+)\/(.+)@(.+)$/;

    for (const repo of repoList) {
      const match = regex.exec(repo);

      if (match === null || match.length !== 4) {
        throw new Error(`The repo ${repo} is not valid`);
      }

      const owner = match[1];
      const name = match[2];
      const ref = match[3];

      const cloneUrl = `https://${token}@github.com/${owner}/${name}.git`;
      const cloneDir = `./.github/actions/${name}`;
      const args = [
        "clone",
        "--depth=1",
        "--single-branch",
        "--branch",
        ref,
        cloneUrl,
        cloneDir,
      ];

      core.info(`Cloning ${cloneUrl}@${ref} to ${cloneDir}`);

      await exec.exec("git", args);
    }
  } catch (error) {
    if (error instanceof Error) core.setFailed(error.message);
  }
}

run();
