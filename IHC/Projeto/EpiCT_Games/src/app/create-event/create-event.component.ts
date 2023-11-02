import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';
import { event, product, SharedService } from '../shared.service';
import * as _moment from 'moment';
import { MomentDateAdapter } from '@angular/material-moment-adapter';
import { MatDialogRef } from '@angular/material/dialog';
import { map, Observable, startWith } from 'rxjs';
import { Router } from '@angular/router';
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
  selector: 'app-create-event',
  templateUrl: './create-event.component.html',
  styleUrls: ['./create-event.component.scss'],
  providers: [
    { provide: MAT_DATE_LOCALE, useValue: 'en-GB' },
    { provide: DateAdapter, useClass: MomentDateAdapter, deps: [MAT_DATE_LOCALE] },
    { provide: MAT_DATE_FORMATS, useValue: DATE_FORMAT },
  ]
})
export class CreateEventComponent implements OnInit {
  form: FormGroup;
  filteredOptions2?: Observable<product[]>;
  jogos!: product[];

  constructor(private _service: SharedService, private _router: Router, private _form: FormBuilder, public dialog: MatDialogRef<CreateEventComponent>) {
    //get products
    this.form =_form.group({
        nome: new FormControl('', [Validators.required]),
        localizacao: new FormControl('', [Validators.required]),
        cidade: new FormControl('', [Validators.required]),
        dataI: new FormControl('', [Validators.required]),
        dataF: new FormControl('', [Validators.required]),
        hora: new FormControl('', [Validators.required,Validators.pattern('^([0-1]?[0-9]|2[0-4]):([0-5][0-9])(:[0-5][0-9])?$')]),
        preço: new FormControl('', [Validators.required, Validators.pattern('^[0-9]+(\,[0-9]{2})')]),
        jogo: new FormControl('', [Validators.required]),
      }, {validator: [gameValidator, dateValidator]});
   }

  ngOnInit(): void {
    this.jogos = this._service.getProducts();
    this.filteredOptions2 = this.form.valueChanges.pipe(//categorias
      startWith(''),
      map(value => this._filter2(value)),
    );
  }

  submit() {
    if (this.form.valid) {
      var event: event;
      event = {
        title: this.form.value.nome,
        location: this.form.value.cidade.trim() + ', ' + this.form.value.localizacao.name,
        start_date: moment(this.form.value.dataI).format('DD-MM-YYYY'),
        end_date: moment(this.form.value.dataF).format('DD-MM-YYYY'),
        hour: this.form.value.hora,
        price: this.form.value.preço,
        game: this.form.value.jogo,
      }

      this.dialog.close();
      var event_product: any = {
        title: event.title,
        key_price: '150,00 €',
        price: null,
        rating: 0,
        description: "",
        comments: [],
        categories: [""],
        platform: [""],
        pegi: "",
        event: event
      }
      
      event_product.type = 'event';
      this._service.openCartPage(event_product);
      this._router.navigate(['/checkout'])
    }
  }

  get jogo() { return this.form.get('jogo'); }
  get nome() { return this.form.get('nome'); }
  get localizacao() { return this.form.get('localizacao'); }
  get cidade() { return this.form.get('cidade'); }
  get dataI() { return this.form.get('dataI'); }
  get dataF() { return this.form.get('dataF'); }
  get hora() { return this.form.get('hora'); }
  get preco() { return this.form.get('preço'); }
  get imagem() { return this.form.get('imagem'); }

  private _filter2(value: any): product[] {
    if (value.jogo == undefined) return this.jogos;

    const filterValue2 = value?.jogo?.toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "")

    return this.jogos.filter(option => option.title.toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "").includes(filterValue2));
  }
  
  onGameInput() {
    if (this.form.hasError('gameWrong')) {
      this.jogo?.setErrors([{'gameWrong': true}]);
    } else {
      this.jogo?.setErrors(null);
      var a = this.jogos.findIndex(x => x.title.toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "") == this.jogo?.value.toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, ""));
      this.form.get('jogo')?.setValue(this.jogos[a].title);
    }
  }

  onDateInput() {
    if (this.form.hasError('dateWrong')) {
      this.dataI?.setErrors([{'dateWrong': true}]);
      this.dataF?.setErrors([{'dateWrong': true}]);
    } else {
      this.dataI?.setErrors(null);
      this.dataF?.setErrors(null);
    }
  }

  close() {
    this.dialog.close();
  }
}

export const gameValidator: ValidatorFn = (formGroup: AbstractControl ): ValidationErrors | null  => {
  var _service: SharedService = new SharedService();
  var games: product[] = _service.getProducts();

  var game_input: string = formGroup.get('jogo')?.value;

  var game_query = games.filter((game) => game.title.toLocaleLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "") == game_input.toLocaleLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, ""));
  if (game_query.length == 0) {
    return {'gameWrong': true};
  }
  return null;
}

export const dateValidator: ValidatorFn = (formGroup: AbstractControl ): ValidationErrors | null  => {
  var now = moment();
  var start = moment(formGroup.value.dataI);
  var end = moment(formGroup.value.dataF);

  if (start.isBefore(now, 'day')) {
    return {'dateWrong': true};
  } else if (start.format('DD-MM-YYYY') == 'Invalid date') {
    return {'dateWrong': true};
  } else if (end.format('DD-MM-YYYY') == 'Invalid date') {
    return {'dateWrong': true};
  } else {
    return null;
  }
}
