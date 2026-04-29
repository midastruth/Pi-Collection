import type { ExecResult, ExtensionAPI } from "@mariozechner/pi-coding-agent";

const USER_MESSAGE = "Please push this worktree to GitHub main.";
const STATUS_COMMAND = "git status --short --branch";
const COMMAND = "GIT_TERMINAL_PROMPT=0 git push origin HEAD:main";
const TIMEOUT_MS = 120_000;

function block(label: string, value: string): string {
	return [`${label}:`, "```", value.trimEnd(), "```"].join("\n");
}

function failureMessage(result: ExecResult): string {
	return [
		"The deterministic `/push` bash command failed. Diagnose and handle the failure.",
		"",
		`Command: \`${COMMAND}\``,
		`Exit code: ${result.code}${result.killed ? " (killed)" : ""}`,
		"",
		block("stdout", result.stdout || "<empty>"),
		"",
		block("stderr", result.stderr || "<empty>"),
	].join("\n");
}

function dirtyWorktreeMessage(status: string): string {
	return [
		"The user asked to push this worktree to GitHub main, but the worktree has uncommitted changes.",
		"",
		"Do not run the push yet. Explain to the user that `git push` would only push committed history, not these local working-tree changes. Give concise next-step suggestions, such as reviewing the diff, committing the changes, stashing them, or discarding them if unwanted.",
		"",
		block("git status --short --branch", status || "<empty>"),
	].join("\n");
}

export default function pushExtension(pi: ExtensionAPI) {
	pi.registerCommand("push", {
		description: "Push the current worktree to GitHub main",
		handler: async (_args, ctx) => {
			await ctx.waitForIdle();

			// Persist the request without asking the LLM what command to run.
			pi.sendMessage({
				customType: "push",
				content: USER_MESSAGE,
				display: true,
				details: { kind: "request" },
			});

			ctx.ui.setStatus("push", "checking worktree");
			let currentCommand = STATUS_COMMAND;
			try {
				const status = await pi.exec("bash", ["-lc", currentCommand], {
					cwd: ctx.cwd,
					timeout: 10_000,
				});

				if (status.code !== 0) {
					pi.sendMessage(
						{
							customType: "push",
							content: [
								"The deterministic `/push` preflight check failed. Diagnose and handle the failure.",
								"",
								`Command: \`${STATUS_COMMAND}\``,
								`Exit code: ${status.code}${status.killed ? " (killed)" : ""}`,
								"",
								block("stdout", status.stdout || "<empty>"),
								"",
								block("stderr", status.stderr || "<empty>"),
							].join("\n"),
							display: true,
							details: { kind: "preflight-failure", command: STATUS_COMMAND, result: status },
						},
						{ triggerTurn: true },
					);
					return;
				}

				const changedLines = status.stdout
					.split("\n")
					.map((line) => line.trimEnd())
					.filter((line) => line && !line.startsWith("##"));

				if (changedLines.length > 0) {
					pi.sendMessage(
						{
							customType: "push",
							content: dirtyWorktreeMessage(status.stdout),
							display: true,
							details: { kind: "dirty-worktree", command: STATUS_COMMAND, status: status.stdout },
						},
						{ triggerTurn: true },
					);
					return;
				}

				ctx.ui.setStatus("push", "pushing → origin/main");
				currentCommand = COMMAND;
				const result = await pi.exec("bash", ["-lc", currentCommand], {
					cwd: ctx.cwd,
					timeout: TIMEOUT_MS,
				});

				if (result.code === 0) {
					pi.sendMessage({
						customType: "push",
						content: "Pushed current HEAD to GitHub main.",
						display: true,
						details: { kind: "success", command: COMMAND, result },
					});
					ctx.ui.notify("Pushed current HEAD to GitHub main.", "info");
					return;
				}

				pi.sendMessage(
					{
						customType: "push",
						content: failureMessage(result),
						display: true,
						details: { kind: "failure", command: COMMAND, result },
					},
					{ triggerTurn: true },
				);
			} catch (error) {
				const message = error instanceof Error ? error.message : String(error);
				pi.sendMessage(
					{
						customType: "push",
						content: [
							"The deterministic `/push` command could not be started. Diagnose and handle the failure.",
							"",
							`Command: \`${currentCommand}\``,
							"",
							block("error", message),
						].join("\n"),
						display: true,
						details: { kind: "error", command: COMMAND, error: message },
					},
					{ triggerTurn: true },
				);
			} finally {
				ctx.ui.setStatus("push", undefined);
			}
		},
	});
}
