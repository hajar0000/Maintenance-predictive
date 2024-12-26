// Example to initialize your charts (using Chart.js here as an example)
var ctx1 = document.getElementById('graph1').getContext('2d');
var graph1 = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow'],
        datasets: [{
            label: 'Dataset 1',
            data: [12, 19, 3],
            backgroundColor: ['#ff6384', '#36a2eb', '#ffcd56'],
        }]
    }
});

// Repeat for other graphs
var ctx2 = document.getElementById('graph2').getContext('2d');
var graph2 = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March'],
        datasets: [{
            label: 'Dataset 2',
            data: [10, 15, 8],
            backgroundColor: '#36a2eb',
        }]
    }
});