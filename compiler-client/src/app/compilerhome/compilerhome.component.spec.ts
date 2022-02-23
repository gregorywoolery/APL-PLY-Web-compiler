import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CompilerhomeComponent } from './compilerhome.component';

describe('CompilerhomeComponent', () => {
  let component: CompilerhomeComponent;
  let fixture: ComponentFixture<CompilerhomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CompilerhomeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CompilerhomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
