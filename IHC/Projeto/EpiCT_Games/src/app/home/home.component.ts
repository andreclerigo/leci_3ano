import { Component, Input, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn } from '@angular/forms';
import { Subscription } from 'rxjs';
import { product,event, SharedService } from '../shared.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  filterValue: any;
  all_products: product[] = [];
  products!: product[];
  events!: event[];

  subscription: Subscription = new Subscription();
  categories_expanded: boolean = false;

  filtros: FormGroup;
  categorias: FormGroup;
  pegi: FormGroup;
  priceRange: FormGroup;

  all_marketplaces: string[] = ['Steam', 'Origin', 'Epic Games', 'EA', 'Battlenet', 'Playstation', 'Xbox', 'Nintendo'];
  all_categories: string[] = ['Ação', 'Aventura', 'FPS', 'RPG', 'Estratégia', 'Battle Royale', 'Desporto', 'MMO', 'Corridas', 'Indie', 'Luta'];
  all_pegi: string[] = ['PEGI 3', 'PEGI 7', 'PEGI 12', 'PEGI 16', 'PEGI 18'];

  constructor(private _service: SharedService,private _formBuilder: FormBuilder) {
    this.filtros = _formBuilder.group({
        'Steam': false,
        'Origin': false,
        'Epic Games': false,
        'EA': false,
        'Battlenet': false,
        'Playstation': false,
        'Xbox': false,
        'Nintendo': false
    });

    this.categorias = _formBuilder.group({
      acao: false,
      aventura: false,
      fps: false,
      rpg: false,
      estrategia: false,
      battleroyale: false,
      desporto: false,
      mmo: false,
      corridas: false,
      indie: false,
      luta: false
    });

    this.pegi = _formBuilder.group({
      pegi3: false,
      pegi7: false,
      pegi12: false,
      pegi16: false,
      pegi18: false
    });

    this.priceRange = _formBuilder.group({ min: '', max: '' }, {validator: minValidator});

    this.subscription = this._service.filter.subscribe((data: string) => {
      this.filterValue = data;
      if (this.filterValue !== '') {
        this.all_products = this._service.getProducts().filter((product: product) => product.title.toLowerCase().includes(this.filterValue.toLowerCase()));
        this.products = Object.create(this.all_products);
        this.events = this._service.getEvent().filter((event: any) => event.title.toLowerCase().includes(this.filterValue.toLowerCase()));
      } else {
        this.all_products = this._service.getProducts();
        this.products = Object.create(this.all_products);
        this.events = this._service.getEvent();
      }
      this.refreshFilters();
    });
  }

  ngOnInit(): void {
    this.filtros.valueChanges.subscribe(_ => this.refreshFilters() );
    this.categorias.valueChanges.subscribe(_ => this.refreshFilters() );
    this.pegi.valueChanges.subscribe(_ => this.refreshFilters() );
    this.priceRange.valueChanges.subscribe(_ => { 
      console.log(this.priceRange.status)
      if (this.priceRange.status == 'VALID') {
        this.refreshFilters()
      } 
    });
  }

  /* Shorthands for form controls (used from within template) */
  get min() { return this.priceRange.get('min') };
  get max() { return this.priceRange.get('max') };

   /* Update validation when the phone input changes */
   onPriceInput() {
    console.log('input')
    if (this.priceRange.hasError('priceWrong')) {
      this.min?.setErrors([{'priceWrong': true}]);
      this.max?.setErrors([{'priceWrong': true}]);
    } else {
      this.min?.setErrors(null);
      this.max?.setErrors(null);
    }
  }

  refreshFilters() {
    // Categories filter
    let products_c: any[] = [];
    let c_false = true;
    this.all_categories.forEach((c: string) => {
      if (this.categorias.get(c.toLocaleLowerCase().replace(/\s/g, "").normalize("NFD").replace(/\p{Diacritic}/gu, ""))?.value) {
        c_false = false;
        products_c = products_c.concat(this.all_products.filter((p: product) => p.categories.includes(c)));
      }
    });
    // Remove duplicate products
    products_c = products_c.filter((value, index, self) =>
      index === self.findIndex((t) => (
        t.place === value.place && t.title === value.title
      ))
    );
    if (c_false) products_c = Object.create(this.all_products);
    
    // Marketplace filter
    let products_m: any[] = [];
    let m_false: boolean = true;
    this.all_marketplaces.forEach((m: string) => {
      if (this.filtros.get(m)?.value) {
        m_false = false;
        products_m = products_m.concat(this.all_products.filter((p: product) => p.platform.includes(m)));
      }
    });
    if (m_false) products_m = Object.create(this.all_products);

    // Age restriction filter
    let products_a: any[] = [];
    let a_false: boolean = true;
    this.all_pegi.forEach((a: any) => {
      if (this.pegi.get(a.toLocaleLowerCase().replace(/\s/g, ""))?.value) {
        a_false = false;
        products_a = products_a.concat(this.all_products.filter((p: product) => p.pegi == a));
      }
    });
    if (a_false) products_a = Object.create(this.all_products);

    // Price filter
    let products_p: any[] = [];
    if (Number(this.max?.value) == 0)
      products_p = this.all_products.filter((p: product) => Number(p.key_price.substring(0, p.key_price.length-2).replace(',', '.')) >= Number(this.min?.value));
    else 
      products_p = this.all_products.filter((p: product) => Number(p.key_price.substring(0, p.key_price.length-2).replace(',', '.')) >= Number(this.min?.value) && Number(p.key_price.substring(0, p.key_price.length-2).replace(',', '.')) <= Number(this.max?.value));

    this.products = products_c.filter(value => products_m.includes(value));
    this.products = products_a.filter(value => this.products.includes(value));
    this.products = products_p.filter(value => this.products.includes(value));
  }
}

export const minValidator: ValidatorFn = (formGroup: AbstractControl ): ValidationErrors | null  => {
  var min: string = formGroup.get('min')?.value.replace(/\s/g, "");
  var max: string = formGroup.get('max')?.value.replace(/\s/g, "");
  console.log(min);
  console.log(max);

  // If min and max are numbers
  if (!isNaN(Number(min)) && !isNaN(Number(max))) {
    // If min or max are negative
    if (Number(min) < 0 || Number(max) < 0) return { priceWrong: true };

    if (Number(min) == 0 && Number(max) < 0) return { priceWrong: true }; 
    
    if (Number(max) == 0) {
      if (Number(min) < 0) return { priceWrong: true };
      return null;
    }

    // If min is greater than max
    if (Number(min) > Number(max)) {
      return { priceWrong: true };
    } else {
      console.log('aqui')
      return null;
    }
  } else {
    return { priceWrong: true };
  }
}
