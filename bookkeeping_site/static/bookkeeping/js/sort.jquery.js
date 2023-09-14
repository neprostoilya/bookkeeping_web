$(document).ready(function() {

  var currentUrl = window.location.href; 

  $('a.sort-link').click(function(e) {
    e.preventDefault();
    var sortValue = $(this).attr('value');
    var sortHref = $(this).attr('href')
    if (sortHref == '?sort=-' + sortValue) {
      sortHref = '?sort=' + sortValue;
      $(this).append('<i style="margin-top: .2em;" class="fa fa-sort-alpha-up"></i>');
      history.pushState(null, null, sortHref);
    } else {
      sortHref = '?sort=-' + sortValue;
      $(this).append('<i style="margin-top: .2em;" class="fa fa-sort-alpha-down"></i>');
      history.pushState(null, null, sortHref);
    }
    window.history.pushState(null, null, sortHref);

    
    if (window.location.href != currentUrl) { 
      location.reload(); 
    }
    $('a.remove-sort-link').addClass('d-none');
    $(this).siblings('.remove-sort-link').removeClass('d-none');
  });
  
  $('a.remove-sort-link').click(function(e) {
    e.preventDefault();
    var sortHref = window.location.href.replace(/[?&]sort=[^&]+/, '');
    history.pushState(null, null, sortHref);
    location.reload(); 
  }); 

  $('a.remove-sort-link').addClass('d-none');
  var urlParams = new URLSearchParams(window.location.search);
  var sortParam = urlParams.get('sort');
  if (sortParam) {
    var sortValue = sortParam.replace('-', '');
    var $sortLink = $('a.sort-link[value="' + sortValue + '"]');
    $sortLink.siblings('.remove-sort-link').removeClass('d-none');
}});