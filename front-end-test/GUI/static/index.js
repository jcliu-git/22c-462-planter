const config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: "Moisture Level",
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [],
            fill: false,
        }],
    },
    options: {
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Time'
                }
                }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        }
    }
};

var moisture_chart;

function addToChart(i){
    $.getJSON('/_data',(data)=>{
        if (config.data.labels.length === 24) { //only shows 24 data points at a time
            config.data.labels.shift();
            config.data.datasets[0].data.shift();
        }
        console.log(data);
        config.data.labels.push(data[1]);
        config.data.datasets[0].data.push(data[2]);
        moisture_chart.update();
    });
}

var i=1;
setInterval(()=>{
    addToChart(i.toString());
    i+=1;
},1000) //every one second 

$(document).ready(function () {
    moisture_chart = new Chart("moisture_chart",config);    
    addToChart(i.toString());
    i+=1;
});


