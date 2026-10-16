const axios = require('axios');
const AI_SERVICE_URL = 'http://localhost:8000';

async function startWorkflow(topic) {
    const url = `${AI_SERVICE_URL}/workflow/start`;
    const body = { topic };
    const response = await axios.post(url, body);
    return response.data;
}

async function getStatus(threadId) {
    const url = `${AI_SERVICE_URL}/workflow/status/${threadId}`
    const response = axios.get(url);
    return (await response).data;
}

async function resumeWork(threadId, decision) {
    const url = `${AI_SERVICE_URL}/workflow/resume`;
    const body = { thread_id: threadId, decision };
    const response = axios.post(url, body);
    return (await response).data;
}

module.exports = {
startWorkflow,
getStatus,
resumeWork
}