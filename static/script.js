// Mobile dropdown
function dropdown() {
     elements = document.querySelectorAll("li a:not(.active)");
     for (i=0; i < elements.length; i++){
          elements[i].style.display = (elements[i].style.display == 'none') ? 'block' :
          (elements[i].style.display == 'block') ? 'none' :
          'inline-block';
     }
};

// Clock function
function getDateTime() {
     var now     = new Date();
     var year    = now.getFullYear();
     var month   = now.getMonth()+1;
     var day     = now.getDate();
     var hour    = now.getHours();
     var minute  = now.getMinutes();
     var second  = now.getSeconds();
     if(month.toString().length == 1) {
          month = '0'+month;
     }
     if(day.toString().length == 1) {
          day = '0'+day;
     }
     if(hour.toString().length == 1) {
          hour = '0'+hour;
     }
     if(minute.toString().length == 1) {
          minute = '0'+minute;
     }
     if(second.toString().length == 1) {
          second = '0'+second;
     }
     var dateTime = day+'/'+month+'/'+year+' - '+hour+':'+minute+':'+second;
     return dateTime;
}

document.addEventListener('DOMContentLoaded', function() {

     setInterval(function(){
          currentTime = getDateTime();
          document.getElementById("clock").innerHTML = currentTime;
     }, 1000);

     // Get info
     if (location.pathname == "/") {
          document.getElementById('language').innerHTML = navigator.language;
          document.getElementById('os').innerHTML = navigator.platform;
          document.getElementById('cpu').innerHTML = navigator.hardwareConcurrency;
          document.getElementById('user-agent').innerHTML = navigator.userAgent;
          document.getElementById('referrer').innerHTML = document.referrer;
          document.getElementById('referrer').href = document.referrer;

          online = (navigator.onLine) ? 'online' : 'offline';
          document.getElementById('online').innerHTML = online;

          cookies = (navigator.cookieEnabled) ? 'enabled' : 'disabled';
          document.getElementById('cookies').innerHTML = cookies;

          document.getElementById('screenX').innerHTML = screen.width;
          document.getElementById('screenY').innerHTML = screen.height;
     }

     // Render map
     $.getJSON("static/smallworld/dist/world.json", function(data) {
          water = '#0d0d0d';
          land = '#5AFA7B';
          marker = '#FF5555';

          if (theme == "light") {
               water = '#f2f2f2';
               land = '#008080';
          } else {
               if (theme == "red") {
                    land = '#FF5555';
                    marker = '#5AFA7B';
               } else if (theme == "blue") {
                    land = '#40E0D0';
               }
          }

          if (location.pathname == "/") {
               Smallworld.defaults.geojson = data;
               $('.map').smallworld({
                    center: [42, 5],
                    waterColor: water,
                    landColor: land,
                    markerColor: marker,
                    markerSize: 4,
                    marker: [latitude, longitude],
               });
          }
          if (document.URL.includes("map")) {
               Smallworld.defaults.geojson = data;
               $('.map').smallworld({
                    center: [42, 10],
                    waterColor: water,
                    landColor: land,
     	          zoom: 2,
                    markerColor: marker,
                    markerSize: 8,
                    marker: [latitude, longitude],
               });
          }
     });
});
