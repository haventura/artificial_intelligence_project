import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RestService,Image,TextData } from '../rest.service';

@Component({
  selector: 'app-file-add',
  templateUrl: './file-add.component.html',
  styleUrls: ['./file-add.component.css']
})
export class FileAddComponent implements OnInit {

  file: File | null = null;
  texts: TextData[] = [];
  images: Image[] = [];
  image = {} as Image;
  color = "#f00fff";
  url = "";
  test = "";

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
      })
      //alert("Uploaded")
    } else {
      alert("Please select a file first")
    }
  }
  





}

