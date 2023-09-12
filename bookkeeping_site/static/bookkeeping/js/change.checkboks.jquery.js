$(document).ready(function() {
  $('.chk-all').click(function() {
    if($(this).prop('checked')){
      $('input[type="checkbox"]').prop('checked', true);
    } else {
      $('input[type="checkbox"]').prop('checked', false);
    }
  });
  $('.chk-none').click(function() {
    $('input[type="checkbox"]').prop('checked', false);
  });
});

$(document).ready(function() {
  var selectedCount = 0;
  $('.checkbox').change(function() {
    if ($(this).is(':checked')) {
      selectedCount++;
    } else {
      selectedCount--;
    }
    $('#selected-count').text(selectedCount);
  });
  
  $('.chk-all').change(function() {
    $('.checkbox').prop('checked', $(this).is(':checked'));
    if ($(this).is(':checked')) {
      selectedCount = $('.checkbox').length;
    } else {
      selectedCount = 0;
    }
    $('#selected-count').text(selectedCount);
  });
});