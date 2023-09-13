$(document).ready(function() {

  var currentUrl = window.location.href; 

  $('a.sort-link').click(function(e) {
    e.preventDefault();
    var sortValue = $(this).attr('value');
    var sortHref = $(this).attr('href')
    if (sortHref == '?sort=-' + sortValue) {
      sortHref = '?sort=' + sortValue;
      history.pushState(null, null, sortHref);
    } else {
      sortHref = '?sort=-' + sortValue;
      history.pushState(null, null, sortHref);
    }
    window.history.pushState(null, null, sortHref);
    $(this).attr('href', sortHref);
    
    if (window.location.href != currentUrl) { 
      location.reload(); 
    }
  });
});