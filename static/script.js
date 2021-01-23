// Mobile dropdown
function dropdown() {
     elements = document.querySelectorAll("li a:not(.active)");
     for (i=0; i < elements.length; i++){
          elements[i].style.display = (elements[i].style.display == 'none') ? 'block' :
          (elements[i].style.display == 'block') ? 'none' :
          'inline-block';
     }
}
