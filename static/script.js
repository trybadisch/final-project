// Mobile dropdown
function dropdown() {
     elements = document.querySelectorAll("li a:not(.active)");
     for (i=0; i < elements.length; i++){
          elements[i].style.display = (elements[i].style.display == 'none') ? 'block' :
          (elements[i].style.display == 'block') ? 'none' :
          'inline-block';
     }
}

// console.log("Cookies: " + navigator.cookieEnabled);
// console.log("Browser Language: " + navigator.browserLanguage);
// console.log("Language: " + navigator.language);
// console.log("Platform: " + navigator.platform);
// console.log("Connection Speed: " + navigator.connectionSpeed);
// console.log("User Agent: " + navigator.userAgent);
// console.log("Webdriver: " + navigator.webdriver);
// console.log("Geolocation: " + navigator.geolocation);


// https://developer.mozilla.org/en-US/docs/Web/API/Navigator

// navigator.connection
// navigator.deviceMemory
// navigatorConcurrentHardware.hardwareConcurrency  // number of logical CPU cores
// navigatorLanguage.language
// navigatorLanguage.languages
// navigator.mediaDevices
// navigator.userAgent
// navigator.onLine

// console.log(document.referrer)
