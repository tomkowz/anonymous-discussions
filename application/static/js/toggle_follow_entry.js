function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

// val = follow, unfollow
function toggle_follow_entry(id) {
  var key_path = '.entry-' + id + ' .follow-entry-toggle';
  var toggle_a = $(key_path);

  var path = '/api/entries/' + id + '/toggle_follow'

  var params = {
    'user_token': getCookie('op_token'),
    'entry_id': id
  };

  $.ajax(path, {
    url: path,
    type: 'GET',
    data: params,
    dataType: 'json',
    contentType: 'application/json',
    success: function(data, textStatus, jqXHR) {
      var follow = data['follow'];
      if (follow == true) {
        toggle_a.text('nie obserwuj');
      } else {
        toggle_a.text('obserwuj');
      }
    },
    error: function(jqHXR, textStatus, errorThrown) {
      alert(JSON.parse(jqHXR.responseText)['error']);
    }
  });
}
