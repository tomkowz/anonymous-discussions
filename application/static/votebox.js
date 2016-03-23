function votebox_vote(type, id, val) {
  var path = '/_votebox';
  $.getJSON(path, {
    object_type: type,
    object_id: id,
    value: val
  }, function(data) {
     $('.' + type + '-' + id + ' .votebox .votebox-up').text('+' + data.up);
     $('.' + type + '-' + id + ' .votebox .votebox-down').text('-' + data.down);
  });
}
