import { Component, NgZone, ViewChild } from '@angular/core';
import { Platform, Nav } from 'ionic-angular';
import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';
import { HomePage } from '../pages/home/home';
import { HotPost } from '../pages/hotpost/hotpost';
import { AboutPage } from '../pages/about/about';
import firebase from 'firebase';

@Component({
  templateUrl: 'app.html'
})
export class MyApp {
  rootPage:any;
  public zone:NgZone;
  @ViewChild(Nav) nav: Nav;
  
  pages: Array<{title: string, component: any}>;


  constructor(platform: Platform, statusBar: StatusBar, splashScreen: SplashScreen) {
    this.zone = new NgZone({});
    this.pages = [
      { title: 'Homepage', component: HomePage },
      { title: 'HotPost', component: HotPost },
      { title: 'About', component: AboutPage }
    ];
    const config = {
      apiKey: "AIzaSyBGLE19gJq1oawff7u-tv09LlRXz3__fmE",
      authDomain: "whatarticle.firebaseapp.com",
      databaseURL: "https://whatarticle.firebaseio.com",
      projectId: "whatarticle",
      storageBucket: "whatarticle.appspot.com",
      messagingSenderId: "28968695656"
    };
    firebase.initializeApp(config);

    firebase.auth().onAuthStateChanged( user => {
      this.zone.run( () => {
        if (!user) { 
          this.rootPage = 'LoginPage';
        } else {
          this.rootPage = HomePage;
        }
      });     
    });

    platform.ready().then(() => {
      statusBar.styleDefault();
      splashScreen.hide();
    });
  }
  openPage(page) {
        this.nav.setRoot(page.component);
  }

}