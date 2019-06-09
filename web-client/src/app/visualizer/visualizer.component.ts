import {
  Component,
  OnInit,
  ElementRef,
  ViewChild
} from '@angular/core';

declare var require: any

var chartJs = require('chart.js');

@Component({
  selector: 'app-visualizer',
  templateUrl: './visualizer.component.html',
  styleUrls: ['./visualizer.component.css']
})
export class VisualizerComponent implements OnInit {

  @ViewChild("graphCanvas") graphCanvas: ElementRef;

  constructor() {}

  file: any;
  data: any;
  data_available = false;
  keys;
  selectedValue = "frame";
  chart;
  clients = [
    {
      name: "cam_1", 
      color: "rgb(220,20,60)"
    },
    {
      name: "cam_2", 
      color: "rgb(141, 192, 0)"
    },
    {
      name: "cam_3", 
      color: "rgb(141, 120, 251)"
    },
    {
      name: "cam_4", 
      color: "rgb(232, 235, 0)"
    },
  ]


  fileChanged(e) {
    this.file = e.target.files[0];
    this.uploadDocument(this.file);
  }

  uploadDocument(file) {
    let fileReader = new FileReader();
    fileReader.onload = (e) => {
      this.data = this.csvJSON(fileReader.result);
      this.keys = Object.keys(this.data[0]);      
      this.initVisualization();
    }
    fileReader.readAsText(this.file);
  }

  changed(e){
    // event comes as parameter, you'll have to find selectedData manually
    // by using e.target.data
    this.chart.destroy();
    this.initMainGraph(this.parseData(this.selectedValue));
  } 


  csvJSON(csv){

    var lines=csv.split("\n");
  
    var result = [];
  
    var headers=lines[0].split(",");
  
    for(var i=1;i<lines.length;i++){
  
      var obj = {};
      var currentline=lines[i].split(",");
  
      for(var j=0;j<headers.length;j++){
        obj[headers[j]] = currentline[j];
      }
  
      result.push(obj);
  
    }
    
    //return result; //JavaScript object
    return result; //JSON
  }

  initVisualization(){
    this.data_available = true;
    this.initMainGraph(this.parseData(this.selectedValue));
  }

  parseData(value){
    let retVal = [];
  
    this.clients.forEach(element => {      
        retVal.push( {
          label: element.name,
          data: this.createDataRow(element.name, value),
          type: 'line',
          borderColor: element.color,
          pointRadius: 0,
          fill: false,
          lineTension: 0,
          borderWidth: 2
        });
    });

    return retVal; 
  }

  createDataRow(client, value){
    let retVal = [];
    this.data.forEach(element => { 
      console.log(element);
      
      if(element.client_id == client){    
        retVal.push({
          't': parseInt(element['server_timestamp'])*1000,
          'y': parseFloat(element[value])
        });
      }
    });
    return retVal;
  }

  initMainGraph(parsed_data){

    let context: CanvasRenderingContext2D = this.graphCanvas.nativeElement.getContext("2d");

    this.chart = new chartJs(context, {
			type: 'bar',
			data: {
				datasets: parsed_data
			},
			options: {
				scales: {
					xAxes: [{
						type: 'time',
						distribution: 'series',
						ticks: {
							source: 'data',
							autoSkip: true
						}
					}],
					yAxes: [{
						scaleLabel: {
							display: true,
							labelString: ''
						}
					}]
				},
				tooltips: {
					intersect: false,
					mode: 'index',
					callbacks: {
						label: function(tooltipItem, myData) {
							var label = myData.datasets[tooltipItem.datasetIndex].label || '';
							if (label) {
								label += ': ';
							}
							label += parseFloat(tooltipItem.value).toFixed(2);
							return label;
						}
					}
				}
			}
		});  
  }

  ngOnInit() {
  }

}
