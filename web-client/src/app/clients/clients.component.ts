import { Component, OnInit } from '@angular/core';
import { WebsocketService } from '../services/websocket.service';
import { Observable, interval } from 'rxjs';


@Component({
  selector: 'clients',
  templateUrl: './clients.component.html',
  styleUrls: ['./clients.component.css']
})

export class ClientsComponent implements OnInit {

  constructor(public websocket: WebsocketService) { }

  public clients = {    
      "cam_1": {
        "data":{
          "raw":{
            "gaze_0_x":0.370813,
            "eye_lmk_Y_0":54.2935,
            "gaze_angle_x":0.296543,
            "pose_Rx":-0.431462,
            "pose_Tz":573.95,
            "gaze_0_y":-0.254981,
            "pose_Tx":-33.6334,
            "eye_lmk_X_0":-61.922,
            "eye_lmk_Z_1":523.172,
            "client_id":"cam_4",
            "gaze_angle_y":-0.283404,
            "eye_lmk_Y_1":59.9796,
            "pose_Ty":100.43,
            "pose_Ry":-0.33408,
            "frame":87,
            "timestamp":78.7154,
            "confidence":0.975,
            "gaze_1_z":-0.9413,
            "success":1,
            "eye_lmk_X_1":-10.2352,
            "pose_Rz":-0.045341,
            "gaze_1_x":0.189668,
            "eye_lmk_Z_0":505.21,
            "gaze_0_z":-0.893019,
            "face_id":0,
            "gaze_1_y":-0.279251
          },
          "parsed_data":[-1,-1,1]
        },
        "active": false,
        "receiveTime": 0,
        "open": false
      },
      "cam_2": {
        "data":{},
        "active": false,
        "receiveTime": 0,
        "open": false
      },
      "cam_3": {
        "data":{},
        "active": false,
        "receiveTime": 0,
        "open": false
      },
      "cam_4": {
        "data":{},
        "active": false,
        "receiveTime": 0,
        "open": false
      }
  };

  public client_keys = Object.keys(this.clients);

  public sub;

  ngOnInit() {
    this.websocket.getMessage().subscribe( message => {
      let client_id = message.raw.client_id
      this.clients[client_id].data = message;
      this.clients[client_id].active = true;
      this.clients[client_id].receiveTime = Date.now();
    });

    this.startValidator();
  }

  startValidator(){
    this.sub = interval(10000).subscribe((val) => { 
      this.client_keys.forEach(client_id => {        
        let client_reveived_last = this.clients[client_id].receiveTime;        
        if (((Date.now()) - client_reveived_last) > 10000 ){
          this.clients[client_id].active = false;
        }
      });
    });
  }

}
