const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');

const app = express();
const port = 3000;

// Enable CORS for all routes
app.use(cors());

// Middleware to parse JSON body
app.use(express.json());

// Define the endpoint to handle requests
app.post('/api/score', async (req, res) => {
    try {
        // Replace with your Azure endpoint URL and API key
        const endpointUrl = 'https://ai-workspace-nriyl.australiasoutheast.inference.ml.azure.com/score';
        const apiKey = 'fLi4FITjX4ZOZzAIVHCZAs0nLL4ESh9n'; // Add your Azure API key here

        // Make a POST request to the Azure endpoint
        const response = await fetch(endpointUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify(req.body)
        });

        // Check if the response is OK
        if (!response.ok) {
            return res.status(response.status).send('Error connecting to Azure endpoint');
        }

        // Parse the JSON response
        const result = await response.json();
        res.json(result); // Send the result back to the client
    } catch (error) {
        console.error('Error:', error);
        res.status(500).send('Error connecting to Azure endpoint');
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Proxy server running at http://localhost:${port}`);
});
