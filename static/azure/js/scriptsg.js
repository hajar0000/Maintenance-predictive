document.addEventListener('DOMContentLoaded', (event) => {
    console.log("Page loaded");

    const predictionsEndpoint = `http://127.0.0.1:8000/azure/predictions/`;
    console.log('Fetching predictions from:', predictionsEndpoint);
    
    fetch(predictionsEndpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched predictions data:', data);
            const predictionsTableBody = document.getElementById('predictions-table-body');

            if (data.predictions) {
                data.predictions.forEach(prediction => {
                    const row = document.createElement('tr');
                    const cellMachineId = document.createElement('td');
                    const cellTimeToFail = document.createElement('td');

                    cellMachineId.innerText = prediction.machine_id;
                    cellTimeToFail.innerText = prediction.seconds_to_fail;

                    row.appendChild(cellMachineId);
                    row.appendChild(cellTimeToFail);

                    predictionsTableBody.appendChild(row);

                    console.log(`Machine ID: ${prediction.machine_id}, Time to Fail: ${prediction.seconds_to_fail}`);
                    console.log(`Time Step: ${JSON.stringify(prediction.time_step)}`);
                    console.log(`Normalized Data: ${prediction.normalized_data}`);
                });
            } else if (data.error) {
                console.error('Error in fetched predictions data:', data.error);
            }
        })
        .catch(error => console.error('Error fetching predictions data:', error));
});

document.addEventListener('DOMContentLoaded', (event) => {
    console.log("Page loaded");

    const errorsEndpoint = `http://127.0.0.1:8000/azure/errors_today/`;
    console.log('Fetching errors from:', errorsEndpoint);

    fetch(errorsEndpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched errors data:', data);
            const errorsContainer = document.getElementById('errors-container');

            if (data.errors_today.length > 0) {
                data.errors_today.forEach(error => {
                    const alertIcon = document.createElement('span');
                    alertIcon.className = 'alert-icon';
                    alertIcon.innerHTML = '&#9888;'; // Unicode for warning sign

                    const errorDetails = document.createElement('p');
                    errorDetails.innerHTML = `Machine ID: ${error.machine_id}, Timestamp: ${error.timestamp}, Error ID: ${error.error_id}`;

                    const errorItem = document.createElement('div');
                    errorItem.appendChild(alertIcon);
                    errorItem.appendChild(errorDetails);
                    errorsContainer.appendChild(errorItem);
                });
            } else {
                const noErrorsMessage = document.createElement('p');
                noErrorsMessage.innerHTML = 'Aucune erreur aujourd\'hui';
                errorsContainer.appendChild(noErrorsMessage);
            }
        })
        .catch(error => console.error('Error fetching errors data:', error));
});
document.addEventListener('DOMContentLoaded', (event) => {
    console.log("Page loaded");

    const mtbfEndpoint = `http://127.0.0.1:8000/azure/mtbf/`;
    console.log('Fetching MTBF data from:', mtbfEndpoint);

    fetch(mtbfEndpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched MTBF data:', data);
            const mtbfTableBody = document.getElementById('mtbf-table-body');

            if (data.mtbf.length > 0) {
                data.mtbf.forEach(item => {
                    const row = document.createElement('tr');
                    const cellMachineId = document.createElement('td');
                    const cellMTBF = document.createElement('td');
                    const cellFailureRate = document.createElement('td');
                    const cellReliability = document.createElement('td');

                    cellMachineId.innerText = item.machine_id;
                    cellMTBF.innerText = item.mtbf.toFixed(2); // Formatting MTBF to 2 decimal places
                    cellFailureRate.innerText = item.failure_rate.toFixed(5); // Formatting Failure Rate to 5 decimal places
                    cellReliability.innerText = item.reliability.toFixed(5); // Formatting Reliability to 5 decimal places

                    row.appendChild(cellMachineId);
                    row.appendChild(cellMTBF);
                    row.appendChild(cellFailureRate);
                    row.appendChild(cellReliability);
                    mtbfTableBody.appendChild(row);
                });
            } else {
                const noDataMessage = document.createElement('tr');
                const noDataCell = document.createElement('td');
                noDataCell.colSpan = 4;
                noDataCell.innerText = 'Aucune donnée disponible';
                noDataMessage.appendChild(noDataCell);
                mtbfTableBody.appendChild(noDataMessage);
            }
        })
        .catch(error => console.error('Error fetching MTBF data:', error));
});
