$(function() {

  $('.ios-switch input[type="checkbox"]').on('click', function() {
    const parentTr = $(this).closest('tr');
    const cameraId = parseInt(parentTr.data('cameraId'));

    $.ajax({
      type: "POST",
      url: `http://127.0.0.1:8080/api/v1/controller/camera/${cameraId}/update_state`,
      data: JSON.stringify({ is_active: this.checked }),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
    });

    if ( parentTr.hasClass('active') ) {
      parentTr.removeClass('active');
    } else {
      parentTr.addClass('active');
    }
  });

});