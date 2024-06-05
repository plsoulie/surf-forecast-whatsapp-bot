// models/User.js
const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
  phoneNumber: { type: String, required: true, unique: true },
  location: { type: String, required: true },
  subscribed: { type: Boolean, default: true }
});

module.exports = mongoose.model('User', UserSchema);
