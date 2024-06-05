const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  phoneNumber: String,
  location: String,
  spotId: String,
  subscribed: { type: Boolean, default: true }
});

module.exports = mongoose.model('User', userSchema);
