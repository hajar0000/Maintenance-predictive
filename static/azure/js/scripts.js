function fetchTelemetryData(machineId, callback) {
    const endpoint = `http://127.0.0.1:8000/azure/telemetries/?machine_id=${machineId}`;
    console.log('Fetching data from:', endpoint);  // Debug log to ensure correct URL is used
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            console.log('Fetched data:', data);  // Log response data to verify the correct machine's data is fetched
            if (data && data.results) {
                callback(data.results);  // Pass the filtered data to the callback
            } else {
                console.error('Data format is incorrect or empty:', data);
            }
        })
        .catch(error => console.error('Error fetching telemetry data:', error));
}


function renderTelemetryData(telemetries) {
    const times = [];
    const voltData = [];
    const rotateData = [];
    const pressureData = [];
    const vibrationData = [];

    // Process telemetry data and populate arrays for the chart
    telemetries.forEach(telemetry => {
        times.push(telemetry.datetime);  // Use the datetime field
        voltData.push(telemetry.volt);   // Use volt field
        rotateData.push(telemetry.rotate); // Use rotate field
        pressureData.push(telemetry.pressure); // Use pressure field
        vibrationData.push(telemetry.vibration); // Use vibration field
    });

    console.log('Prepared chart data:', { times, voltData, rotateData, pressureData, vibrationData });

    // Render charts (as before)
    const voltChart = echarts.init(document.getElementById('volt-chart'));
    const rotateChart = echarts.init(document.getElementById('rotate-chart'));
    const pressureChart = echarts.init(document.getElementById('pressure-chart'));
    const vibrationChart = echarts.init(document.getElementById('vibration-chart'));


    voltChart.setOption({
        title: {
            text: 'Voltage over Time',
            textStyle: {
                fontSize: 11 // Adjust this value as needed
            }
        },
        tooltip: {
            trigger: 'axis',
            textStyle: {
                fontSize: 8  // Adjust as needed
            }
        },
        xAxis: {
            type: 'category',
            data: times,
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            }
        },
        yAxis: {
            type: 'value',
            name: 'Voltage',
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            },
            nameTextStyle: {
                fontSize: 8  // Taille de la police du nom de l'axe y
            }
        },
        series: [{ name: 'Voltage', type: 'line', data: voltData }],
    });
    
    rotateChart.setOption({
        title: {
            text: 'Rotation over Time',
            textStyle: {
                fontSize: 11 // Adjust this value as needed
            }
        },
        tooltip: {
            trigger: 'axis',
            textStyle: {
                fontSize: 8  // Adjust as needed
            }
        },
        xAxis: {
            type: 'category',
            data: times,
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            }
        },
        yAxis: {
            type: 'value',
            name: 'Rotation',
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            },
            nameTextStyle: {
                fontSize: 8  // Taille de la police du nom de l'axe y
            }
        },
        series: [{ name: 'Rotation', type: 'line', data: rotateData }],
    });
    
    pressureChart.setOption({
        title: {
            text: 'Pressure over Time',
            textStyle: {
                fontSize: 11 // Adjust this value as needed
            }
        },
        tooltip: {
            trigger: 'axis',
            textStyle: {
                fontSize: 8  // Adjust as needed
            }
        },
        xAxis: {
            type: 'category',
            data: times,
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            }
        },
        yAxis: {
            type: 'value',
            name: 'Pressure',
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            },
            nameTextStyle: {
                fontSize: 8  // Taille de la police du nom de l'axe y
            }
        },
        series: [{ name: 'Pressure', type: 'line', data: pressureData }],
    });
    
    vibrationChart.setOption({
        title: {
            text: 'Vibration over Time',
            textStyle: {
                fontSize: 11 // Adjust this value as needed
            }
        },
        tooltip: {
            trigger: 'axis',
            textStyle: {
                fontSize: 8  // Adjust as needed
            }
        },
        xAxis: {
            type: 'category',
            data: times,
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            }
        },
        yAxis: {
            type: 'value',
            name: 'Vibration',
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            },
            nameTextStyle: {
                fontSize: 8  // Taille de la police du nom de l'axe y
            }
        },
        series: [{ name: 'Vibration', type: 'line', data: vibrationData }],
    });
}    

