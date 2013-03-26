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
oo.rice.listeners = {};


oo.rice.listeners.append_frame = function( event ){
	var frame = $(this);
	oo.trigger( oo.rice.events.frame.append, new oo.rice.Frame({
		id: frame.attr('data-id'),
		title: frame.attr('data-title'),
		mimetype: frame.attr('data-mimetype'),
		page_slug: [ frame.attr('data-page-slug') ],
		slug: frame.attr('data-slug')
	}));
};

oo.rice.dragstart = function( event ){
	$("#actual-serie").height( 40 );
}



oo.rice.init = function(){oo.log("[oo.rice.init]");
	
	// compile api callers:
	oo.api.compile( 'serie' );

	// load last serie from cookie
	oo.rice.serie = new oo.rice.Serie({ 
		autoload:true,
		id: 0
	});

	// start global listeners: append frame
	$(document).on("click",".append-frame", oo.rice.listeners.append_frame );

	// use serie
	$(document).on("click",".change-serie", function(event){ oo.trigger( oo.rice.events.serie.change, { id: $(this).attr('data-id')});});
	

	$("*[data-make-small=parent]").click( function(){ $(this).parent().css("left","-40%"); });

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
		append:'oo.rice.events.frame.append',
		add: 'oo.rice.events.frame.add' 
	}
};

/*


    Serie Class
    ===========

*/
oo.rice.Serie = function( options ){

	var serie = this

	this.settings = $.extend({
		autoload: false,
		collection: '.frames',
		modal: '#serie-viewer',
		frames:[],
		slug:'',
		language:'',
		id: 0
	}, options );

	this.quasi_frames = [];

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
		return md5( JSON.stringify( serie.settings ) );
	};

	/*
		Serie Magic callback.
	*/
	this.load = function( result ){
		serie.settings.frames = [];
		// when here, result.status = "ok"
		


		oo.grain.transform( $(serie.settings.modal), result['objects'][0] )


		
		serie.open();
	};

	/*
		Listener for oo.rice.events.frame.append event
		It expects an object of type oo.rice.Frame to be delivered.
	*/
	this.append_frame = function( event, frame ){

		oo.log( serie.settings.id);
		if (serie.settings.id == 0){
			// load last saved serie
			oo.api.serie.list({limit:1, order_by:'["-date_last_modified"]'}, serie.load );
			serie.quasi_frames.push( frame );
			return
		}

		$(serie.settings.modal).show();

		// add and send
		oo.log( "[serie:oo.rice.Serie] append_frame to ", frame, serie.settings.collection );
		serie.settings.frames.push( frame );
		
		for (i in serie.settings.frames){
			serie.settings.frames[i].settings.sort = i;
		}

		$( serie.settings.collection ).append( frame.html() );

		// draw directly at the very end
		oo.fn.wait( serie.sync, 1000 );

	};

	/*
		This function export to the REST api the current set of frames.

	*/
	this.sync = function(){
		var url = oo.api.urlfactory( oo.urls.sync_serie, serie.settings.id );
		oo.log("[serie:oo.rice.Serie] sync: ", url);
		
		

		// oo.urloo.urls.sync_serie()
		$.ajax( $.extend( oo.api.settings.post,{
			url: url,
			data:{
				frames:'[' + oo.rice.serie.settings.frames.join(',') +']'
			},
			success:function(result){
				oo.log( '[serie:oo.rice.Serie]', result );
				oo.api.process( result, serie.update );
			}
		}));

	};

	this.update = function( result ){

	}

	this.open = function(){
		$(serie.settings.modal).show().draggable();
		$(serie.settings.modal + " .frames").sortable();
		
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


	

	this.init = function(){
		oo.log( "[serie] init", serie.settings );

		// intitialize history
		serie.history = new oo.rice.History()

		

		// start sortable plugin
		$( serie.settings.collection ).sortable();


		// autoload!
		// http://127.0.0.1:8000/api/serie/?limit=1&order_by=[%22-date_last_modified%22]


		// start listeners
		oo.on( oo.rice.events.frame.append, serie.append_frame );


	}

	this.init();
}


/*


    Frame Class
    ===========

*/
oo.rice.Frame = function( options ){
	
	var frame = this;

	this.settings = $.extend({
		id:0,
		mimetype: 'text/plain',
		slug: '', // frame object as it comes from api/frame
		page_slug:[],
		title:'',
		role:'Te',
		sort:0
	}, options );

	this.props = function(){
		return this.settings
	}

	

	this.html = function(){
		if( typeof frame.el == "undefined" ){

		

			frame.el = $("<div/>",{ 'class':'frame ' + frame.settings.role + ' ' + frame.settings.page_slug.join('-') }).append(
				'<div class="icon"></div>',
				'<div class="title">' + frame.settings.title +'</div>',
				'<div class="counter-wrapper"><div class="counter">' + frame.settings.sort + '</div></div>'
			);
		};
		return frame.el;
	}

	this.toString = function(){
		return JSON.stringify( frame.settings );
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