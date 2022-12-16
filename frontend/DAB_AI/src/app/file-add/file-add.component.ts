import { Component, ElementRef, OnInit,ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RestService, TranscriptData, TextData } from '../rest.service';
import { ImageCroppedEvent, LoadedImage } from 'ngx-image-cropper';

@Component({
  selector: 'app-file-add',
  templateUrl: './file-add.component.html',
  styleUrls: ['./file-add.component.css']
})
export class FileAddComponent implements OnInit {


  @ViewChild('canvas', {static: true}) myCanvas!: ElementRef;
  
  transcriptData = {} as TranscriptData;
  textData = {} as TextData;
  textDataList: TextData[] = [];
  file: File | null = null;
  file_edited: File | null = null;
  imageChangedEvent: any = '';
  croppedImage: any = '';
  colorList = ["#ff0000","#00ff00","#0000ff","#ffff00","#ff00ff","#00ffff"]
  
  loadedImage = {} as LoadedImage
  color = "#f00fff";
  url = "";
  url_edited = "";
  answerText = "Waiting for the introduction of the file";

  

  constructor(public rest: RestService,private route: ActivatedRoute ,private router: Router) { }

  ngOnInit(): void {
    const canvas: HTMLCanvasElement = this.myCanvas.nativeElement;
    const context = canvas.getContext("2d");
    if(context){
      this.drawRectangle(context);
      // context.drawImage(this.url, 20, 20); 
    }
  }

  onFilechange(event: any) {
    console.log(event.target.files[0])
    //display img
    
    this.loadedImage = event.target.files[0]
    var reader = new FileReader();

    // const canvas: HTMLCanvasElement = this.myCanvas.nativeElement;
    // const context = canvas.getContext("2d");
    // if(context){
    //   var img = new Image();
    //   img.onload = function() {
    //     canvas.width = img.width;
    //     canvas.height = img.height;
    //     context.drawImage(img,0,0)
    //   }
      
    // }
    

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
        //console.log(resp);
        this.transcriptData = resp
        var textData = new TextData(this.transcriptData.content, '#ffff00');
        this.textDataList.push(textData)
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

  drawRectangle(context: CanvasRenderingContext2D){
    // (x, y, width, height)
    context.strokeStyle = "green";
    context.strokeRect(20,20,100,100);
    context.strokeStyle = "red";
    context.strokeRect(120,120,100,100);
    
    
  }
 
    
  

}

