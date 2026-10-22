import { spawn } from "node:child_process"
import { existsSync } from "node:fs"
import { dirname, join, resolve } from "node:path"
import { Plugin } from "@opencode/plugin"

const ENTRYPOINT = "sloperator.py"

interface SlopRun {
  readonly stdout: string
  readonly stderr: string
  readonly exitCode: number
}

/** Walk up from `start` until the Sloperator entrypoint is found. */
function findProjectRoot(start: string): string {
  const initial = resolve(start)
  let current = initial

  while (true) {
    if (existsSync(join(current, ENTRYPOINT))) return current
    const parent = dirname(current)
    if (parent === current) return initial
    current = parent
  }
}

/** Run `uv run --no-active sloperator.py <path>` and capture its output. */
function runSloperator(projectRoot: string, path: string): Promise<SlopRun> {
  return new Promise((resolveRun, rejectRun) => {
    const child = spawn("uv", ["run", "--no-active", ENTRYPOINT, path], {
      cwd: projectRoot,
      stdio: ["ignore", "pipe", "pipe"],
    })

    let stdout = ""
    let stderr = ""

    child.stdout.setEncoding("utf8")
    child.stderr.setEncoding("utf8")
    child.stdout.on("data", (chunk: string) => {
      stdout += chunk
    })
    child.stderr.on("data", (chunk: string) => {
      stderr += chunk
    })
    child.on("error", rejectRun)
    child.on("close", (code) => {
      resolveRun({ stdout, stderr, exitCode: code ?? 1 })
    })
  })
}

export default Plugin.define({
  id: "run-slop",
  async setup(ctx) {
    const projectRoot = findProjectRoot(ctx.location.directory)

    await ctx.tool.transform((editor) => {
      editor.add({
        name: "run_slop",
        description:
          "Run a SlopLang (.slop) program with the Sloperator interpreter. Returns the program's stdout, stderr, and exit code as JSON.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description:
                "Path to the .slop file to run. Relative paths are resolved from the project root.",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as { path: string }

          const result = await runSloperator(projectRoot, path)
          const json = JSON.stringify(result, null, 2)

          return { content: json, metadata: { exitCode: result.exitCode } }
        },
      })
    })
  },
})
