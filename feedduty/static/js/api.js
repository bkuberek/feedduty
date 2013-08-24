/**
 * api.js
 * Copyright: © 2013 Bastian Kuberek
 */

var API = {};

$(document).ready(function() {

  API.form = $('form#api-form');
  API.modal = $('#api-response-modal');
  API.modal.modal({show: false});

  $('button.reload').click(function(event) {
    window.location.reload();
  });

  API.form.on('click', 'button[type="submit"]', function(event) {
    event.preventDefault();

    var http_method = $(this).attr('data-method');

    if (http_method === 'delete') {
      if (!confirm('Are you sure you want to delete this record?')) {
        return false;
      }
    }

    $.ajax({
      url: window.location.href,
      type: http_method,
      dataType: 'json',
      data: API.form.serialize(),
      complete: function(jqXHR, textStatus) {
        var headers = jqXHR.status + ' ' + jqXHR.statusText + '\n' + jqXHR.getAllResponseHeaders();
        var body = JSON.stringify(jqXHR.responseJSON, null, 2);

        API.modal.modal('toggle');
        API.modal.find('.modal-body').html($('<pre/>', {text: headers})).append($('<pre/>', {text: body}));
      }
    });

    return false;
  });
});
