$(document).ready(function() {
  $('.add-related').click(function(event) {
    event.preventDefault();
    window.open($(this).attr('href'), 'newwindow', 'width=800,height=500');
  });
});