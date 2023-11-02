import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { RegisterComponent } from '../register/register.component';
import { SharedService } from '../shared.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  hide: boolean = true;

  form: FormGroup = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required])
  });
  
  constructor(private _snackBar: MatSnackBar, private _service: SharedService, public dialog: MatDialog, private dialogRef: MatDialogRef<LoginComponent>) { }

  ngOnInit(): void {
  }

  /* Error Message for Email validation */
  getErrorMessageEmail() {
    if (this.form.controls['email'].hasError('required')) {
      return 'Você deve inserir um email';
    }

    return this.form.controls['email'].hasError('email') ? 'Email não é válido' : '';
  }

  /* Submit form action */
  submit() {
    /* Only submit if the form is valid */
    if (this.form.valid) {
      var result = this._service.login(this.form.get('email')!.value, this.form.get('password')!.value);

      if (result) {
        /* Close the Dialog */
        this.dialogRef.close();
        this._snackBar.open('Login realizado com sucesso!', 'Fechar', { duration: 2500 });
      } else {
        this._snackBar.open('Email ou senha incorretos!', 'Fechar', { duration: 2500 });
      }
    } 
  }

  close() {
    this.dialogRef.close();
  }

  register() {
    /* Close the Dialog */
    this.dialogRef.close();
    const dialogRef = this.dialog.open(RegisterComponent);
  }
}
