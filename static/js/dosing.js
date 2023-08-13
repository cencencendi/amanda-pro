// All variables are stored here
const dosingControlMode = document.getElementById('dosing-control-mode');
const manualLabel = document.getElementById('manual-dosing');
const autoLabel = document.getElementById('auto-dosing');
const ecSwitch = document.getElementById('ec-switch');
const phSwitch = document.getElementById('ph-switch');
const ecPlusMinBtn = {
  target: {
    min: document.getElementById('ec-target-min'),
    plus: document.getElementById('ec-target-plus'),
  },
  tolerance: {
    min: document.getElementById('ec-tolerance-min'),
    plus: document.getElementById('ec-tolerance-plus'),
  },
};
const phPlusMinBtn = {
  target: {
    min: document.getElementById('ph-target-min'),
    plus: document.getElementById('ph-target-plus'),
  },
  tolerance: {
    min: document.getElementById('ph-tolerance-min'),
    plus: document.getElementById('ph-tolerance-plus'),
  },
};

const ecTarget = document.getElementById('ec-target');
const ecTolerance = document.getElementById('ec-tolerance');
const phTarget = document.getElementById('ph-target');
const phTolerance = document.getElementById('ph-tolerance');
const schedulesContainer = document.getElementById('schedules-container');
let listOfSchedules = [];
let isDosingAuto = dosingControlMode.checked;
// The end of stored variables

getDosingData();

manualLabel.addEventListener('click', function () {
  dosingControlMode.checked = false;
  isDosingAuto = false;
  updateStyles();
  updateData();
});

autoLabel.addEventListener('click', function () {
  dosingControlMode.checked = true;
  isDosingAuto = true;
  updateStyles();
  updateData();
});

// Set the EC and PH Target and Tolerance

