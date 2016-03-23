function post_entry() {
  $.ajax({
    url: '/api/entries',
    type: 'POST',
    data: $('form').serialize(),
    dataType: 'json',
    success: function(response) {
      $('.error').text('');
      $('.success').text('Wpis został dodany.');
    },
    error: function(error) {
      $('.error').text('Wprowadzony tekst jest zbyt, krótki lub zawiera niedozwolone znaki.');
      $('.success').text('');
    }
  });
}
