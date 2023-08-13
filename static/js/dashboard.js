// All variables are stored here
const dashboardCard = {
  ecValue: document.querySelector('#EC-value .card-text'),
  pHValue: document.querySelector('#pH-value .card-text'),
  doValue: document.querySelector('#DO-value .card-text'),
  waterTempValue: document.querySelector('#water-temp-value .card-text'),
  kWhValue: document.querySelector('#kWh-value .card-text'),
  co2Value: document.querySelector('#CO2-value .card-text'),
};

const locAndTime = {
  location: document.getElementById('location'),
  date: document.getElementById('date'),
  time: document.getElementById('time'),
};
// The end of stored variables

getDashboardData();

async function getDashboardData() {
  let prevMinute = null;

  async function updateTime() {
    const nowMinute = new Date().getMinutes();

    if (nowMinute !== prevMinute) {
      await getSensorData();
      await getLocationDatetimeData();

      prevMinute = nowMinute;
    }
  }

  async function getSensorData() {
    try {
      const response = await fetch('/get-dashboard-data/');
      const data = await response.json();

      // Update sensor values on the dashboard
      const sensorValue = data['sensorValue'];
      for (const key in sensorValue) {
        if (sensorValue.hasOwnProperty(key)) {
          const value = sensorValue[key];
          dashboardCard[key].textContent = value;
        }
      }

      // Update sensor alert conditions
      const sensingCondition = data['sensingCondition'];
      const ecValueCard = document.getElementById('EC-value');
      const phValueCard = document.getElementById('pH-value');

      if (!sensingCondition['isECAppropriate']) {
        ecValueCard.classList.add('sensor-alert');
      } else {
        ecValueCard.classList.remove('sensor-alert');
      }

      if (!sensingCondition['ispHAppropriate']) {
        phValueCard.classList.add('sensor-alert');
      } else {
        phValueCard.classList.remove('sensor-alert');
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  async function getLocationDatetimeData() {
    try {
      const response = await fetch('/get-location-and-datetime/');
      const data = await response.json();

      // Update location and datetime values on the dashboard
      for (const key in data) {
        if (data.hasOwnProperty(key)) {
          const value = data[key];
          locAndTime[key].textContent = value;
        }
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  // Call updateTime every 100 milliseconds
  setInterval(updateTime, 100);
}
