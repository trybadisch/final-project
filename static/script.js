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
});
