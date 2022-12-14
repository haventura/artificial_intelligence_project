import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RestService,Image,TextData } from '../rest.service';
import { ImageCroppedEvent, LoadedImage } from 'ngx-image-cropper';

@Component({
  selector: 'app-file-add',
  templateUrl: './file-add.component.html',
  styleUrls: ['./file-add.component.css']
})
export class FileAddComponent implements OnInit {

  file: File | null = null;
  imageChangedEvent: any = '';
  croppedImage: any = '';
  image = {} as Image;
  loadedImage = {} as LoadedImage
  color = "#f00fff";
  url = "";
  answerText = "Waiting for the introduction of the file";

  constructor(public rest: RestService,private route: ActivatedRoute ,private router: Router) { }

  ngOnInit(): void {

  }

  onFilechange(event: any) {
    console.log(event.target.files[0])
    //display img
    this.loadedImage = event.target.files[0]
    var reader = new FileReader();
    reader.readAsDataURL(event.target.files[0]);
    reader.onload = (event:any)=>{
      this.url=event.target.result;
    }
  }
  
  upload() {
    
    if (this.croppedImage) {
      this.file = this.dataURLtoFile(this.croppedImage, 'filename')
      this.rest.uploadfile(this.file).subscribe((resp) => {
        //Code will execute when back-end will respond
        console.log(resp),
        this.image = resp;
        this.answerText = "Decode answer :";
      })
      //alert("Uploaded")
      this.answerText = "Your file is being analysed";
    } else {
      alert("Please select a file first")
    }
  }
  

  fileChangeEvent(event: any): void {
      this.imageChangedEvent = event;
  }
  imageCropped(event: ImageCroppedEvent) {
      this.croppedImage = event.base64;
  }
  imageLoaded(image: LoadedImage) {
      // show cropper
  }
  cropperReady() {
      // cropper ready
  }
  loadImageFailed() {
      // show message
  }
  dataURLtoFile(dataurl: any, filename: string) {
 
    var arr = dataurl.split(','),
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), 
        n = bstr.length, 
        u8arr = new Uint8Array(n);
        
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    
    return new File([u8arr], filename, {type:mime});
  }
}

