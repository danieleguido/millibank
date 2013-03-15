var oo = oo || {}; 
oo.vars.glue = oo.vars.glue || {}; 
oo.glue = {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.reload = function(){
	window.location.reload();
}

oo.magic.page = oo.magic.page || {};

oo.magic.page.add = function( result ){
	oo.log("[oo.magic.page.add]", result);
	window.location.reload();
}

oo.magic.pin = oo.magic.pin || {};
oo.magic.pin.add = function( result ){
	oo.log("[oo.magic.pin.add]", result);
	window.location.reload();
}
oo.magic.pin.get = function( result ){
	oo.log("[oo.magic.pin.get]", result);
	// window.location.reload();
}



/*


    Glue Init
    =========

	Require wysihtml5 plugin

*/
oo.glue = {};
oo.glue.pin = {};
oo.glue.pin.listeners = {};

oo.glue.resize = function(){
	var h = $(window).height();

	if ( h < 600){
		$("#navbar .description").hide();
	} else {
		$("#navbar .description").show();
	}

	var hh = $("header").height();
	var fh = $("footer").height();


	$(".modal-body").height( h - 160 );

	//$(".items").height(
	//	h - hh - fh
	//);
}

oo.glue.pin.listeners.edit = function( event ){
	var pin_id = $(this).attr("data-id");
	oo.log("[oo.glue.pin.listeners.edit] pin id :", pin_id);
	oo.toast( oo.i18n.translate('loading') );
	// get pin and activate modal
	oo.api.pin.get({id:pin_id}, function( result ){
		$().toastmessage("cleanToast");
		oo.log("[oo.api.pin.get:callback]", result);
		$("#id_edit_pin_id").val( pin_id );
		$("#id_edit_pin_title").val( result.object.title );
		$("#id_edit_pin_permalink").val( result.object.permalink );
		$("#id_edit_pin_abstract").val( result.object.abstract );
		$("#id_edit_pin_content").val( result.object.content );
		$("#edit-pin-modal").modal({show:true});
		
	});

	// load and callback to oo.glue.pin.edit
};


oo.glue.pin.listeners.update = function(event){ event.preventDefault(); 
	var el = $(this);



	// get django form auto_id
	var auto_id = el.attr("data-auto-id");
	oo.log("[oo.glue.init:$('.update-pin'):click] form namespace 'auto_id' : ", auto_id);


	var params = {
		id:$("#" + auto_id + "_id").val(),
		title:$("#" + auto_id + "_title").val(),
		content:$("#" + auto_id + "_content").val(),
		abstract:$("#" + auto_id + "_abstract").val(),
		permalink:$("#" + auto_id + "_permalink").val(),
		auto_id: auto_id
	}

	oo.log("[oo.glue.init:$('.update-pin'):click] edit pin : ", params.id );
	oo.api.pin.edit( params );
}

oo.glue.pin.listeners.add = function(event){ event.preventDefault(); 
	var el = $(this);

	// get django form auto_id
	var auto_id = el.attr("data-auto-id"); // eg "id_add_walt_w" or "id_add_walt_l"

	oo.log("[oo.glue.init:$('.add-walt-pin'):click] form namespace 'auto_id' : ", auto_id)

	// build stuff
	var permalink = $("#" + auto_id + "_permalink").val();
	var page_slug = el.attr("data-page-slug"); // page parent slug. It could be undefined
	var pin_slug = el.attr("data-pin-slug"); // pin parent slug. It could be undefined.

	var content = $("#" + auto_id + "_content").val();
	var mimetype = $("#" + auto_id + "_mimetype").val();
	

	oo.log("[oo.glue.init:click] #add-pin, page-slug:", page_slug, ", parent-pin-slug:", pin_slug );

	var params = {
		title_en:$("#" + auto_id + "_title_en").val(),
		title_fr:$("#" + auto_id + "_title_en").val(),
		title_it:$("#" + auto_id + "_title_en").val(),
		slug:$("#" + auto_id + "_slug").val(),
		auto_id: auto_id
	}


	if ( typeof permalink != "undefined" && permalink.length ){
		$.extend(params,{permalink:permalink});
	}

	if ( typeof content != "undefined" && content.length ){
		$.extend(params,{content:content});
	}

	if ( typeof mimetype != "undefined" && mimetype.length ){
		$.extend(params,{mimetype:mimetype});
	}

	if ( typeof page_slug != "undefined" && page_slug.length ){
		$.extend(params,{page_slug:page_slug});
	}

	if ( typeof pin_slug != "undefined" && pin_slug.length ){
		$.extend(params,{parent_pin_slug:pin_slug});
	}

	// procede to api
	oo.api.pin.add( params );
}

oo.glue.init = function(){ oo.log("[oo.glue.init]");
	
	// compile pin api
	oo.api.compile( 'pin' );

	// bib text parser init
	oo.glue.bibtex.init();

	// input.repeatable: copy $.val() to targeted data-target element
	$(document).on('keyup', 'input.repeatable', function(event){ var $this = $(this); $( '#' + $this.attr('data-target') ).val( oo.fn.slug( $this.val() ) );});


	$(document).on('keyup', 'textarea.embeddable', oo.glue.embed.keyup );
	
	// remove invalid elements
	$(document).click( function(event){ $(".invalid").removeClass('invalid');});

	$(document).on('shown', function () {
		oo.log( "ehi" );
	  $('input:text:visible:first', this).focus();
	});

	// modal max height
	oo.on('resize', function(){ oo.fn.wait( oo.glue.resize, 100 );});
	oo.glue.resize();


	// open generic pin editor (ajax load the pin)
	$(".edit-pin").on("click", oo.glue.pin.listeners.edit );

	// save edited pin
	$(".update-pin").on("click", oo.glue.pin.listeners.update );

	// generic pin adder to walt page, with error control
	$(".add-walt-pin").on("click", oo.glue.pin.listeners.add );

};

oo.glue.embed = {};
// clean a textarea
oo.glue.embed.keyup = function( event ){
	var el = $(this);
	var content = el.val().replace(/^\s+|\s+$/g,'');
	var url = "";



	try{
		url = content.match(/src=(?!\s)['"]?(.+?)[\s"']/).pop()
	} catch( e ){
		el.val( content );
		oo.toast()
		return;
	}


	// replave numeric pixel width 100%
	el.val( content.replace(/width=(?!\s)["']?([\dpx\%]+)[\s'"]/g,'width="100%"') );
	
	//
	$('#' + el.attr('data-target-permalink')).val( url );


};



oo.glue.bibtex = { timer:0 }
oo.glue.bibtex.wait = function( event ){
	clearTimeout( oo.glue.bibtex.timer );
	oo.glue.bibtex.timer  = setTimeout( oo.glue.bibtex.parse, 1000);
}

oo.glue.bibtex.parse = function(){
	try{	
		var bib = oo.fn.bibtex( $("#id_add_walt_l_content").val() );
		oo.log( bib );
		$("#id_add_walt_l_title_en").val( bib.title );
		$("#id_add_walt_l_slug").val( oo.fn.slug( bib[ bib.bibtext_key ] ) );
	} catch( e ){
		oo.log( e );
	}
}

oo.glue.bibtex.init = function(){
	// content as bibtext parser !@!
	$("#id_add_walt_l_content").on("keyup", oo.glue.bibtex.wait );

}


oo.glue.upload = { is_dragging:false }
oo.glue.upload.enable = function()
{
	oo.log("[oo.glue.upload.enable]");
	$('#fileupload').fileupload('enable');
}

oo.glue.upload.disable = function(){
	oo.log("[oo.glue.upload.disable]");
	$('#fileupload').fileupload('disable');
}
oo.glue.upload.init = function(){
	oo.log("[oo.glue.init]");

	$('#fileupload').fileupload({
		url: oo.urls.pin_upload,
		dataType: 'json',
		sequentialUploads: true,
		dragover: function(e,data){
			if (oo.glue.upload.is_dragging)
				return;
			oo.log("[oo.glue.upload] dragover");
			oo.glue.upload.is_dragging = true;
		},
		drop:function(e,data){
			oo.log("[oo.glue.upload] drop");
			oo.glue.upload.is_dragging = false;
		},
		done: function (e, data) {
			oo.log( e, data.result);
			oo.toast("uploaded finished", { stayTime: 2000,cleanup:true });
			if( data.result.status == "ok"){
				oo.toast( "COMPLETED GUY!:!!!" );
			} else{
				oo.toast( data.result.error, ds.i18n.translate("error"), { stayTime: 2000, cleanup:true });	
			}
		},
		start: function (e, data) {
			oo.toast(oo.i18n.translate("start uploading"), { stayTime: 2000 });
		},
		fail: function( e, data){
			oo.log(e, data);
			oo.fault( e.type);
		},
		progressall: function (e, data) {
			var progress = parseInt(data.loaded / data.total * 100, 10);
			$('#progress .bar').width( progress + '%');
		},

    	add: function (e, data) {
			var slug = $('body').attr('data-page-slug');
			if( slug.length > 0 ){
				data.formData = { 'page_slug':slug };
			}
			data.submit();
			
		}
	});
	// enabled by default, or comment
	// oo.glue.upload.disable();
};


