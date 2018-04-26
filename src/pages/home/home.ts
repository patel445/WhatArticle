import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';
import { AuthProvider } from '../../providers/auth/auth';
import { RedditData } from '../../providers/reddit-data'
//https://whatarticle.firebaseio.com/word_clouds.json?print=pretty

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {   
    posts:any;
    
	constructor(public navCtrl: NavController,public authProvider: AuthProvider, public public http: Http) {
      this.http.get('https://whatarticle.firebaseio.com/word_clouds.json?print=pretty').map(res => res.json()).subscribe(data => {
            console.log(data)
       });
       
	}
    
  logMeOut() {
    this.authProvider.logoutUser().then( () => {
      this.navCtrl.setRoot('LoginPage');
    });
  }
   
}