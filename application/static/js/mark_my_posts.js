function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function toggleMarkMyPosts() {
  var checkbox = $("#mark-my-posts");
  var checked = checkbox.is(':checked') == true;

  var params = {
    'user_token': getCookie('op_token'),
    'mark_my_posts': checked
  };

  var path = '/api/user_settings';
  $.ajax(path, {
    url: path,
    type: 'PUT',
    dataType: 'json',
    data: JSON.stringify(params),
    contentType: 'application/json',
    success: function(data, textStatus, jqXHR) {
      // no-op, checkbox will change its status on its own.
    },
    error: function(jqHXR, textStatus, errorThrown) {
      alert(JSON.parse(jqHXR.responseText)['error']);
    }
  });
}
