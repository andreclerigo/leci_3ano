import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { event,product,SharedService } from '../shared.service';

@Component({
  selector: 'app-event',
  templateUrl: './event.component.html',
  styleUrls: ['./event.component.scss']
})
export class EventComponent implements OnInit {
  month: string[] = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
  @Input() data: any;
  isActive1 = false;

  constructor(private _router: Router, private _service: SharedService) { }

  ngOnInit(): void {
  }

  /* Open the page with the product details */
  open_event() {
    this._router.navigate(['/product']);  // change navigation to future page of "/event"
    this._service.openProductPage(this.data);
  }

  /* Add the selected item to the shopping cart */
  addCart() {
    var event_product: any = {
      title: this.data.title,
      key_price: this.data.price,
      price: null,
      image: this.data.img,
      rating: 0,
      description: "",
      comments: [],
      categories: [""],
      platform: [""],
      pegi: ""
    }
    
    event_product.type = 'ticket';
    this._service.openCartPage(event_product);
  }

  dateToString(date: string) {
    var info_list = date.split('-');

    return info_list[0] + ' de ' + this.month[parseInt(info_list[1]) - 1] + ' de ' + info_list[2];
  }
}
