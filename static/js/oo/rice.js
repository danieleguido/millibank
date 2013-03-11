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
oo.magic.serie.add = function( result ){

}

/*


    Api
    ===

*/



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
	
	// compile api callers:
	oo.api.compile( 'serie' );

	// load last serie from cookie
	oo.rice.serie = new oo.rice.Serie({ autoload:true });

	// start global listeners
	$(document).on('click','.drag-to-serie', oo.rice.add_frame  );

	// reveal add new serie modal on click
	$(document).on("click",".add-serie", function(event){ oo.trigger( oo.rice.events.serie.add ) });

	// use serie
	$(document).on("click",".change-serie", function(event){ oo.trigger( oo.rice.events.serie.change, { id: $(this).attr('data-id')});});
	
	// add serie on click
	$("#add-serie").click( function(){ event.preventDefault();
		title = $("#id_add_serie_title_en").val();

		oo.api.serie.add({
			title_en:title,
			title_fr:title,
			title_it:title,
			slug:$("#id_add_serie_slug").val(),
			type: $("#id_add_serie_type").val()
		});
	});

}

oo.rice.events = {
	serie:{
		add: 'oo.rice.events.serie.add',
		change: 'oo.rice.events.serie.change' // load and use a different serie
	},
	frame:{
		add: 'oo.rice.events.frame.add' 
	},
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
		slug:'',
		language:''

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
		return md5( JSON.stringify( serie.settings ) )
	}

	/*
		Serie Magic callback.
	*/
	this.load = function( result ){
		$( serie.settings.target_selector ).empty();
		serie.settings.frames = []

		oo.log( "[serie:oo.rice.Serie] load", result );
		$("#timeline-serie .title").text( result.object.title + '(' + result.object.frames.length + ')');

		serie.open();
	}


	this.sync = function(){
		// save and draw or
		// draw and save
		$( serie.settings.target_selector ).empty();
		for( f in serie.settings.frames ){
			$( serie.settings.target_selector ).append( this.settings.frames[f].html() );
		}
	}


	this.open = function(){
		// has a serie ?
		
		$("#timeline-serie").css({bottom:0});
		
	}

	this.close = function(){
		$("#timeline-serie").css({bottom:'-84px'});
		
	}
	/*
		Empty current timeline, load serie frames on timeline.
		n.b. trigger a serie.changed.
	*/
	this.change = function( event, data ){
		serie.close();
		oo.log( "[serie:oo.rice.Serie] change", event, data );
		serie.settings.slug = data.slug;
		oo.api.serie.get({ id: data.id }, serie.load );
	}

	this.add = function( event ){
		$('#add-serie-modal').reveal(); $("#id_add_serie_title_en").focus();
	}

	/*
		@param frames -	
	*/
	this.set_frames = function( frames ){
		oo.log( "[serie:oo.rice.Serie] set_frames", this.settings );
		// compare version. 

		this.settings.frames = []
		
		for( f in frames ){
			this.settings.frames.push( oo.rice.Frame( frames[f] ) );
		}
	}

	this.add_frame = function( event, frame ){
		
	
		// add and send
		oo.log( "[serie:oo.rice.Serie] add_frame", frame );
		serie.settings.frames.push( frame );
		serie.sync();
	};

	this.init = function(){
		oo.log( "[serie] init", serie.settings );

		// intitialize history
		serie.history = new oo.rice.History()

		// initialize sortable
		$( serie.settings.target_selector ).sortable({
		    revert: true,
		    update: function(event, ui) {
		        if ($(ui.item).hasClass('draggable')) {
		            
		        }
		    }
		});

		$( serie.settings.source_selector ).draggable({
		    connectToSortable: serie.settings.target_selector,
		    helper: 'clone',
		    revert: 'invalid',
		    start: serie.open
		});

		$('ul, li').disableSelection();


		// enable listeners
		oo.on( oo.rice.events.add_frame, serie.add_frame );
		oo.on( oo.rice.events.serie.change, serie.change );
		oo.on( oo.rice.events.serie.add, serie.add )
		

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
			"#" + this.settings.slug
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