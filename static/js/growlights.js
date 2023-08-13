// All variables are stored here
const growlightControlMode = document.getElementById('growlight-control-mode');
const manualLabel = document.getElementById('manual-growlight');
const autoLabel = document.getElementById('auto-growlight');
const growlightSwitches = {
  firstSwitch: document.getElementById('switch-growlight-1'),
  secondSwitch: document.getElementById('switch-growlight-2'),
};
const firstGrowlight = {
  firstCycle: {
    startTime: document.getElementById('growlight-1-cycle-1-start'),
    endTime: document.getElementById('growlight-1-cycle-1-end'),
  },
  secondCycle: {
    startTime: document.getElementById('growlight-1-cycle-2-start'),
    endTime: document.getElementById('growlight-1-cycle-2-end'),
  },
};
const secondGrowlight = {
  firstCycle: {
    startTime: document.getElementById('growlight-2-cycle-1-start'),
    endTime: document.getElementById('growlight-2-cycle-1-end'),
  },
  secondCycle: {
    startTime: document.getElementById('growlight-2-cycle-2-start'),
    endTime: document.getElementById('growlight-2-cycle-2-end'),
  },
};
const growlightTimes = [firstGrowlight, secondGrowlight];
let isGrowlightAuto = growlightControlMode.checked; // A variable to store the growlight mode
// The end of stored variables

getGrowlightsData();

manualLabel.addEventListener('click', function () {
  growlightControlMode.checked = false;
  isGrowlightAuto = false;
  updateStyles();
  updateData();
});

autoLabel.addEventListener('click', function () {
  growlightControlMode.checked = true;
  isGrowlightAuto = true;
  updateStyles();
  updateData();
});

// Function to update label style

function updateStyles() {
  if (isGrowlightAuto) {
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

// Function to update disable switch if Growlight Mode is Auto or Manual
function disableControl() {
  // Automatically disable all switch if growlight mode is auto
  for (let key in growlightSwitches) {
    if (growlightSwitches.hasOwnProperty(key)) {
      growlightSwitches[key].disabled = isGrowlightAuto ? true : false;
    }
  }

  // Automatically disable all time picker if growlight mode is auto
  for (let growlightTime of growlightTimes) {
    for (let cycles in growlightTime) {
      const cycle = growlightTime[cycles];
      for (let key in cycle) {
        if (cycle.hasOwnProperty(key)) {
          cycle[key].disabled = isGrowlightAuto ? false : true;
        }
      }
    }
  }
}

// ============================= POST AND GET DATA TO OR FROM DJANGO ===============================
async function updateData() {
  const firstGrowlightTime = {};
  const secondGrowlightTime = {};
  const updatedGrowlightSwitces = {};

  // Get the firstGrowlight time schedule
  for (key in firstGrowlight) {
    if (firstGrowlight.hasOwnProperty(key)) {
      firstGrowlightTime[key] = {
        startTime: firstGrowlight[key].startTime.value,
        endTime: firstGrowlight[key].endTime.value,
      };
    }
  }

  // Get the secondGrowlight time schedule
  for (key in secondGrowlight) {
    if (secondGrowlight.hasOwnProperty(key)) {
      secondGrowlightTime[key] = {
        startTime: secondGrowlight[key].startTime.value,
        endTime: secondGrowlight[key].endTime.value,
      };
    }
  }

  // Get growlightSwitches condition
  for (key in growlightSwitches) {
    if (growlightSwitches.hasOwnProperty(key)) {
      updatedGrowlightSwitces[key] = growlightSwitches[key].checked;
    }
  }

  // Get the csrfToken (THIS IS IMPORTANT! DO NOT DELETE!)
  function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
  }

  const csrfToken = getCookie('csrftoken');

  // POST data to database
  try {
    const response = await fetch('post-growlights-data/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        timeData: [firstGrowlightTime, secondGrowlightTime],
        switchesData: updatedGrowlightSwitces,
        growlightMode: isGrowlightAuto,
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

async function getGrowlightsData() {
  try {
    const response = await fetch('/setting/growlights/get-growlights-data/');
    const data = await response.json();

    const [firstGrowlightTime, secondGrowlightTime] = data['timeData'];
    const switchesData = data['switchesData'];
    const growlightMode = data['growlightMode'];

    // Update the firstGrowlight time schedule
    for (let cycles in firstGrowlight) {
      const cycle = firstGrowlight[cycles];
      for (let key in cycle) {
        if (cycle.hasOwnProperty(key)) {
          cycle[key].value = firstGrowlightTime[cycles][key];
        }
      }
    }

    // Update the secondGrowlight time schedule
    for (let cycles in secondGrowlight) {
      const cycle = secondGrowlight[cycles];
      for (let key in cycle) {
        if (cycle.hasOwnProperty(key)) {
          cycle[key].value = secondGrowlightTime[cycles][key];
        }
      }
    }

    // Update the switches condition
    for (let switches in growlightSwitches) {
      if (growlightSwitches.hasOwnProperty(switches)) {
        growlightSwitches[switches].checked = switchesData[switches];
      }
    }

    // Update the growlight mode
    growlightControlMode.checked = growlightMode;
    isGrowlightAuto = growlightMode;
    updateStyles();
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}
