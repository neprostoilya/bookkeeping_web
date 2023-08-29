function showPopup(icon) {
   var comment = icon.getAttribute("data-comment"); 
   var popupBody = document.querySelector(".popup-body");
   popupBody.innerHTML = "<p>" + comment + "</p>"; 
   document.getElementById("popup").classList.add("show");
}
 
function closePopup() {
   var popupBody = document.querySelector(".popup-body");
   popupBody.innerHTML = ""; 
   document.getElementById("popup").classList.remove("show");
}