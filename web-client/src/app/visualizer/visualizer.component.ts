import {
  Component,
  OnInit,
  ElementRef,
  ViewChild
} from '@angular/core';

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

  fileChanged(e) {
    this.file = e.target.files[0];
    this.uploadDocument(this.file);
  }

  uploadDocument(file) {
    let fileReader = new FileReader();
    fileReader.onload = (e) => {
      this.data = this.csvJSON(fileReader.result);
      this.initVisualization();
    }
    fileReader.readAsText(this.file);
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
    this.initMainGraph(this.parseData("pose_Rx"));
  }

  parseData(value){
    let retVal = [];
    this.data.forEach(element => {
      retVal.push({
        'x': new Date(parseInt(element.server_timestamp)),
        'y': element[value]
      });
    });
    return retVal; 
  }

  initMainGraph(parsed_data){

    console.log(parsed_data);

    let context: CanvasRenderingContext2D = this.graphCanvas.nativeElement.getContext("2d");

    new chartJs(context, {
      type: 'line',
      data: parsed_data,
      options: {
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'millisecond'
                }
            }]
        }
    }
    });  
  }

  ngOnInit() {
  }

}
