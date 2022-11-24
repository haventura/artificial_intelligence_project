import { Component, NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TextComponent } from './text/text.component';
import { MainPageComponent } from './main-page/main-page.component';
import { FileAddComponent } from './file-add/file-add.component';

const routes: Routes = [
  {
    path: 'text',
    component: TextComponent
  },
  {
    path: 'main-page',
    component: TextComponent
  },
  {
    path: 'file-add',
    component: FileAddComponent
  },
  {
    path: '',
    redirectTo: 'file-add',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
