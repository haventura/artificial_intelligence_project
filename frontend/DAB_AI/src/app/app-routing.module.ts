import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TextComponent } from './text/text.component';

const routes: Routes = [
  {
    path: 'text',
    component: TextComponent
  },
  {
    path: '',
    redirectTo: 'text',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
