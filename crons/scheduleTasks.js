const cron = require('node-cron');
const User = require('../models/User');
const twilioClient = require('../utils/twilioClient');
const { getSurfForecast } = require('../services/forecastService');
require('dotenv').config();

const sendForecasts = async () => {
  const users = await User.find({ subscribed: true });
  users.forEach(async (user) => {
    try {
      const forecast = await getSurfForecast(user.spotId);
      const message = `Surf Forecast for ${user.location}:\nWave Height: ${forecast.waveHeight}m\nWind: ${forecast.windSpeed} m/s\n...`; // Customize message

      await twilioClient.messages.create({
        from: process.env.TWILIO_WHATSAPP_NUMBER,
        to: `whatsapp:${user.phoneNumber}`,
        body: message,
      });
    } catch (error) {
      console.error(`Error fetching forecast for ${user.location}:`, error);
    }
  });
};

// Schedule the task
cron.schedule('0 22 * * *', sendForecasts, {
  scheduled: true,
  timezone: 'Europe/Paris'
});
