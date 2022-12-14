import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RestService,Image,TextData } from '../rest.service';
import { Dimensions, ImageCroppedEvent, ImageTransform, LoadedImage, base64ToFile } from 'ngx-image-cropper';

@Component({
  selector: 'app-file-add',
  templateUrl: './file-add.component.html',
  styleUrls: ['./file-add.component.css']
})
export class FileAddComponent implements OnInit {


  file: File | null = null;
  image = {} as Image;
  color = "#f00fff";
  url = "";
  answerText = "Waiting for the introduction of the file";
  imageChangedEvent: any = '';
  croppedImage: any = '';
  canvasRotation = 0;
  transform: ImageTransform = {};
  scale = 1;
  rotation = 0;

  constructor(public rest: RestService,private route: ActivatedRoute ,private router: Router) { }

  ngOnInit(): void {

  }

  onFilechange(event: any) {
    console.log(event.target.files[0])
    this.file = event.target.files[0]
    //display img
    var reader = new FileReader();
    reader.readAsDataURL(event.target.files[0]);
    reader.onload = (event:any)=>{
      this.url=event.target.result;
    }
  }
  
  upload() {
    if (this.file) {
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
  
  // getFile(){
  //   this.rest.getImage().subscribe(
  //     data => {
  //       console.log(data);
  //       this.file = data
  //     })
  // }
  
  fileChangeEvent(event: any): void {
    this.imageChangedEvent = event;
  }
  imageCropped(event: ImageCroppedEvent) {
      this.croppedImage = event.base64;
  }
  imageLoaded() {
    throw new Error('Method not implemented.');
    }
  // imageLoaded(image: LoadedImage) {
  //     // show cropper
  // }
  cropperReady(sourceImageDimensions: Dimensions) {
    console.log('Cropper ready', sourceImageDimensions);
  }
  loadImageFailed() {
      // show message
  }
  rotateLeft() {
    this.canvasRotation--;
    this.flipAfterRotate();
  }

  rotateRight() {
      this.canvasRotation++;
      this.flipAfterRotate();
  }
  private flipAfterRotate() {
      const flippedH = this.transform.flipH;
      const flippedV = this.transform.flipV;
      this.transform = {
          ...this.transform,
          flipH: flippedV,
          flipV: flippedH
      };
  }
  flipHorizontal() {
    this.transform = {
        ...this.transform,
        flipH: !this.transform.flipH
    };
    }

  flipVertical() {
    this.transform = {
        ...this.transform,
        flipV: !this.transform.flipV
    };
  }

  resetImage() {
      this.scale = 1;
      this.rotation = 0;
      this.canvasRotation = 0;
      this.transform = {};
  }

  zoomOut() {
      this.scale -= .1;
      this.transform = {
          ...this.transform,
          scale: this.scale
      };
  }

  zoomIn() {
      this.scale += .1;
      this.transform = {
          ...this.transform,
          scale: this.scale
      };
  }
  updateRotation() {
    this.transform = {
        ...this.transform,
        rotate: this.rotation
    };
  }

}

