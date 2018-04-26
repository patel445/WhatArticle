(function() {
   console.log("TEST");

    test = jQuery.getJSON("https://whatarticle.firebaseio.com/word_clouds.json");
   console.log(test);

   keys = Object.keys(test);
     for (key in keys) {
         //keys2 = Object.keys(key);
         console.log(keys[key]);
     }
    console.log("ASD");

})();