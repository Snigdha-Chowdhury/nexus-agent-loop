const express = require('express');
const router = express.Router();
const aiService = require('../service/aiService');

router.post('/start', async (req, res) => {
    const { topic } = req.body;
    const result = await aiService.startWorkflow(topic);
    res.json(result);
});

router.get(`/status/:threadId`, async (req, res) => {
    const { threadId } = req.params;
    const result = await aiService.getStatus(threadId);
    res.json(result);
})
router.post('/resume', async (req, res) => {
    const { threadId, decision } = req.body;
    const result = await aiService.resumeWorkflow(threadId, decision);
    res.json(result);
})

module.exports = router;