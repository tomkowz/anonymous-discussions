function votebox_vote(type, id, val) {
  var key_path = '.' + type + '-' + id + ' .votebox .votebox-';
  var btn_up = $(key_path + 'up');
  var btn_down = $(key_path + 'down');

  var path = '/_votebox';
  $.getJSON(path, {
    object_type: type,
    object_id: id,
    value: val
  }, function(data) {

    // Update values
    btn_up.text('+' + data.up);
    btn_down.text('-' + data.down);

    // Disable buttons
    btn_up.attr('onclick', '');
    btn_down.attr('onclick', '');
  });
}
