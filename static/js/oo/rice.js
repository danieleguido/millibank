/**
	oo
	Serie handler
*/

var oo = oo || {}; oo.rice = {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.serie = {}
oo.magic.serie.add = function(){}

/*


    Api
    ===

*/
oo.api.serie = {};
oo.api.serie.add = function( params ){ oo.log( '[oo.api.serie.add]', params );
	$.ajax( $.extend( oo.api.settings.post,{ url: oo.urls.serie.add,
		data: params,
		success:function(result){ oo.log( "[oo.api.pin.add] result:", result );
			oo.api.process( result, oo.magic.serie.add, "id_add_serie" );
		}
	}));
};

/*


    Rice UI
    =======

*/
oo.rice = oo.rice || {};

oo.rice.dragstart = function( event ){
	$("#actual-serie").height( 40 );
}

oo.rice.add_frame = function( event ){
	var frame = $(this);
	oo.trigger( oo.rice.events.add_frame, new oo.rice.Frame({ id: frame.attr('data-id'), mimetype: frame.attr('data-mimetype'), slug: frame.attr('data-slug') }) );
}

oo.rice.init = function(){oo.log("[oo.rice.init]");
	
	// load last serie from cookie
	oo.rice.serie = new oo.rice.Serie({ autoload:true });

	// start global listeners
	$(document).on('click','.drag-to-serie', oo.rice.add_frame  );

}

oo.rice.events = {
	    'add_frame':'oo.rice.events.add_frame',
	 'change':'oo.rice.events.change',
	  'clean':'oo.rice.events.clean',
	   'init':'oo.rice.events.init',
	'replace':'oo.rice.events.replace',
	 'remove':'oo.rice.events.remove',
	  'reset':'oo.rice.events.reset',
	  'inscribe':'oo.rice.events.inscribe'
};

/*


    Serie Class
    ===========

*/
oo.rice.Serie = function( options ){

	var serie = this

	this.settings = $.extend({
		autoload: false,
		target_selector: '#actual-serie',
		source_selector: '.draggable',
		frames:[],
		slug:'serie-slug'

	}, options );

	/*
		Expose publicly serie frames
	*/
	this.get_frames = function(){
		return this.settings.frames;
	}

	/*
		get current hash (md5) git like
	*/
	this.get_hash = function(){
		return md5( JSON.stringify( this.settings ) )
	}


	this.html = function(){

	}


	this.sync = function(){
		

	}

	/*
		@param frames -	
	*/
	this.set_frames = function( frames ){
		oo.log( "[serie] set_frames", this.settings );
		// compare version. 

		this.settings.frames = []
		
		for( f in frames ){
			this.settings.frames.push( oo.rice.Frame( frames[f] ) );
		}
	}

	this.add_frame = function( event, frame ){
		// add and send
		oo.log( "[serie] set_frames", frame );
		serie.settings.frames.push( frame );
		serie.sync();
	};

	this.init = function(){
		oo.log( "[serie] init", this.settings );

		// intitialize history
		this.history = new oo.rice.History()

		// initialize sortable
		$( this.settings.target_selector ).sortable({
		    revert: true,
		    update: function(event, ui) {
		        if ($(ui.item).hasClass('draggable')) {
		            $(ui.item).css({color:'red'});
		        }
		    }
		});

		$( this.settings.source_selector ).draggable({
		    connectToSortable: this.settings.target_selector,
		    helper: 'clone',
		    revert: 'invalid'
		});

		$('ul, li').disableSelection();


		// enable listeners
		oo.on( oo.rice.events.add_frame, this.add_frame );

		

	}

	this.init();
}


/*


    Frame Class
    ===========

*/
oo.rice.Frame = function( options ){
	
	this.settings = $.extend({
		id:0,
		mimetype: 'text/plain',
		slug: '', // frame object as it comes from api/frame
	}, options );

	this.props = function(){
		return this.settings
	}

	this.html = function(){
		return $("<li/>",{ 'data-slug': this.settings.slug, 'class':'frame ' + this.settings.mimetype }).text(
			"#" + this.settings.id
		);
	}
};


oo.rice.History = function( options ){

	this.buffer = [];
	this.cursor = 0;

	this.settings = $.extend({
		onInscribeEvent: oo.rice.events.inscribe
	}, options );

	this.inscribe = function( eventType, data ){
		oo.log( "[new oo.rice.History] inscribe", eventType, data);
		this.buffer.push({
			hash: md5( data ),
			type: eventType,
			data:data
		});
		this.cursor = this.buffer.length - 1;
	}

	this.back = function(){
		
	}

	this.init = function(){
		oo.log( "[new oo.rice.History] init");
		oo.on( oo.rice.events.inscribe, this.inscribe );
	}
	this.init();
}