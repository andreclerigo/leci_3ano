import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators,  ValidationErrors, ValidatorFn, AbstractControl, FormBuilder } from '@angular/forms';
import { DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';
import { MomentDateAdapter } from '@angular/material-moment-adapter';
import * as _moment from 'moment';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { LoginComponent } from '../login/login.component';
import { SharedService } from '../shared.service';
import { MatSnackBar } from '@angular/material/snack-bar';
const moment = _moment;

export const DATE_FORMAT = {
  parse: {
      dateInput: ['DD-MM-YYYY', 'DD/MM/YYYY']
  },
  display: {
      dateInput: 'DD-MM-YYYY',
      monthYearLabel: 'YYYY',
      dateA11yLabel: 'LL',
      monthYearA11yLabel: 'YYYY'
  }
};
@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
  providers: [
    { provide: MAT_DATE_LOCALE, useValue: 'en-GB' },
    { provide: DateAdapter, useClass: MomentDateAdapter, deps: [MAT_DATE_LOCALE] },
    { provide: MAT_DATE_FORMATS, useValue: DATE_FORMAT },
  ]
})
export class RegisterComponent implements OnInit {
  hide: boolean = true;
  hide_confirm: boolean = true;
  minPw: number = 8;
  form!: FormGroup;

  constructor(private _formBuilder: FormBuilder,
    private _service: SharedService,
    private _snackBar: MatSnackBar,
    public dialog: MatDialog,
    private dialogRef: MatDialogRef<RegisterComponent>
  ) { }

  ngOnInit(): void {
    this.form = this._formBuilder.group({
      fname: new FormControl('', [Validators.required]),
      lname: new FormControl('', [Validators.required]),
      email: new FormControl('', [Validators.required, Validators.email]),
      password: ['', [Validators.required, Validators.minLength(this.minPw)]],
      password2: ['', [Validators.required]],
      company: new FormControl(false),
      nif: new FormControl(''),
    }, {validator: [passwordMatchValidator, nifMatchValidator]});
  }

  /* Shorthands for form controls (used from within template) */
  get password() { return this.form.get('password'); }
  get password2() { return this.form.get('password2'); }
  get nif() { return this.form.get('nif'); }
  get company() { return this.form.get('company'); }

  /* Called on each input in either password field */
  onPasswordInput() {
    if (this.form.hasError('passwordMismatch'))
      this.password2?.setErrors([{'passwordMismatch': true}]);
    else
      this.password2?.setErrors(null);
  }

  onNifInput() {
    if (this.form.hasError('nifWrong'))
      this.nif?.setErrors([{'nifWrong': true}]);
    else
      this.nif?.setErrors(null);
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
    var user = {
      email: this.form.value.email,
      password: this.form.value.password,
      nif: this.form.value.nif
    }

    var result = this._service.register(user);

    if (result) {
      /* Close the Dialog */
      this.dialogRef.close();
      this._snackBar.open('Registo realizado com sucesso!', 'Fechar', { duration: 2500 });
    } else {
      this._snackBar.open('Email inserido já está registo!', 'Fechar', { duration: 2500 });
    }
    
  }

  login() {
    // Close the dialog
    this.dialogRef.close();
    const dialogRef = this.dialog.open(LoginComponent, {
      width: '20%'
    });
  }

  close() {
    this.dialogRef.close();
  }

  companyChange() {
    if (this.company?.value) {
      this.form.controls['nif'].setValidators([Validators.required]);
    } else {
      this.form.controls['nif'].clearValidators();
    }
    this.form.controls['nif'].updateValueAndValidity();
  }
}

export const passwordMatchValidator: ValidatorFn = (formGroup: AbstractControl ): ValidationErrors | null => {
  if (formGroup.get('password')?.value === formGroup.get('password2')?.value)
    return null;
  else
    return {passwordMismatch: true};
};

export const nifMatchValidator: ValidatorFn = (formGroup: AbstractControl ): ValidationErrors | null => {
  var nif = formGroup.get('nif')?.value;

  console.log(formGroup.get('nif')?.status);

  if (formGroup.get('nif')?.status == 'VALID') {
    if (nif.length == 9 && !isNaN(Number(nif)) && Number(nif.substring(0, 3)) >= 500 && Number(nif.substring(0, 3)) <= 599) {
      console.log('aqui')
      return null;
    } else {
      return {nifWrong: true};
    }
  } else {
    return {nifWrong: true};
  }
};
