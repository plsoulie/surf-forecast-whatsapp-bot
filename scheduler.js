// scheduler.js
const cron = require('node-cron');
const axios = require('axios');
const twilio = require('twilio');
const User = require('./models/User');

const client = twilio(process.env.TWILIO_SID, process.env.TWILIO_AUTH_TOKEN);

const fetchForecast = async (location) => {
  const weatherResponse = await axios.get(`https://api.openweathermap.org/data/2.5/weather?q=${location}&appid=${process.env.OPENWEATHERMAP_API_KEY}`);
  // const tideResponse = await axios.get(`https://www.worldtides.info/api/v2?lat=...&lon=...&key=${process.env.WORLDTIDES_API_KEY}`);

  // Process and format the data
  const forecast = {
    weather: weatherResponse.data.weather[0].description,
    temperature: weatherResponse.data.main.temp,
    windSpeed: weatherResponse.data.wind.speed,
    windDirection: weatherResponse.data.wind.deg,
    // Process tide data similarly
  };

  return forecast;
};

const sendForecasts = async () => {
  const users = await User.find({ subscribed: true });
  users.forEach(async (user) => {
    const forecast = await fetchForecast(user.location);
    const message = `Weather: ${forecast.weather}\nTemperature: ${forecast.temperature}\nWind: ${forecast.windSpeed} m/s from ${forecast.windDirection} degrees\n...`; // Add more details
    await client.messages.create({
      from: `whatsapp:${process.env.TWILIO_WHATSAPP_NUMBER}`,
      to: `whatsapp:${user.phoneNumber}`,
      body: message,
    });
  });
};

// Schedule the task
cron.schedule('6 22 * * *', sendForecasts, {
  scheduled: true,
  timezone: 'Europe/Paris'
});
