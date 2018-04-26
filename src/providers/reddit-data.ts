import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';
//https://whatarticle.firebaseio.com/word_clouds.json?print=pretty

@Injectable()
export class RedditData {
    constructor(public http: Http){
        console.log("Hello");
    }
    posts: any;
    
    getRemoteData(){
       this.http.get('https://www.reddit.com/r/gifs/new/.json?limit=10').map(res => res.json()).subscribe(data => {
            console.log(data);
            this.posts = data.data.children;
       });
    }

}