import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-annotate',
  templateUrl: './annotate.component.html',
  styleUrls: ['./annotate.component.css']
})
export class AnnotateComponent implements OnInit {

  constructor() { }

  public test_frame = {
    "test_person_id": 0,
    "position": 1,
    "aoi": "A1"
  };

  public position_list = [1,2,3,4];
  public aoi_list = ["A1","A2","A3","B1","B2"];

  ngOnInit() {
  }

  start(){
    console.log("Start");
  }

  next(){
    console.log("Next");
  }

  stop(){
    console.log("Stop");
  }

}
