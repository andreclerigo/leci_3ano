import { Country } from '@angular-material-extensions/select-country';
import { STEPPER_GLOBAL_OPTIONS } from '@angular/cdk/stepper';
import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { product, SharedService } from '../shared.service';
import { DoneComponent } from './done/done.component';

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss'],
  providers: [
    {
      provide: STEPPER_GLOBAL_OPTIONS,
      useValue: {showError: true},
    },
  ],
})
export class CheckoutComponent implements OnInit {
  infoForm!: FormGroup;
  paymentForm!: FormGroup;
  payment: string = "";
  phone_disable: boolean = true;
  company: boolean = false;

  isActive1: boolean = false;
  isActive2: boolean = false;
  isActive3: boolean = false;
  checked1: boolean = false;
  checked2: boolean = false;
  checked3: boolean = false;
 
  cart: any = [];
  subscription: Subscription = new Subscription();
  subscriptionN: Subscription = new Subscription();

  constructor(private _formBuilder: FormBuilder, public done_dialog: MatDialog, private _router: Router, private _service: SharedService) {
    this.subscription = this._service.cartOpened.subscribe((data: product[]) => {
      var cart = data;
      
      /* Get the qty of items */
      cart.forEach((element: any) => {        
        this.cart.push({ 
          title: element.title,
          key_price: element.key_price,
          price: element.price,
          type: element.type,
          event: element.event,
          qty: cart.filter((v: any) => (v.title === element.title && v.type === element.type)).length
        });
      });
      
      /* Remove duplicate values es6 magic */
      this.cart = this.cart.filter((value: any, index: any, self: any) =>
      index === self.findIndex((t: any) => (
        t.place === value.place && t.title === value.title && t.type === value.type
        ))
      );
    });

    this.subscriptionN = this._service.currentNif.subscribe(nif => nif ? this.company = true : this.company = false);
  }

  ngOnInit() {
    this.infoForm = this._formBuilder.group({
      name: ['', Validators.required],
      country: [''],
      city: ['', Validators.required],
      address: ['', Validators.required],
      post_code: ['', Validators.required],
      nif: [''],
    }, {validator: [nifValidator, postCodeValidator]});

    this.paymentForm = this._formBuilder.group({
      payment: ['', Validators.required],
      phone: [''],
    }, {validator: phoneValidator});

    if (this.company) {
      this.infoForm.controls['nif'].setValue(localStorage.getItem('nif'));
    }
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
    if (this.cart[0]?.type == 'event') this._service.openCartPage(null);
  }

  /* Shorthands for form controls (used from within template) */
  get name() { return this.infoForm.get('name') };
  get city() { return this.infoForm.get('city') };
  get address() { return this.infoForm.get('address') };
  get post_code() { return this.infoForm.get('post_code') };
  get nif() { return this.infoForm.get('nif') };
  get phone() { return this.paymentForm.get('phone') };

  /* Update validation when the phone input changes */
  onPhoneInput() {
    if (this.paymentForm.hasError('phoneWrong'))
      this.phone?.setErrors([{'phoneWrong': true}]);
    else
      this.phone?.setErrors(null);
  }

  /* Update validation when the phone input changes */
  onNifInput() {
    if (this.infoForm.hasError('nifWrong'))
      this.nif?.setErrors([{'nifWrong': true}]);
    else
      this.nif?.setErrors(null);
  }

  /* Update validation when the post code input changes */
  onPostCodeInput() {
    if (this.infoForm.hasError('postCodeWrong'))
      this.post_code?.setErrors([{'postCodeWrong': true}]);
    else
      this.post_code?.setErrors(null);
  }

