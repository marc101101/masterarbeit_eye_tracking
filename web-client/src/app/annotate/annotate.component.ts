import { Component, OnInit } from '@angular/core';
import { AnnotateService } from '../services/annotate.service';

@Component({
  selector: 'app-annotate',
  templateUrl: './annotate.component.html',
  styleUrls: ['./annotate.component.css']
})
export class AnnotateComponent implements OnInit {

  constructor(public annotateService: AnnotateService) { }

  public test_frame = {
    "test_person_id": 0,
    "position": 1,
    "aoi": "A1"
  };

  public recording: boolean = false;

  public position_list: Array<Number> = [1,2,3,4];
  public aoi_list: Array<string> = ["A1","A2","A3","B1","B2","B3","C1","C2","C3"];

  ngOnInit() {
  }

  start(){
    if(!this.recording){
      this.annotateService.annotate(this.test_frame, "start").subscribe(res => {
        console.log("Start");
        this.recording = true;
      });
    }
  }

  next(){
    this.annotateService.annotate(this.test_frame, "next").subscribe(res => {
      console.log("Next");    
      this.setPosition();
    });
  }

  stop(){
    if(this.recording){
      this.annotateService.annotate(this.test_frame, "stop").subscribe(res => {
        console.log("Stop");  
        this.recording = false;
        this.resetFrame();      
      });
    }
  }

  private resetFrame() {
    this.test_frame.position = 1;
    this.test_frame.aoi = "A1";
  }

  private setPosition() {    
    if((this.position_list.length == this.test_frame.position) && (this.aoi_list.length-1 == this.aoi_list.indexOf(this.test_frame.aoi))){
      this.stop();
    }
    else{
      if(this.position_list.length <= this.test_frame.position){
        this.test_frame.position = 1;
        this.setAoi();
      }
      else{
        this.test_frame.position = this.test_frame.position + 1;
      }
    }
  }

  private setAoi(){
    if(this.aoi_list.length <= this.aoi_list.indexOf(this.test_frame.aoi)){
      this.test_frame.aoi = this.aoi_list[0];
      this.setAoi();
    }
    else{
      this.test_frame.aoi = this.aoi_list[this.aoi_list.indexOf(this.test_frame.aoi) + 1];
    }
  }


}
