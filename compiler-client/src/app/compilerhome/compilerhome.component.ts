import { Component, OnInit } from '@angular/core';
import { CompilerService } from '../api/compiler.service';

@Component({
  selector: 'app-compilerhome',
  templateUrl: './compilerhome.component.html',
  styleUrls: ['./compilerhome.component.scss']
})
export class CompilerhomeComponent implements OnInit {

  constructor(private compilerService: CompilerService) {

  }

  codecontain: any;
  outputcode: any;

  ngOnInit(): void {
  }

  submitCode() {
    console.log(this.codecontain);
    this.compilerService.compilecode(this.codecontain)
      .then(_ => _.subscribe(
        result => {
          this.outputcode = result;
        }
      ))
  }

}
