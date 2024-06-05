// routes/users.js
const express = require('express');
const router = express.Router();
const User = require('../models/User');

// Subscribe a user
router.post('/subscribe', async (req, res) => {
  const { phoneNumber, location } = req.body;
  try {
    let user = await User.findOne({ phoneNumber });
    if (user) {
      return res.status(400).json({ msg: 'User already subscribed' });
    }
    user = new User({ phoneNumber, location });
    await user.save();
    res.status(200).json({ msg: 'User subscribed successfully' });
  } catch (err) {
    res.status(500).json({ msg: 'Server error' });
  }
});

module.exports = router;
