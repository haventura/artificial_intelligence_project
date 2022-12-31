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


  @ViewChild('canvas') myCanvas!: ElementRef;
  
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
  
  canvas_top: number = 0;
  canvas_left: number = 0;
  canvas_width: number = 0;
  canvas_height: number = 0;

  cropper_top: number = 0;
  cropper_left: number = 0;
  cropper_width: number = 0;
  cropper_height: number = 0;

  constructor(public rest: RestService,private route: ActivatedRoute ,private router: Router) { }

  ngOnInit(): void {
    // const canvas: HTMLCanvasElement = this.myCanvas.nativeElement;
    // const context = canvas.getContext("2d");
    // if(context){
    //   this.drawRectangle(context);
    //   // context.drawImage(this.url, 20, 20); 
    // }
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
        //console.log(resp);
        this.transcriptData = resp
        var textData = new TextData(this.transcriptData.content, '#ffff00');
        this.textDataList.push(textData)
        this.answerText = "Decoded answer:";
      })

      const cropper_element = document.getElementsByClassName("ngx-ic-cropper")[0] as HTMLElement;
      if(cropper_element){
        var x_pos: number = +cropper_element.style.left.split('px')[0];
        var y_pos: number = +cropper_element.style.top.split('px')[0];
        var width: number = +cropper_element.style.width.split('px')[0];
        var height: number = +cropper_element.style.height.split('px')[0];
        this.drawRectangleOnCanvas(x_pos, y_pos, width, height, "red")
      } 
      this.answerText = "Your file is being analysed";
    } else {
      alert("Please select a file first")
    }
  }
  
  fileChangeEvent(event: any): void { 
      this.imageChangedEvent = event; 
      console.log("hello");  
      const canvas: HTMLCanvasElement = this.myCanvas.nativeElement;
      const context = canvas.getContext("2d");
      if(context){
        context.clearRect(0, 0, canvas.width, canvas.height);
      }
  }

  imageCropped(event: ImageCroppedEvent) {
    this.croppedImage = event.base64;
  }

  imageLoaded(image: LoadedImage) {
      // show cropper
      var image_element = document.getElementsByClassName("ngx-ic-source-image")[0]
      console.log("loaded"); 
      if (image_element!=null){
        console.log("element exist"); 
        var cropper_coords = image_element.getBoundingClientRect();
        console.log(cropper_coords.top, cropper_coords.right, cropper_coords.bottom, cropper_coords.left);
        this.canvas_top = cropper_coords.top;
        this.canvas_left = cropper_coords.left;
        this.canvas_width = cropper_coords.width;
        this.canvas_height = cropper_coords.height;
      }  
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

  drawRectangleOnCanvas(x_pos: number, y_pos: number, width: number, height: number, color: string){
    // (x, y, width, height)
    const canvas: HTMLCanvasElement = this.myCanvas.nativeElement;
    if(canvas){
      const originalHeight = +canvas.style.height.split('px')[0];
      const originalWidth = +canvas.style.width.split('px')[0];
      let dimensions = this.getObjectFitSize(
        true,
        canvas.clientWidth,
        canvas.clientHeight,
        +canvas.style.width.split('px')[0],
        +canvas.style.height.split('px')[0]
      );
      const dpr = window.devicePixelRatio || 1;
      canvas.style.width = (dimensions.width * dpr).toString();
      canvas.style.height = (dimensions.height * dpr).toString();
  
      let context = canvas.getContext("2d");
      let ratio = Math.min(
        canvas.clientWidth / originalWidth,
        canvas.clientHeight / originalHeight
      );
      if(context){
        context.strokeStyle = color;
        context.scale(ratio * dpr, ratio * dpr); //adjust this!
        context.strokeRect(x_pos,y_pos,width,height);
      } 
    }
  }
  
  // adapted from: https://www.npmjs.com/package/intrinsic-scale
  getObjectFitSize(
    contains: boolean, /* true = contain, false = cover */
    containerWidth: number,
    containerHeight: number,
    width: number,
    height: number
  ) {
    var doRatio = width / height;
    var cRatio = containerWidth / containerHeight;
    var targetWidth = 0;
    var targetHeight = 0;
    var test = contains ? doRatio > cRatio : doRatio < cRatio;

    if (test) {
      targetWidth = containerWidth;
      targetHeight = targetWidth / doRatio;
    } else {
      targetHeight = containerHeight;
      targetWidth = targetHeight * doRatio;
    }

    return {
      width: targetWidth,
      height: targetHeight,
      x: (containerWidth - targetWidth) / 2,
      y: (containerHeight - targetHeight) / 2
    };
  }
}

