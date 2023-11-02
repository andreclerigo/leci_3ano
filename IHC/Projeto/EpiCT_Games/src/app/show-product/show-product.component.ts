import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { product, SharedService } from '../shared.service';
import { FormGroup, FormControl, Validators,  ValidationErrors, ValidatorFn, AbstractControl, FormBuilder } from '@angular/forms';


@Component({
  selector: 'app-show-product',
  templateUrl: './show-product.component.html',
  styleUrls: ['./show-product.component.scss']
})
export class ShowProductComponent implements OnInit {
  product!: product;
  subscription : Subscription = new Subscription();
  filledStar : number = 0;
  halfStar: boolean = false;
  emptyStar: number = 0;
  form!: FormGroup;

  constructor(private _formBuilder: FormBuilder,private _service: SharedService) {
    this.subscription = this._service.productOpened.subscribe((data: product) => {
      this.product = data;
    });
  }

  ngOnInit(): void {
    console.log(this.product);
    this.calculateRate();
    this.form = this._formBuilder.group({
      msg: new FormControl('', [Validators.required]),    
    });
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
  
  calculateRate(){
    this.filledStar = Math.floor(this.product?.rating);
    this.halfStar = this.product?.rating - this.filledStar > 0;
    this.emptyStar = 5 - this.filledStar - (this.halfStar ? 1 : 0);
  }

  refreshProducts(){
    this.subscription = this._service.productOpened.subscribe((data: product) => {
      this.product = data;
    });
    console.log(this.product);
  }

  addCartKey() {
    var data: any = this.product;
    data.type = 'key';
    this._service.openCartPage(data);
  }

  addCartCD() {
    var data: any = this.product;
    data.type = 'CD';
    this._service.openCartPage(data);
  }

  platforms(product: product) {
    return product.platform.map(platform => platform).join(', ');
  }

  categories(product: product) {
    return product.categories.map(category => category).join(', ');
  }

  addComment(){
    console.log("comentario");
    var products: product[] = this._service.getProducts();

    console.log(products.find((p: product) => p.title == this.product?.title)!.comments.push(this.form.get('msg')?.value))
    console.log(products);
    localStorage.setItem('products', JSON.stringify(
      products
    ));
    console.log(JSON.parse(localStorage.getItem('products')!));
  }
}
