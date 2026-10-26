const express = require('express');
const cors = require('cors');
const workflowRoutes = require('./routes/workflow');

const app = express();
app.use(cors());
app.use(express.json());

app.use('./api/workflow', workflowRoutes);

app.listen(3001, () => {
    console.log('Backend is running on port 3001');
})