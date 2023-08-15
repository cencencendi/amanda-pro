// All variables are stored here
const whatWillInclude = {
  ec: document.getElementById('include-ec'),
  do: document.getElementById('include-do'),
  ph: document.getElementById('include-ph'),
  water_temp: document.getElementById('include-water-temp'),
  kwh: document.getElementById('include-kwh'),
  co2: document.getElementById('include-co2'),
};
const dateSelection = document.getElementById('select-date');
// Graphs
const ctx = document.getElementById('myChart').getContext('2d');
let myChart = null;
let checkedValue = null;
// End of stored variables

chartTheData();
updateDateSelection();

async function postSelectedData(event) {
  try {
    // If the date has not yet selected then return nothing
    if (dateSelection.selectedIndex == 0) {
      event.target.checked = false;
      return;
    }

    // Uncheck previous checkbox
    if (checkedValue) {
      whatWillInclude[checkedValue].checked = false;
      checkedValue = null;
    }

    // Check which checkbox is checked
    for (key in whatWillInclude) {
      if (whatWillInclude.hasOwnProperty(key) && whatWillInclude[key].checked) {
        checkedValue = key;
      }
    }

    // Which date is selected
    const selectedDate = dateSelection.options[dateSelection.selectedIndex].value;

    // Get the csrfToken (THIS IS IMPORTANT! DO NOT DELETE!)
    function getCookie(name) {
      const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
      return cookieValue ? cookieValue.pop() : '';
    }

    const csrfToken = getCookie('csrftoken');

    // Post data to django and wait for the response
    const response = await fetch('post-selected-data/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        checkedValue: checkedValue,
        selectedDate: selectedDate,
      }),
    });

    // Check if the response status indicates success
    if (!response.ok) {
      throw new Error('Request failed with status ' + response.status);
    }

    const data = await response.json();
    updateChart(data.avg_data, checkedValue, selectedDate);
  } catch (error) {
    // Handle the error here
    console.error('An error occurred:', error);
    alert('An error occurred. Please try again later.');
  }
}

// Get Date Selection data
async function getDateSelection() {
  const response = await fetch('/graph/get-date-selection/');
  const data = await response.json();
  return data;
}
// Update select date option
async function updateDateSelection() {
  const data = await getDateSelection();
  let option = `<option selected></option>`;
  data.dates.forEach((date) => {
    option += dateOptionGenerator(date);
  });
  dateSelection.innerHTML = option;
}

function dateOptionGenerator(date) {
  return `<option value="${date}">${date}</option>`;
}

function chartTheData() {
  // eslint-disable-next-line no-unused-vars
  myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        '00:00',
        '01:00',
        '02:00',
        '03:00',
        '04:00',
        '05:00',
        '06:00',
        '07:00',
        '08:00',
        '09:00',
        '10:00',
        '11:00',
        '12:00',
        '13:00',
        '14:00',
        '15:00',
        '16:00',
        '17:00',
        '18:00',
        '19:00',
        '20:00',
        '21:00',
        '22:00',
        '23:00',
      ],
      datasets: [{ data: null }],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: 'Hour',
            font: {
              weight: 'bold',
            },
          },
        },
        y: {
          title: {
            display: true,
            text: 'Value',
            font: {
              weight: 'bold',
            },
          },
          ticks: {
            callback: function (value, index, values) {
              return value.toFixed(2); // Format the value as floating-point with 2 decimal places
            },
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: true,
          text: '-',
        },
      },
    },
  });
}

function updateChart(data, checkedValue, selectedDate) {
  if (!data) {
    myChart.data.datasets = [{ data: null }];
    myChart.options.scales.y.title.text = 'Value';
    myChart.options.plugins.title.text = '-';
    myChart.update();
    return;
  }

  color = getRandomHexColor();
  const newDataset = {
    data: data,
    borderColor: color,
    backgroundColor: color,
    borderWidth: 2,
  };

  // Just for better-looking chart
  myChart.data.datasets = [newDataset];
  myChart.options.scales.y.title.text = ((checkedValue) => {
    if (checkedValue == 'ec') {
      return 'EC Value (μS/cm)';
    } else if (checkedValue == 'ph') {
      return 'pH Value';
    } else if (checkedValue == 'do') {
      return 'DO Value (mg/L)';
    } else if (checkedValue == 'kwh') {
      return 'kWh Value (kWh)';
    } else if (checkedValue == 'water_temp') {
      return 'Water Temperature Value (°C)';
    } else if (checkedValue == 'co2') {
      return 'CO2 Value (ppm)';
    } else {
      return 'Value';
    }
  })(checkedValue);
  myChart.options.plugins.title.text = `Hourly Average ${checkedValue} Value on ${selectedDate}`;
  myChart.update();
}

function getRandomHexColor() {
  // Generate a random hexadecimal color code
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
