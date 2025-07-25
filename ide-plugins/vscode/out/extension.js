"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
const axios_1 = require("axios");
function activate(context) {
    const orchestrateCommand = vscode.commands.registerCommand('t-developer.orchestrate', async () => {
        const goal = await vscode.window.showInputBox({
            prompt: 'Enter your goal for T-Developer to orchestrate'
        });
        if (goal) {
            await orchestrateGoal(goal);
        }
    });
    const generateAgentCommand = vscode.commands.registerCommand('t-developer.generateAgent', async () => {
        const agentName = await vscode.window.showInputBox({
            prompt: 'Enter agent name'
        });
        const agentGoal = await vscode.window.showInputBox({
            prompt: 'Enter agent goal/purpose'
        });
        if (agentName && agentGoal) {
            await generateAgent(agentName, agentGoal);
        }
    });
    const dashboardCommand = vscode.commands.registerCommand('t-developer.showDashboard', () => {
        const panel = vscode.window.createWebviewPanel('t-developer-dashboard', 'T-Developer Dashboard', vscode.ViewColumn.One, { enableScripts: true });
        panel.webview.html = getDashboardHtml();
    });
    context.subscriptions.push(orchestrateCommand, generateAgentCommand, dashboardCommand);
}
exports.activate = activate;
async function orchestrateGoal(goal) {
    const config = vscode.workspace.getConfiguration('t-developer');
    const apiUrl = config.get('apiUrl', 'http://localhost:8000');
    const apiKey = config.get('apiKey');
    try {
        vscode.window.showInformationMessage(`Orchestrating: ${goal}`);
        const response = await axios_1.default.post(`${apiUrl}/orchestrate`, {
            goal: goal
        }, {
            headers: apiKey ? { 'Authorization': `Bearer ${apiKey}` } : {}
        });
        if (response.data.success) {
            vscode.window.showInformationMessage('Orchestration completed!');
            const doc = await vscode.workspace.openTextDocument({
                content: JSON.stringify(response.data, null, 2),
                language: 'json'
            });
            vscode.window.showTextDocument(doc);
        }
        else {
            vscode.window.showErrorMessage(`Failed: ${response.data.error}`);
        }
    }
    catch (error) {
        vscode.window.showErrorMessage(`Error: ${error}`);
    }
}
async function generateAgent(name, goal) {
    const config = vscode.workspace.getConfiguration('t-developer');
    const apiUrl = config.get('apiUrl', 'http://localhost:8000');
    const apiKey = config.get('apiKey');
    try {
        vscode.window.showInformationMessage(`Generating agent: ${name}`);
        const response = await axios_1.default.post(`${apiUrl}/generate`, {
            type: 'agent',
            name: name,
            goal: goal
        }, {
            headers: apiKey ? { 'Authorization': `Bearer ${apiKey}` } : {}
        });
        if (response.data.success) {
            vscode.window.showInformationMessage('Agent generated!');
            const doc = await vscode.workspace.openTextDocument({
                content: response.data.code,
                language: 'python'
            });
            vscode.window.showTextDocument(doc);
        }
        else {
            vscode.window.showErrorMessage(`Failed: ${response.data.error}`);
        }
    }
    catch (error) {
        vscode.window.showErrorMessage(`Error: ${error}`);
    }
}
function getDashboardHtml() {
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <title>T-Developer Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .metric { margin: 10px 0; padding: 10px; border: 1px solid #ccc; }
            .status { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>T-Developer Dashboard</h1>
        <div class="metric">
            <h3>System Status</h3>
            <p class="status">✅ Online</p>
        </div>
        <div class="metric">
            <h3>Active Agents</h3>
            <p>Loading...</p>
        </div>
        <div class="metric">
            <h3>Recent Workflows</h3>
            <p>Loading...</p>
        </div>
    </body>
    </html>
    `;
}
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map