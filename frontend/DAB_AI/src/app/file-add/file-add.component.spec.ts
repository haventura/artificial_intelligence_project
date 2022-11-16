import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FileAddComponent } from './file-add.component';

describe('FileAddComponent', () => {
  let component: FileAddComponent;
  let fixture: ComponentFixture<FileAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FileAddComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FileAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