  /* Set the correct checked box and the correct payment info */
  selectPayment(payment: string, event: Event) {
    event.preventDefault();
    this.payment = payment;
    this.paymentForm.get('payment')?.setValue(payment);
    
    if (payment == 'paypal') {
      if (this.checked1) {
        this.checked1 = false;
        this.paymentForm.get('payment')?.setValue(null);
      } else {
        this.checked1 = true;
      }

      this.checked2 = false;
      this.checked3 = false;
      this.paymentForm.get('phone')?.clearValidators();
    }
    if (payment == 'credit_card') {
      if (this.checked2) {
        this.checked2 = false;
        this.paymentForm.get('payment')?.setValue(null);
      } else {
        this.checked2 = true;
      }

      this.checked1 = false;
      this.checked3 = false;
      this.paymentForm.get('phone')?.clearValidators();
    }
    if (payment == 'mbway') {
      if (this.checked3) {
        this.checked3 = false;
        this.paymentForm.get('payment')?.setValue(null);
      } else {
        this.checked3 = true;
      }

      this.checked1 = false;
      this.checked2 = false;
      this.paymentForm.get('phone')?.setValidators(Validators.required);
    }

    this.paymentForm.get('phone')?.updateValueAndValidity();
  }

  checkoutDone() {
    const dialogRef = this.done_dialog.open(DoneComponent, {
      width: '40%',
      height: '40%'
    });

    dialogRef.afterClosed().subscribe(_ => {
      if (this.cart[0].type == 'event') {
        this.cart[0].event.img = '/assets/img/events/event_default.jpg';
        this._service.addEvent(this.cart[0].event);
      }
      this._router.navigate(['/']);
      this._service.openCartPage(null);
    });
  }

  productPrice(product: any) {
    if (product.type == 'key' || product.type == 'ticket' || product.type == 'event') {
      return product.key_price;
    } else {
      return product.price;
    }
  }

  productType(product: any) {
    if (product.type == 'key') return 'Chave';
    if (product.type == 'ticket') return 'Bilhete';
    if (product.type == 'CD') return 'CD-ROM';
    if (product.type == 'event') return 'Criação de evento';

    return null
  }

  totalPriceProduct(product: any) {
    var qty: number = product.qty;
    var price: string = this.productPrice(product);

    return String((qty * parseFloat(price.substring(0, price.length - 3).replace(/,/g, '.'))).toFixed(2)).replace('.', ',');
  }

  onCountryChange(c: Country) {
  }

  totalPriceCart() {
    var total = 0;
    this.cart.forEach((element: any) => {
      if (element.type == 'key' || element.type == 'ticket') {
        total += element.qty * parseFloat(element.key_price.substring(0, element.key_price.length - 3).replace(/,/g, '.'));
      }  else if(element.type == 'event') {
        total = parseFloat(element.key_price.substring(0, element.key_price.length - 3).replace(/,/g, '.'));
      }else {
        total += element.qty * parseFloat(element.price.substring(0, element.price.length - 3).replace(/,/g, '.'));
      }
    });
    return String(total.toFixed(2)).replace('.', ',');
  }
}

export const phoneValidator: ValidatorFn = (formGroup: AbstractControl ): ValidationErrors | null  => {
  var phone: string = formGroup.get('phone')?.value;

  if (phone.length == 0) return null;

  if (phone.length == 9 && !isNaN(Number(phone))) {
    return null;
  } else {
    return { phoneWrong: true };
  }
}

export const nifValidator: ValidatorFn = (formGroup: AbstractControl ): ValidationErrors | null  => {
  var nif: string = formGroup.get('nif')?.value;

  if (nif.length == 0) return null;

  if (nif.length == 9 && !isNaN(Number(nif))) {
    return null;
  } else {
    return { nifWrong: true };
  }
}

export const postCodeValidator: ValidatorFn = (formGroup: AbstractControl ): ValidationErrors | null  => {
  var post_code: string = formGroup.get('post_code')?.value.replace(/\s/g, "");
  var post_code_list = post_code.split("-");

  if (post_code_list.length == 0) return null;

  if (post_code_list.length == 2) {
    if (post_code_list[0].length == 4 && !isNaN(Number(post_code_list[0]))) {
      if (post_code_list[1].length == 3 && !isNaN(Number(post_code_list[1]))) {
        return null;
      } else {
        return { postCodeWrong: true };
      }
    } else {
      return { postCodeWrong: true };
    }
  } else {
    return { postCodeWrong: true };
  }
}
