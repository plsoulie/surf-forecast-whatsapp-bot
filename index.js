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
        await User.create({ mobileNumber: fromNumber, state: 'awaiting_name' });
        response.message('Hello! What is your first name?');
    } else if (user.state === 'awaiting_name') {
        user.firstName = incomingMsg;
        user.state = 'awaiting_spot';
        await user.save();
        response.message(`Thanks, ${incomingMsg}! Now, send me the name of the surf spot you want to check.`);
    } else if (user.state === 'awaiting_spot') {
        getSpotIds(incomingMsg, async (spots) => {
            console.log("Received spots:", spots);  // Debugging log
            if (spots && spots.length > 1) {
                user.state = 'selecting_spot';
                user.spotOptions = spots;
                await user.save();
                const spotsMessage = spots.map((spot, index) => `${index + 1}. ${spot.name}, ${spot.location}`).join('\n');
                response.message(`Multiple spots found:\n${spotsMessage}\nPlease reply with the number of the spot you are interested in.`);
            } else if (spots && spots.length === 1) {
                const forecast = await getForecast(spots[0].id);
                response.message(forecast);
            } else {
                response.message('Spot not found. Please try again.');
            }
            res.set('Content-Type', 'text/xml');
            res.send(response.toString());
        });
        return;
    } else if (user.state === 'selecting_spot') {
        const selectedSpotIndex = parseInt(incomingMsg) - 1;
        if (user.spotOptions && user.spotOptions[selectedSpotIndex]) {
            const selectedSpotId = user.spotOptions[selectedSpotIndex].id;
            const forecast = await getForecast(selectedSpotId);
            response.message(forecast);
            user.state = 'awaiting_spot';
            user.spotOptions = [];
            await user.save();
        } else {
            response.message('Invalid selection. Please try again.');
        }
        res.set('Content-Type', 'text/xml');
        res.send(response.toString());
    } else {
        response.message("Please send 'forecast <spot_name>' to get the surf forecast.");
        res.set('Content-Type', 'text/xml');
        res.send(response.toString());
    }
});

function getSpotIds(spotName, callback) {
    exec(`python3 surf_api.py get_spot_id "${spotName}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            console.error(`stderr: ${stderr}`);
            return callback([]);
        }
        console.log("Raw output from get_spot_id:", stdout);  // Debugging log
        console.log("Error output from get_spot_id:", stderr);  // Debugging log
        const spots = stdout.split('\n').filter(line => line).map(line => {
            const [id, name, location] = line.split('|');
            return { id, name, location };
        });
        console.log("Parsed spots:", spots);  // Debugging log
        callback(spots);
    });
}

function getForecast(spotId) {
    return new Promise((resolve, reject) => {
        exec(`python3 main.py "${spotId}"`, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                console.error(`stderr: ${stderr}`);
                resolve("Failed to retrieve the forecast.");
            }
            resolve(stdout);
        });
    });
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