// Function to update label style
function updateStyles() {
  if (isDosingAuto) {
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

// Function to disable or undisable switch if Dosing Mode is Auto or Manual
function disableControl() {
  // Disable or undisable ecSwitch and pHSwitch
  ecSwitch.disabled = isDosingAuto ? true : false;
  phSwitch.disabled = isDosingAuto ? true : false;

  for (key in ecPlusMinBtn) {
    const targetAndTolerance = ecPlusMinBtn[key];
    for (btnKey in targetAndTolerance) {
      if (targetAndTolerance.hasOwnProperty(btnKey)) {
        const btn = targetAndTolerance[btnKey];
        const btnIcon = btn.querySelector('svg');
        // Set the Plus or Min icon color based on the dosing control mode
        btnIcon.style.fill = isDosingAuto ? (btnKey == 'min' ? 'red' : 'rgba(15, 177, 112, 1)') : 'rgba(155, 155, 155, 1)';
        // Set the Plus or Min icon cursor based on the dosing control mode
        btn.style.cursor = isDosingAuto ? 'pointer' : 'not-allowed';
      }
    }
  }

  //   Just same as before but this control the pH target and tolerance button
  for (key in phPlusMinBtn) {
    const targetAndTolerance = phPlusMinBtn[key];
    for (btnKey in targetAndTolerance) {
      if (targetAndTolerance.hasOwnProperty(btnKey)) {
        const btn = targetAndTolerance[btnKey];
        const btnIcon = btn.querySelector('svg');
        btnIcon.style.fill = isDosingAuto ? (btnKey == 'min' ? 'red' : 'rgba(15, 177, 112, 1)') : 'rgba(155, 155, 155, 1)';
        btn.style.cursor = isDosingAuto ? 'pointer' : 'not-allowed';
      }
    }
  }
}

// Function to handle click target and tolerance button
function handleClickPlusMin(event) {
  if (!isDosingAuto) {
    return;
  }
  const clickedId = event.currentTarget.id;

  function updateEcTarget() {
    ecTarget.textContent = clickedId.startsWith('ec-target')
      ? clickedId.endsWith('plus')
        ? parseInt(ecTarget.textContent) + 100
        : parseInt(ecTarget.textContent) - 100
      : parseInt(ecTarget.textContent);
  }

  function updateEcTolerance() {
    ecTolerance.textContent = clickedId.startsWith('ec-tolerance')
      ? clickedId.endsWith('plus')
        ? parseInt(ecTolerance.textContent) + 50
        : parseInt(ecTolerance.textContent) - 50
      : parseInt(ecTolerance.textContent);
  }

  function updatePhTarget() {
    phTarget.textContent = clickedId.startsWith('ph-target')
      ? clickedId.endsWith('plus')
        ? (parseFloat(phTarget.textContent) + 0.1).toFixed(1)
        : (parseFloat(phTarget.textContent) - 0.1).toFixed(1)
      : parseFloat(phTarget.textContent);
  }

  function updatePhTolerance() {
    phTolerance.textContent = clickedId.startsWith('ph-tolerance')
      ? clickedId.endsWith('plus')
        ? (parseFloat(phTolerance.textContent) + 0.1).toFixed(1)
        : (parseFloat(phTolerance.textContent) - 0.1).toFixed(1)
      : parseFloat(phTolerance.textContent);
  }

  function updateDripDurationAdd() {
    const dripDuration = document.getElementById('add-drip-duration');

    dripDuration.textContent = clickedId.startsWith('add-drip-duration')
      ? clickedId.endsWith('plus')
        ? parseInt(dripDuration.textContent) + 1
        : parseInt(dripDuration.textContent) - 1
      : parseInt(dripDuration.textContent);
  }

  updateEcTarget();
  updateEcTolerance();
  updatePhTarget();
  updatePhTolerance();
  updateData();
  updateDripDurationAdd();
}

// Function Add Schedule
function addSchedule() {
  // Get the schedule time
  const scheduleTime = document.getElementById('add-schedule-time-input');
  const scheduleDuration = document.getElementById('add-drip-duration');

  if (scheduleTime.value && scheduleDuration.textContent) {
    listOfSchedules.push({ time: scheduleTime.value, duration: scheduleDuration.textContent });
    // Sort the schedules
    listOfSchedules = sortTime(listOfSchedules);
    updateData();
    updateSchedule();
  }
}

// Function Delete Schedule
function deleteSchedule(event) {
  const scheduleId = event.currentTarget.id;
  const numberOfSchedule = scheduleId[scheduleId.length - 1];

  listOfSchedules.splice(numberOfSchedule - 1, 1);
  updateData();
  updateSchedule();
}
function updateSchedule() {
  if (listOfSchedules.length == 0) {
    schedulesContainer.innerHTML = emptySchedule();
    return;
  }

  let schedulesDiv = headerOfSchedule();
  listOfSchedules.forEach((schedule, index) => (schedulesDiv += scheduleDivContent(schedule, index)));
  schedulesContainer.innerHTML = schedulesDiv;
}

function sortTime(listOfSchedules) {
  listOfSchedules.sort((first, second) => {
    // Split the time string into hours and minutes
    const [firstHours, firstMinutes] = first.time.split(':').map(Number);
    const [secondHours, secondMinutes] = second.time.split(':').map(Number);

    // Compare hours first, if they are different, return the comparison result
    if (firstHours !== secondHours) {
      return firstHours - secondHours;
    }

    // If hours are the same, compare minutes
    return firstMinutes - secondMinutes;
  });
  return listOfSchedules;
}

function scheduleDivContent(schedule, index) {
  return `<div class="row my-2 mx-0">
            <div class="col-5 fs-5">Schedule ${index + 1}</div>
            <div class="col fs-5">${schedule.time}</div>
            <div class="col fs-5">${schedule.duration} ${schedule.duration < 2 ? 'minute' : 'minutes'}</div>
            <div class="col d-flex justify-content-evenly align-items-center position-relative">
                <svg width="25" height="25" style="fill: red; cursor: pointer;" id="delete-schedule-${
                  index + 1
                }" onclick="deleteSchedule(event)"><use xlink:href="#trash" /></svg>
            </div>
          </div>`;
}

function emptySchedule() {
  return `<div class="d-flex justify-content-center align-items-center py-5 mt-5" id="empty-schedule">
            <span class="fs-2 fw-bold fst-italic h-100 mt-5">Empty Schedule</span></div>`;
}

function headerOfSchedule() {
  return `<div class="row my-2 mx-0">
            <div class="col-5 fw-bold fs-5">Schedule Name</div>
            <div class="col fw-bold fs-5">Time</div>
            <div class="col fw-bold fs-5">Duration</div>
            <div class="col fw-bold fs-5"></div>
          </div>`;
}

// ============================= POST AND GET DATA TO OR FROM DJANGO ===============================
// Funtion to get dosing data
async function getDosingData() {
  try {
    const response = await fetch('/setting/dosing/get-dosing-data/');
    const data = await response.json();

    // Update switches condition
    dosingControlMode.checked = data['dosingControlMode'];
    isDosingAuto = data['dosingControlMode'];

    for (let key in data['dosingSwitches']) {
      const element = document.getElementById(key);
      if (data['dosingSwitches'].hasOwnProperty(key)) {
        element.checked = data['dosingSwitches'][key];
      }
    }

    // Update Target and Tolerance
    for (let key in data['targetAndTolerance']) {
      const element = document.getElementById(key);
      if (data['targetAndTolerance'].hasOwnProperty(key)) {
        element.textContent = data['targetAndTolerance'][key];
      }
    }

    listOfSchedules = data['wateringSchedule'];
    updateStyles();
    updateSchedule();
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

async function updateData() {
  // POST data to database

  // Get the csrfToken (THIS IS IMPORTANT! DO NOT DELETE!)
  function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
  }

  const csrfToken = getCookie('csrftoken');

  try {
    const response = await fetch('post-dosing-data/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        dosingMode: isDosingAuto,
        targetAndTolerance: {
          ec_target: ecTarget.textContent,
          ec_tolerance: ecTolerance.textContent,
          ph_target: phTarget.textContent,
          ph_tolerance: phTolerance.textContent,
        },
        wateringSchedule: listOfSchedules,
        dosingSwitches: {
          ec_switch: ecSwitch.checked,
          ph_switch: phSwitch.checked,
        },
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
}
