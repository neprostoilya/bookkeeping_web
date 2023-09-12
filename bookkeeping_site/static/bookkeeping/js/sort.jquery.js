$(document).ready(function() {
    var sortParam = '';
    $('a.sort-link').click(function(e) {
      e.preventDefault();
      var sortValue = $(this).attr('value');
      if (sortParam == '') {
        sortParam = '?sort=-' + sortValue;
      } else if (sortParam == '?sort=-' + sortValue) {
        sortParam = '?sort=' + sortValue;
      } else {
        sortParam = '';
      }
      window.history.pushState(null, null, sortParam);
      location.reload(); 
    });

    $('a.remove-sort-link').click(function(e) {
      e.preventDefault();
      sortParam = '';
      window.history.pushState(null, null, '');
      location.reload(); 
    });
  });