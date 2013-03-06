var oo = oo || {}; oo.rice = {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};



/*


    Rice UI
    =======

*/
oo.rice = oo.rice || {};

oo.rice.dragstart = function( event ){
	$("#actual-serie").height( 40 );
}

oo.rice.append = function( event ){
	if (typeof oo.rice.serie == "undefined" ){
		// default serie
		oo.rice.serie = new oo.rice.Serie();
	}
	oo.trigger( oo.rice.events.append, {what:'me'});
}

oo.rice.init = function(){oo.log("[oo.rice.init]");
	
	// load last serie from cookie
	oo.rice.serie = new oo.rice.Serie({ autoload:true });

	$(document).on('click','.drag-to-serie',oo.rice.append );


}

oo.rice.events = {
	    'append':'oo.rice.events.add',
	 'change':'oo.rice.events.change',
	  'clean':'oo.rice.events.clean',
	   'init':'oo.rice.events.init',
	'replace':'oo.rice.events.replace',
	 'remove':'oo.rice.events.remove',
	  'reset':'oo.rice.events.reset'
};

/*


    Serie Class
    ===========

*/
oo.rice.Serie = function( options ){


	this.settings = $.extend({
		autoload: false
	}, options );

	this.append = function( event, data ){
		oo.log( event, data );
	};

	this.init = function(){
		// if options.autoload:

		oo.log( "[oo.rice.Serie] Serie object created", this.settings );

		// enable listeners
		
		oo.on( oo.rice.events.append, this.append );
	}

	this.init();
}