function fetcherrorData(machineId, callback) {
    fetch(`http://127.0.0.1:8000/azure/errors/${machineId}/count/`)
        .then(response => response.json())
        .then(data => {
            if (data && Array.isArray(data)) {
                callback(data);
            } else {
                console.error('Invalid data received:', data);
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}
function fetchMaintenanceData(machineId, callback) {
    fetch(`http://127.0.0.1:8000/azure/maintenances/${machineId}/count/`)
        .then(response => response.json())
        .then(data => {
            if (data && Array.isArray(data)) {
                callback(data);
            } else {
                console.error('Invalid data received:', data);
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}
// Fetch data and render chart
function fetchFailureDistribution(machineId) {
    fetch(`http://127.0.0.1:8000/azure/failure-distribution/?machine_id=${machineId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.failures) {
                renderChart(data);
                renderDistributionScores(data.distributions);
            } else {
                console.error('No failure data found:', data);
            }
        })
        .catch(error => console.error('Error fetching failure distribution data:', error));
}

function updateGraphs() {
    const machineId = document.getElementById('machine-id').value;  // Récupérer l’ID de la machine
    if (machineId) {
        fetchTelemetryData(machineId, renderTelemetryData);
        fetcherrorData(machineId, rendererrorData);
        fetchMaintenanceData(machineId, renderMaintenanceData); // Appel pour les maintenances
        fetchFailureDistribution(machineId);
    } else {
        alert('Please enter a machine ID');
    }
}

// Function to render chart
function renderChart(data) {
    const chartDom = document.getElementById('graph8-chart');
    const myChart = echarts.init(chartDom);
    
    const scatterData = data.failures.map(f => {
        const date = new Date(f.datetime);
        let failureType;

        switch (f.failure) {
            case 'comp1': failureType = 'comp1'; break;
            case 'comp2': failureType = 'comp2'; break;
            case 'comp3': failureType = 'comp3'; break;
            case 'comp4': failureType = 'comp4'; break;
            default: failureType = 'Unknown';
        }

        return [date, failureType];
    });

    const option = {
        title: {
            text: 'Distribution des pannes',
            textStyle: {
                fontSize: 11 // Adjust this value as needed
            }
        },
        tooltip: {
            position: 'top',
            formatter: function (params) {
                return `${params.value[0].toLocaleDateString()} - ${params.value[1]}`;
            },
            nameTextStyle: {
                fontSize: 8  // Taille de la police du nom de l'axe y
            }

        },
        grid: {
            left: '3%',
            bottom: '3%',
            right: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'time',
            name: 'Date',
            splitLine: {
                show: true
            },
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            },
        },
        yAxis: {
            type: 'category',
            name: 'Type de Panne',
            data: ['comp1', 'comp2', 'comp3', 'comp4'],
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            },
            nameTextStyle: {
                fontSize: 8  // Taille de la police du nom de l'axe y
            }
        },
        series: [
            {
                name: 'Pannes',
                type: 'scatter',
                symbolSize: 20,
                data: scatterData,
                animationDelay: function (idx) {
                    return idx * 5;
                }
            }
        ]
    };

    myChart.setOption(option);
}

// Function to render distribution scores
function renderDistributionScores(distributions) {
    const scoresContainer = document.getElementById('distribution-scores');
    scoresContainer.innerHTML = distributions.map(d => `${d.name} (p-value = ${d.p_value.toFixed(4)})`).join('<br>');
}

// Function to render the telemetry data using ECharts
function rendererrorData(data) {
    const errorTypes = data.map(item => item.errorID);
    const counts = data.map(item => item.count);

    const chart = echarts.init(document.getElementById('graph5-chart'));
    const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          nameTextStyle: {
            fontSize: 8  // Taille de la police du nom de l'axe y
          }
        },
        title: {
            text: 'Error Count by Type',
            textStyle: {
                fontSize: 11 // Adjust this value as needed
            }
        },
        xAxis: {
            type: 'category',
            data: errorTypes,
            name: 'Error Type',
            nameTextStyle: {
                fontSize: 8
            },
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            },
        },
        yAxis: {
            type: 'value',
            name: 'Count',
            nameTextStyle: {
                fontSize: 8
            },
            axisLabel: {
                textStyle: {
                    fontSize: 8  // Adjust as needed
                }
            },
            nameTextStyle: {
                fontSize: 8  // Taille de la police du nom de l'axe y
            }
        },
        series: [{
            type: 'bar',
            data: counts,
            label: {
                show: true,
                position: 'top',
                formatter: '{c}'
            }
        }]
    };
    chart.setOption(option);
}

function renderMaintenanceData(data) {
    const components = data.map(item => item.comp); // Récupérer les noms des composants
    const counts = data.map(item => item.count);   // Récupérer les nombres de maintenances

    const chart = echarts.init(document.getElementById('graph6-chart'));
    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)', // Amélioration du format de tooltip
            nameTextStyle: {
                fontSize: 8  // Taille de la police du nom de l'axe y
            }
        },
        title: {
            text: 'Maintenance Count by Type',
            textStyle: {
                fontSize: 11 // Adjust this value as needed
            }
        },
        legend: {
            top: '5%',
            left: 'center',
            itemWidth: 10, // Taille des icônes dans la légende
            itemHeight: 10,
            textStyle: {
                fontSize: 10 // Taille du texte dans la légende
            }
        },
        series: [
            {
                name: 'Maintenance Count',
                type: 'pie',
                radius: ['40%', '70%'], // Épaisseur du donut
                center: ['50%', '70%'], // Centrage vertical
                startAngle: 180, // Demi-donut
                endAngle: 360,
                data: components.map((comp, index) => ({
                    value: counts[index],
                    name: comp
                })),
                label: {
                    show: true,
                    formatter: '{b}\n{c}', // Afficher le composant et la valeur
                    fontSize: 10,          // Taille des étiquettes
                    position: 'outside',
                    alignTo: 'edge' // Alignement pour éviter les chevauchements
                },
                labelLine: {
                    length: 10, // Longueur de la ligne reliant l'étiquette au segment
                    length2: 10
                }
            }
        ]
    };
    chart.setOption(option);
}

