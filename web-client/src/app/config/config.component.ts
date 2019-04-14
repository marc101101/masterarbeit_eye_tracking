import { Component, OnInit } from '@angular/core';
import { ConfigService } from '../services/config.service';

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
      console.log(this.config);      
    })
  }

  saveConfig(){
    this.configService.updateClientConfig(this.config).subscribe( response => {
      console.log("Success");      
    });
  }

}
