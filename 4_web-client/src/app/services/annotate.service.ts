import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { map, catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class AnnotateService {

  private url: string = environment.apiUrl;

  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json'
    })
  };

  constructor(public http: HttpClient) { }

  sendMeta(meta_data): Observable<any>{
    return this.http.post(this.url + "/meta/", meta_data, this.httpOptions).pipe(
      map((res: Response) => {
        return res;
      })
    )
  } 

  annotate(test_frame, method:string): Observable<any>{
    return this.http.post(this.url + "/annotate/" + method, test_frame, this.httpOptions).pipe(
      map((res: Response) => {
        return res;
      })
    )
  } 
}