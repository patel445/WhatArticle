import { Component } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';
import { AuthProvider } from '../../providers/auth/auth';
import { IonicPage, NavController, NavParams} from 'ionic-angular';
//https://whatarticle.firebaseio.com/word_clouds.json?print=pretty

@Component({
  selector: 'hotposts',
  templateUrl: 'hotpost.html'
})
export class HotPost {   
    hotposts:any;
    constructor(public navCtrl: NavController, public navParams: NavParams, public http: Http) {
    this.http.get('https://whatarticle.firebaseio.com/hot_posts.json?print=pretty').map(res => res.json()).subscribe(data => {
            console.log(data)
            this.hotposts = data;
     }); 
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad AboutPage');
  }
  
}