import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CompilerhomeComponent } from './compilerhome.component';

const routes: Routes = [
  {
    path: '',
    component: CompilerhomeComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class CompilerhomeComponentRoutingModule { }
