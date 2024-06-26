// db.js
const mongoose = require('mongoose');

mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true });

const userSchema = new mongoose.Schema({
  mobileNumber: String,
  firstName: String,
  state: String,
  spotOptions: Array
});

const User = mongoose.model('User', userSchema);

module.exports = { User };
