import { Component, HostListener } from '@angular/core';
import { AnnotateService } from '../services/annotate.service';

@Component({
  selector: 'app-annotate',
  templateUrl: './annotate.component.html',
  styleUrls: ['./annotate.component.css']
})
export class AnnotateComponent  {

  constructor(public annotateService: AnnotateService) { }

  public test_frame = {
    "test_person_id": null,
    "position": null,
    "aoi": null
  };

  public timeLeft: number = 5;
  public interval;
  public recording: boolean = false;

  public position_list: Array<Number> = [1,2,3,4,5];
  public aoi_list: Array<Number> = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29];

  @HostListener('window:keyup', ['$event'])
  keyEvent(event: KeyboardEvent) {    
    if (event.key == "ArrowRight") {
      this.next();
    }    
  }

  randomize(){
    this.position_list = this.shuffle(this.position_list);
    this.aoi_list = this.shuffle(this.aoi_list);
  }

  startTimer() {
    this.interval = setInterval(() => {
      if(this.timeLeft > 0) {
        this.timeLeft--;
      } else {
        this.pauseTimer();
      }
    },1000)
  }

  pauseTimer() {    
    clearInterval(this.interval);
    this.timeLeft = 5;
  }

  start(){
    if(!this.recording){
      this.test_frame.position = this.position_list[0];
      this.test_frame.aoi = this.aoi_list[0];

      let meta = {
        "test_person_id": this.test_frame.test_person_id,
        "position_list": this.position_list,
        "aoi_list": this.aoi_list
      };

      this.annotateService.sendMeta(meta).subscribe(res => {
        this.annotateService.annotate(this.test_frame, "start").subscribe(res => {
          console.log("Start");
          this.startTimer();
          this.recording = true;
        });
      })
    }
  }

  next(){
    this.annotateService.annotate(this.test_frame, "next").subscribe(res => {
      console.log("Next");
      console.log(Date.now());
      console.log(new Date(Date.now()));   
      this.setAoi();
      this.pauseTimer();
      this.startTimer();
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

  //src: https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
  private shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;
  
    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
  
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;
  
      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }
  
    return array;
  }
  

  private resetFrame() {
    this.test_frame.position = null;
    this.test_frame.aoi = null;
    this.pauseTimer();
  }

  private setPosition() {         
    if((this.position_list.length-1 == this.position_list.indexOf(this.test_frame.position)) && (this.aoi_list.length-1 == this.aoi_list.indexOf(this.test_frame.aoi))){
      this.stop();
    }
    else{
      if(this.position_list.length <= this.position_list.indexOf(this.test_frame.position)){
        this.test_frame.position = this.position_list[0];
        this.setPosition();
      }
      else{
        this.test_frame.position = this.position_list[this.position_list.indexOf(this.test_frame.position) + 1];
      }
    }
  }

  private setAoi(){
    if(this.aoi_list.length-1 <= this.aoi_list.indexOf(this.test_frame.aoi)){      
      this.setPosition();
      this.test_frame.aoi = this.aoi_list[0];
    }
    else{
      this.test_frame.aoi = this.aoi_list[this.aoi_list.indexOf(this.test_frame.aoi) + 1];
    }
  }


}
