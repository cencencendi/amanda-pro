// All variables are stored here
const irrigationControlMode = document.getElementById('irrigation-control-mode');
const manualLabel = document.getElementById('manual-irrigation');
const autoLabel = document.getElementById('auto-irrigation');
const sensorCycleSwitch = document.getElementById('sensor-cycle-switch');

const irrigationControlSwitches = {
  waterSupplySwitch: document.getElementById('water-supply-switch'),
  sensorPumpSwitch: document.getElementById('sensor-pump-switch'),
  plantPumpSwitch: document.getElementById('plant-pump-switch'),
  drainValveSwitch: document.getElementById('drain-valve-switch'),
};

const irrigationIcons = {
  waterSupplyIcon: document.getElementById('water-supply-pump-icon').querySelector('svg'),
  sensorPumpIcon: document.getElementById('sensor-pump-icon').querySelector('svg'),
  plantPumpIcon: document.getElementById('plant-pump-icon').querySelector('svg'),
  drainValveIcon: document.getElementById('drain-valve-icon').querySelector('svg'),
};

let isIrrigationAuto = irrigationControlMode.checked;
// The end of stored variables

getIrrigationData();

manualLabel.addEventListener('click', function () {
  irrigationControlMode.checked = false;
  isIrrigationAuto = false;
  updateStyles();
  updateData();
});

autoLabel.addEventListener('click', function () {
  irrigationControlMode.checked = true;
  isIrrigationAuto = true;
  updateStyles();
  updateData();
});

// Switch all the icon
document.getElementById('irrigation-control-container').addEventListener('click', updateData);

// Update Sensor Cycle condition if clicked
document.getElementById('sensor-cycle-switch').addEventListener('click', updateData);

// Function to update label style
function updateStyles() {
  if (irrigationControlMode.checked) {
    autoLabel.style.backgroundColor = 'rgba(15, 177, 112, 1)';
    autoLabel.style.color = 'white';
    manualLabel.style.backgroundColor = 'rgba(215, 215, 215, 1)';
    manualLabel.style.color = 'rgba(155, 155, 155, 1)';
  } else {
    autoLabel.style.backgroundColor = 'rgba(215, 215, 215, 1)';
    autoLabel.style.color = 'rgba(155, 155, 155, 1)';
    manualLabel.style.backgroundColor = 'rgba(15, 177, 112, 1)';
    manualLabel.style.color = 'white';
  }
  disableControl();
}

// Function to disable or undisable switch if Irrigation Mode is Auto or Manual
function disableControl() {
  // Automatically switch sensorCycle to true if irrigation mode is auto
  sensorCycleSwitch.checked = irrigationControlMode.checked ? true : sensorCycleSwitch.checked;
  sensorCycleSwitch.disabled = irrigationControlMode.checked ? true : false;

  // Automatically disable all switch if irrigation mode is auto
  for (let key in irrigationControlSwitches) {
    if (irrigationControlSwitches.hasOwnProperty(key)) {
      irrigationControlSwitches[key].disabled = irrigationControlMode.checked ? true : false;
    }
  }
}

// Function to update the icon color
function updateIcon() {
  for (let key in irrigationIcons) {
    const theIcon = irrigationIcons[key];
    if (irrigationIcons.hasOwnProperty(key)) {
      // Make a key from ...Icon to ...Switch (example: waterSupplyIcon to waterSupplySwitch)
      const switchKey = key.slice(0, key.indexOf('Icon')) + 'Switch';
      // Select the irrigation control switches object using the switchKey
      const theSwitch = irrigationControlSwitches[switchKey];
      theIcon.style.fill = theSwitch.checked ? 'rgba(15, 177, 112, 1)' : 'red';
    }
  }
}

// ============================= POST AND GET DATA TO OR FROM DJANGO ===============================
// Funtion to get irrigation data
async function getIrrigationData() {
  try {
    const response = await fetch('/setting/irrigation/get-irrigation-data/');
    const data = await response.json();

    const switches = data['irrigationControlSwitches'];

    // Update switches condition
    irrigationControlMode.checked = data['irrigationControlMode'];

    for (let key in irrigationControlSwitches) {
      if (irrigationControlSwitches.hasOwnProperty(key)) {
        irrigationControlSwitches[key].checked = switches[key];
      }
    }

    sensorCycleSwitch.checked = data['sensorCycleSwitch'];
    updateStyles();
    updateIcon();
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

async function updateData() {
  // POST data to database

  const irrigationSwitches = {};
  for (key in irrigationControlSwitches) {
    if (irrigationControlSwitches.hasOwnProperty(key)) {
      irrigationSwitches[key] = irrigationControlSwitches[key].checked;
    }
  }

  // Get the csrfToken (THIS IS IMPORTANT! DO NOT DELETE!)
  function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
  }

  const csrfToken = getCookie('csrftoken');

  try {
    const response = await fetch('post-irrigation-data/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        irrigationControlSwitches: irrigationSwitches,
        sensorCycleSwitch: sensorCycleSwitch.checked,
        irrigationMode: isIrrigationAuto,
      }),
    });

    if (!response.ok) {
      throw new Error('Network response was not OK');
    }

    const responseData = await response.json();
    // Handle the response data if needed
  } catch (error) {
    console.log(error);
  }

  updateIcon();
}
