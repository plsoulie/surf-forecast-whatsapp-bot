# SwellBot: Express.js WhatsApp Chatbot with PySurfline Integration

This project demonstrates the integration of an Express.js-based WhatsApp chatbot with the PySurfline API, allowing users to get real-time surf conditions directly through WhatsApp.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Overview

The application combines an Express.js server and a WhatsApp chatbot with Python's PySurfline library to provide users with surf condition updates. Users can send messages to the WhatsApp chatbot to get current surf conditions from Surfline.

## Features

- WhatsApp chatbot built using Express.js.
- Fetch real-time surf conditions using PySurfline.
- Easy setup and deployment.
- MongoDB integration for data storage.
- Twilio integration for WhatsApp messaging.

## Installation

### Prerequisites

- Node.js (v14.x or later)
- Python (v3.6 or later)
- npm (comes with Node.js)
- pip (comes with Python)
- ngrok (for local development)
- MongoDB account
- Twilio account

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/swellbot.git
   cd swellbot
   ```

2. **Install Node.js dependencies:**

   ```bash
   npm install
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add the following:

   ```
   PORT=3000
   MONGODB_URI=your_mongodb_uri
   TWILIO_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number
   ```

5. **Start the server:**

   ```bash
   npm start
   ```

6. **Expose your local server to the internet using ngrok:**
   ```bash
   ngrok http 3000
   ```

## Usage

1. Set up a Twilio WhatsApp sandbox and configure it to use the ngrok URL as your webhook.

2. Send a message to your WhatsApp bot using the Twilio WhatsApp number.

3. The bot will respond with current surf conditions for the specified location.
