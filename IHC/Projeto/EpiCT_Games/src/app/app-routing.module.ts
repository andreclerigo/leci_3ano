import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CheckoutComponent } from './checkout/checkout.component';
import { HomeComponent } from './home/home.component';
import { ShowCartComponent } from './show-cart/show-cart.component';
import { ShowProductComponent } from './show-product/show-product.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'product', component: ShowProductComponent },
  { path: 'cart', component: ShowCartComponent },
  { path: 'checkout', component: CheckoutComponent },
  { path: '',   redirectTo: '/home', pathMatch: 'full' },   /* Default routing to HomeComponent */
  //{ path: '**' , component: PageNotFoundComponent }         /* 404 not found will be redirected to PageNotFoundComponent */
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
