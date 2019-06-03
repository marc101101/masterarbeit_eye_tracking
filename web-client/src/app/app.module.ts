import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ConfigComponent } from './config/config.component';
import { HomeComponent } from './home/home.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { ConfigService } from './services/config.service';
import { HttpClientModule } from '@angular/common/http';

import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ClientsComponent } from './clients/clients.component';
import { AnnotateComponent } from './annotate/annotate.component';

import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { WebsocketService } from './services/websocket.service';

const config: SocketIoConfig = { url: 'http://localhost:5000', options: {} };

@NgModule({
  declarations: [
    AppComponent,
    ConfigComponent,
    HomeComponent,
    PageNotFoundComponent,
    ClientsComponent,
    AnnotateComponent
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    AppRoutingModule,
    FormsModule, 
    ReactiveFormsModule,
    SocketIoModule.forRoot(config)
  ],
  providers: [
    ConfigService,
    HttpClientModule,
    WebsocketService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
