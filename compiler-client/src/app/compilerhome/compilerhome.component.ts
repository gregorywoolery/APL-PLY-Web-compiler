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
  outputcode: any = "see your output here";

  ngOnInit(): void {
  }

  submitCode() {
    let codeJson = {
      code: this.codecontain
    }

    this.compilerService.compilecode(codeJson)
      .then(_ => _.subscribe(
        result => {
          console.log(result)
          this.outputcode = result;
        }
      ))
  }

}
