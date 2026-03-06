const fs = require('fs');
const path = require('path');
const axios = require('axios'); 
require('dotenv').config();

const AGENTS_DIR = path.join(__dirname, '.ai-agents');
const GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions';

async function runAgent(agentName, userTask, previousContext = "") {
    const filePath = path.join(AGENTS_DIR, `${agentName}.md`);
    if (!fs.existsSync(filePath)) {
        throw new Error(`Agent file not found: ${filePath}`);
    }
    const systemPrompt = fs.readFileSync(filePath, 'utf-8');
    
    // Check for API key
    if (!process.env.GROQ_API_KEY) {
        throw new Error("GROQ_API_KEY is missing from .env");
    }

    try {
        const response = await axios.post(GROQ_API_URL, {
            model: "llama-3.3-70b-versatile",
            messages: [
                { role: "system", content: systemPrompt },
                { role: "user", content: `Task: ${userTask}\n\nContext: ${previousContext}` }
            ],
            response_format: { type: "json_object" }
        }, {
            headers: { 'Authorization': `Bearer ${process.env.GROQ_API_KEY}` }
        });

        return response.data.choices[0].message.content;
    } catch (error) {
        console.error(`Error in agent ${agentName}:`, error.response?.data || error.message);
        throw error;
    }
}

async function main() {
    const task = process.argv[2];
    if (!task) {
        console.error("Usage: node runner.js \"your task here\"");
        process.exit(1);
    }

    console.log(`🚀 Starting Task: ${task}`);

    try {
        // Step 1: Planner
        console.log("⏳ Running Planner...");
        const plannerOutput = await runAgent('planner', task);
        console.log("✅ Planner Finished");

        // Step 2: Architect
        console.log("⏳ Running Architect...");
        const architectOutput = await runAgent('architect', task, plannerOutput);
        console.log("✅ Architect Finished");

        // Step 3: Coder
        console.log("⏳ Running Coder...");
        const coderOutput = await runAgent('coder', task, architectOutput);
        console.log("✅ Coder Finished");

        console.log("\n--- Final Output (Coder) ---");
        console.log(coderOutput);
    } catch (error) {
        console.error("❌ Workflow failed.");
    }
}

main();
