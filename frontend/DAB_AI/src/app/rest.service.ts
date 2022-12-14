import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable,throwError,map } from 'rxjs';


const endpoint = "http://localhost:8000/";

//Interface TextData
export interface TranscriptData{
  content: string;
}

export class TextData{
  Content: string;
  Color: string;
  constructor(public content: string, public color: string) { 
    this.Color = color;
    this.Content = content;
  }
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

  // getImage(): Observable<Image> {
  //   return this.http.post<Image>(endpoint + 'uploadfile/');
  // }

  public uploadfile(file: File) {
    let formParams = new FormData();
    formParams.append('file', file)
    return this.http.post<any>('http://localhost:8000/uploadfile/', formParams)
  }

}
