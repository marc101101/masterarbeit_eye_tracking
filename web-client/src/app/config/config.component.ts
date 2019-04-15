import { Component, OnInit } from '@angular/core';
import { ConfigService } from '../services/config.service';
import { Client } from '../model/client';

@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.css']
})
export class ConfigComponent implements OnInit {

  public config;

  constructor(public configService: ConfigService) { }

  ngOnInit() {
    this.configService.getClientConfig().subscribe( response => {
      this.config = response;
    })
  }

  saveConfig() {
    this.configService.updateClientConfig(this.config).subscribe(response => {
      M.toast({ html: 'Successfully saved config' });
    });
  }

  addNewClient(){
    let client_name = "cam_" + Object.keys(this.config).length + 1;
    let new_client = new Client(0, 0, 0, 0, 0, 0, 0, 0, 0);
    this.config[client_name] = new_client;
    M.toast({ html: 'Added new client' });
  }

  deleteClient(client_id){
    delete this.config[client_id];
    M.toast({ html: 'Deleted client ' + client_id });
  }

  duplicateClient(client_id){
    let client_name = "cam_" + Object.keys(this.config).length + 1;
    let new_client = this.config[client_id];
    this.config[client_name] = new_client;
    M.toast({ html: 'Duplicated client ' + client_id });
  }

}
