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

});