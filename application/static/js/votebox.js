function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function votebox_vote(type, id, val) {
  var key_path = '.' + type + '-' + id + ' .votebox .votebox-';
  var btn_up = $(key_path + 'up');
  var btn_down = $(key_path + 'down');

  var path = '/api/vote';
  var params = {
    'user_token': getCookie('op_token'),
    'object_id': id,
    'object_type': type,
    'value': val
  };

  $.ajax(path, {
    url: path,
    type: 'POST',
    dataType: 'json',
    data: JSON.stringify(params),
    contentType: 'application/json',
    success: function(data, textStatus, jqXHR) {
      // Update values
      var new_up = data[type]['votes_up'];
      var new_down = data[type]['votes_down'];

      btn_up.text('+' + new_up);
      btn_down.text('-' + new_down);

      var cl = "selected";
      if (val == 'up') {
        btn_up.addClass(cl);
        btn_down.removeClass(cl);
      } else if (val == 'down') {
        btn_down.addClass(cl);
        btn_up.removeClass(cl);
      }
    },
    error: function(jqHXR, textStatus, errorThrown) {
      alert(JSON.parse(jqHXR.responseText)['error']);
    }
  });
}
