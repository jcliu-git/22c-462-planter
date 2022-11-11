//Connect to database
/*const { Client } = require('pg');

const client = new Client({
  host : 'ec2-44-209-57-4.compute-1.amazonaws.com',
  port : 5432,
  user : 'wzgfnyeewdbzlx',
  password : '68b169eefd466125c85c00c9bf7a28c2a4137ea409591093a62b680eb20af23e',
  database : 'da41gg09sivbgs',
  ssl: {
    rejectUnauthorized: false
  }
});

client.connect(function(err) {
    if(err) return;
    console.log("Connected to db :)");  
});*/

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
    $.getJSON($SCRIPT_ROOT + '/_data',(data)=>{
        if (config.data.labels.length === 24) { //only shows 24 data points at a time
            config.data.labels.shift();
            config.data.datasets[0].data.shift();
        }
        config.data.labels.push(data.result.timestamp);
        config.data.datasets[0].data.push(data.result.value);
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


