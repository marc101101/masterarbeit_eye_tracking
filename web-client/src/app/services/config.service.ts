import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '../../../node_modules/@angular/common/http';
import { Observable } from '../../../node_modules/rxjs';
import { environment } from '../../environments/environment';
import { map, catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ConfigService {

  private url: string = environment.apiUrl;

  /**
   * Authorization header with in auth.serivce requested JWT token.
   */
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json'
    })
  };

  constructor(public http: HttpClient) { }

  /**
   * Get client config
   */
  getClientConfig(): Observable<any>{
    return this.http.get(this.url + "/config", this.httpOptions).pipe(
      map((res: Response) => {
        return res;
      })
    )
  } 

  /**
   * Update client config
   */
  updateClientConfig(config): Observable<any>{
    return this.http.post(this.url + "/config", config, this.httpOptions).pipe(
      map((res: Response) => {
        return res;
      })
    )
  }  

}
