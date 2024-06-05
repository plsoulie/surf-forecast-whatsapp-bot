const { exec } = require('child_process');

const getSurfForecast = (spotId) => {
  return new Promise((resolve, reject) => {
    exec(`python get_surf_forecast.py ${spotId}`, (error, stdout, stderr) => {
      if (error) {
        return reject(error);
      }
      try {
        const forecast = JSON.parse(stdout);
        resolve(forecast);
      } catch (parseError) {
        reject(parseError);
      }
    });
  });
};

module.exports = {
  getSurfForecast,
};
