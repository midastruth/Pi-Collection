import type { ExecResult, ExtensionAPI } from "@mariozechner/pi-coding-agent";

const USER_MESSAGE = "Please push this worktree to GitHub main.";
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

			ctx.ui.setStatus("push", "pushing → origin/main");
			try {
				const result = await pi.exec("bash", ["-lc", COMMAND], {
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
							"The deterministic `/push` bash command could not be started. Diagnose and handle the failure.",
							"",
							`Command: \`${COMMAND}\``,
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
