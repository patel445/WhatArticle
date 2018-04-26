import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';
import { AuthProvider } from '../../providers/auth/auth';
//https://whatarticle.firebaseio.com/word_clouds.json?print=pretty

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {   
    posts:any;
    posts2:any;
    posts3:any;
    posts4:any;
    posts5:any;
    posts6:any;
    posts7:any;
    posts8:any;
    posts9:any;
    
    
	constructor(public navCtrl: NavController,public authProvider: AuthProvider, public http: Http) {
      this.http.get('https://whatarticle.firebaseio.com/wordclouds.json?  print=pretty').map(res => res.json()).subscribe(data => {
            console.log(data)
            this.posts = data.all;
            this.posts2 = data.askreddit;
            this.posts3 = data.worldnews;
            this.posts4 = data.funny;
            this.posts5 = data.news;
            this.posts6 = data.politics;
            this.posts7 = data.gaming;
            this.posts8 = data.programmerhumor;
            this.posts9 = data.showerthoughts;
     }); 
	}
    
  logMeOut() {
    this.authProvider.logoutUser().then( () => {
      this.navCtrl.setRoot('LoginPage');
    });
  }
   
}