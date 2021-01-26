// Mobile dropdown
function dropdown() {
     elements = document.querySelectorAll("li a:not(.active)");
     for (i=0; i < elements.length; i++){
          elements[i].style.display = (elements[i].style.display == 'none') ? 'block' :
          (elements[i].style.display == 'block') ? 'none' :
          'inline-block';
     }
};

document.addEventListener('DOMContentLoaded', function() {

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

     $.getJSON("static/smallworld/dist/world.json", function(data) {
          data = data;

          if (location.pathname == "/") {
               Smallworld.defaults.geojson = data;
               $('.map').smallworld({
                    center: [42, 5],
                    waterColor: '#0d0d0d',
                    landColor: '#5AFA7B',

                    markerColor: '#FF5555',
                    markerSize: 4,
                    marker: [latitude, longitude],
               });
          }
          if (document.URL.includes("map")) {
               Smallworld.defaults.geojson = data;
               $('.map').smallworld({
                    center: [42, 10],
                    waterColor: '#0d0d0d',
                    landColor: '#5AFA7B',
     	          zoom: 2,

                    markerColor: '#FF5555',
                    markerSize: 6,
                    marker: [latitude, longitude],
               });
          }
     });
});
