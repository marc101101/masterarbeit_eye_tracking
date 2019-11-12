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
        "data":{},
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
