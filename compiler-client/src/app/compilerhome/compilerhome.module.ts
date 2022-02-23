import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { CompilerhomeComponent } from './compilerhome.component';
import { CompilerhomeComponentRoutingModule } from './compilerhome-routing.module';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    CompilerhomeComponentRoutingModule,
    ReactiveFormsModule
  ],
  declarations: [CompilerhomeComponent]
})
export class CompilerhomeComponentModule { }
