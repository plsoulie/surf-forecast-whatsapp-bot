const express = require('express');
const router = express.Router();
const User = require('../models/User');
const { getSurfForecast } = require('../services/forecastService');

// Route to handle user subscription
router.post('/subscribe', async (req, res) => {
  const { phoneNumber, location, spotId } = req.body;
  try {
    let user = await User.findOne({ phoneNumber });
    if (user) {
      return res.status(400).json({ msg: 'User already subscribed' });
    }
    user = new User({ phoneNumber, location, spotId });
    await user.save();
    res.status(200).json({ msg: 'User subscribed successfully' });
  } catch (err) {
    console.error('Error subscribing user:', err);
    res.status(500).json({ msg: 'Server error' });
  }
});

// Route to get forecast for a specific spot
router.get('/forecast/:spotId', async (req, res) => {
  const { spotId } = req.params;
  try {
    const forecast = await getSurfForecast(spotId);
    res.status(200).json(forecast);
  } catch (err) {
    console.error('Error fetching forecast:', err);
    res.status(500).json({ msg: 'Server error' });
  }
});

module.exports = router;
