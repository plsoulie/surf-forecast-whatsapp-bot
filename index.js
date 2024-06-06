require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const { MessagingResponse } = require('twilio').twiml;
const { exec } = require('child_process');
const { User } = require('./db');

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));

app.post('/whatsapp', async (req, res) => {
    const incomingMsg = req.body.Body.trim();
    const fromNumber = req.body.From;
    const response = new MessagingResponse();

    const user = await User.findOne({ mobileNumber: fromNumber });

    if (!user) {
        // New user, ask for their name
        await User.create({ mobileNumber: fromNumber, state: 'awaiting_name' });
        response.message('Hello! What is your first name?');
    } else if (user.state === 'awaiting_name') {
        // Update user's name and change state
        user.firstName = incomingMsg;
        user.state = 'awaiting_spot';
        await user.save();
        response.message(`Thanks, ${incomingMsg}! Now, send me the name of the surf spot you want to check.`);
    } else if (user.state === 'awaiting_spot') {
        // Process the spot name and return forecast
        getForecast(incomingMsg, (forecast) => {
            response.message(forecast);
            res.set('Content-Type', 'text/xml');
            res.send(response.toString());
        });
        return;
    } else {
        response.message("Please send 'forecast <spot_name>' to get the surf forecast.");
    }

    res.set('Content-Type', 'text/xml');
    res.send(response.toString());
});

function getForecast(spotName, callback) {
    exec(`python main.py "${spotName}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return callback("Failed to retrieve the forecast.");
        }
        callback(stdout);
    });
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
