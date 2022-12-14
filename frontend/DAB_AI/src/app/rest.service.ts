import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable,throwError,map } from 'rxjs';


const endpoint = "http://localhost:8000/";

//Interface Image
export interface Image{
  img_name: string;
  img_url: string;
  text_data: TextData[];
}

//Interface TextData
export interface TextData{
  color: string;
  content: string;
}


@Injectable({
  providedIn: 'root'
})
export class RestService {

  constructor(private http: HttpClient) { }

  // public uploadfile(file: File) {
  //   let formParams = new FormData();
  //   formParams.append('file', file)
  //   return this.http.post('http://localhost:8000/uploadfile/', formParams)
  // }
  // public uploadfile(file: File) {
  //   let formParams = new FormData();
  //   formParams.append('file', file)
  //   return this.http.post('http://localhost:8000/uploadfile/', formParams)
  // }

  getImage(): Observable<File> {
    return this.http.get<File>('http://localhost:8000/images/20221214-091255');
  }

  public uploadfile(file: File) {
    let formParams = new FormData();
    formParams.append('file', file)
    return this.http.post<any>('http://localhost:8000/uploadfile/', formParams)
  }

}
