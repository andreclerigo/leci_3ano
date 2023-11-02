import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-done',
  templateUrl: './done.component.html',
  styleUrls: ['./done.component.scss']
})
export class DoneComponent implements OnInit {

  constructor(private dialogRef: MatDialogRef<DoneComponent>) { 
    setTimeout(() => {
      this.dialogRef.close();
    }, 4000);
  }

  ngOnInit(): void {
  }

}
