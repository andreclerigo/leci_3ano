import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { CreateEventComponent } from './create-event/create-event.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { SharedService } from './shared.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  filterValue: string = '';
  title: string = 'EpiCT_Games';
  cart_number: number = 0;
  loggedIn: boolean = false;
  company: boolean = false;
  subscriptionC: Subscription = new Subscription();
  subscriptionL: Subscription = new Subscription();
  subscriptionN: Subscription = new Subscription();

  constructor(private _router: Router, private _service: SharedService, public dialog: MatDialog) {
    this.subscriptionL = this._service.currentLogStatus.subscribe(logStatus => this.loggedIn = logStatus);
    this.subscriptionN = this._service.currentNif.subscribe(nif => nif ? this.company = true : this.company = false);
  }

  ngOnInit() {
    this.subscriptionC = this._service.cartOpened.subscribe((data: any) => {
      if (data == null) {
        this.cart_number = 0;
      } else {
        this.cart_number = data.length;
      }
    });
  }

  applyFilter(event: Event) {
    this.filterValue = (event.target as HTMLInputElement).value;
    this._service.setFilter(this.filterValue);
  }

  search() {
    this._router.navigate(['/']);
  }

  /* Redirect to the home page */
  redirectHome() {
    this._router.navigate(['/home']);
  }

  /* Redirect to the shopping cart page */
  redirectCart() {
    this._router.navigate(['/cart']);
  }

  /* Open Login Dialog */
  redirectLogin() {
    const dialogRef = this.dialog.open(LoginComponent, {
      width: '20%'
    });
  }

  redirectCreateEvent() {
    const dialogRef = this.dialog.open(CreateEventComponent, {
      width: '35%'
    });
  }

  /* Open Register Dialog */
  redirectRegister() {
    const dialogRef = this.dialog.open(RegisterComponent);
  }

  logout() {
    this._service.logout();
  }
}
