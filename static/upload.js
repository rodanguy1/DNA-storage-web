$(document).ready(function() {

	$('form').on('submit', function(event) {

		event.preventDefault();

		var formData = new FormData($('form')[0]);

		jQuery.ajax({
			xhr : function() {
			    alert('The files uploading will take a few minutes');
				var xhr = new window.XMLHttpRequest();

				xhr.upload.addEventListener('progress', function(e) {

					if (e.lengthComputable) {

						console.log('Bytes Loaded: ' + e.loaded);
						console.log('Total Size: ' + e.total);
						console.log('Percentage Uploaded: ' + (e.loaded / e.total))

						var percent = Math.round((e.loaded / e.total) * 100);

						$('#progressBar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');

					}

				});

				return xhr;
			},
			type : 'POST',
			url : '/upload',
			data : formData,
			processData : false,
			contentType : false,
			complete: function() {
                if (response.status == 302) {
                   window.location = response.getResponseHeader('after_run');
                   window.location.replace("/after_run");
                }
                window.location.replace("/after_run");
            },
//			window.location.href ="after_run";
//			window.location = "/after_run";
//			if (response.redirect) {
//                window.location.href = response.redirect;
//            },
			success: function (response) {
              // Make sure the response actually has a redirect
              if (response.redirect) {
                window.location.href = response.redirect;
              }
              window.location.replace("/after_run");
            }
		});

	});

});