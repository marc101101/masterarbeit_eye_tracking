import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable } from 'rxjs';
import { map } from "rxjs/operators";

@Injectable()
export class WebsocketService {

    constructor(private socket: Socket) { }
 
    public getMessage(): Observable<any> {
        return this.socket.fromEvent("event").pipe(map( data => data ));
    } 

}