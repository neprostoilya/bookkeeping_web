var sel_date2 = document.getElementById("date_sel2");
var today2 = new Date();
var dd2 = String(today2.getDate() + 1).padStart(2, '0');
var mm2 = String(today2.getMonth() + 1).padStart(2, '0'); 
var yyyy2 = today2.getFullYear();

today2 = yyyy2 + '-' + mm2 + '-' + dd2;
sel_date2.value = today2;