var walt = {};


walt.reveal = {}

walt.reveal.init = function(){
	$('.add-pin-modal').click(function(e) {
		e.preventDefault();
		$('#add-pin').reveal();
	});
};
