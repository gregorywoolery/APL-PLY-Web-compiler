import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CompilerService {
  URL = `${environment.apiURL}`;


  constructor(private http: HttpClient) { }

  async compilecode(value: any) {
    return this.http.post(`${this.URL}/compile`, value);
  }

}
