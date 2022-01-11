$(document).ready(function() {
	$('#findplane').on('click', function() {

		$.ajax({
			data : {
				rotaxis : $('#rotaxis').val(),
				maxsigma : $('#maxsigma').val()
			},
			type : 'POST',
			url : '/gbbuild/findplane'
		})
		.done(function(data) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.ab).show();
				$('#errorAlert').hide();
			}
		});

	});


	$('#makeinter').on('click', function() {

		$.ajax({
			data : {
				rotaxis : $('#rotaxis').val(),
				maxsigma : $('#maxsigma').val()
			},
			type : 'POST',
			url : '/gbbuild/makegb'
		})
		.done(function(data) {
			if (data.error) {
				$('#secondresult').text("Nothing").show();
			}
			else {
				$('#secondresult').text(data.result).show();
			}
		});


	});

	$(function() {
		$('#but1').click(function() {
								var form_data = new FormData();
								form_data.append("newfile", $("#myciffile")[0].files[0]);

								$.ajax({
									type: 'POST',
									url: '/gbbuild/sendfile',
									data: form_data,
									contentType: false,
									cache: false,
									processData: false,
									success: function(data_s) {
										var singlestr=data_s.resultsingle;
										console.log('Files Uploaded Successfully!');
										  $("#file_content").text(data_s.resultsingle);
									},
								});
							});
						});


});

