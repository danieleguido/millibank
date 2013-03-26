/*
	GRAIN
	a small and simple template engine. Alternative to ember.js or angular.
	

	1. create somewhere on page your element with data-object attribute. This will be your 
		base template for 'serie' objects

	<div data-object='serie'>
		<h3>(( title ))</h3>
		<h3>(( title ))</h3>
		<h3>(( title ))</h3>
		<ul data-for-object='serie.frame'>
			
		</ul>
	</div>
	
	2. handle list of objects

	<ul data-for-object='serie'>
		
	</ul>
	
	3. 

*/

var oo = oo || {}; 

oo.grain = {}

oo.grain.templates = {}

oo.grain.templatetags = {
	url:function( factor, args ){
		return oo.api.urlfactory( args[0], factor )
	},
	loop:function( items, args ){
		oo.log( items, args )
		var template = args[0];

		el = $("<div/>")

		for (var i in items){

			oo.log(oo.grain.templates[ template ], items[i])
			el.append( oo.grain.templates[ template ].load( items[i] ) )
		}
		return el.html()  
		// call a template engine foreach
	},
	length: function(a){
		return a.length
	}
}


oo.grain.register = function(a, i){
	var el = $(this)

	var t  = el.attr( 'data-object' );

	if ( typeof oo.grain.templates[ t ] == "undefined" ){
		oo.grain.templates[ t ] = new oo.grain.Template({ type:t, element:el }); 
	}

	oo.log(el.attr( 'data-object' ));
}

oo.grain.init = function(){
	// load template in page
	$('*[data-object]').each( oo.grain.register );
}


oo.grain.transform =  function( el, object ){
	
	var d = /\(\(\s?([\d\w-_\.]+)\s?\)\)/g;
	// with function... eval? split with |, args with "," so don't use it
	var fn = /\(\(\s?([\d\w-\|_,\/\.]+)\s?\)\)/g;

	var str = "" + el.clone().wrap('<p>').parent().html().replace(d, function(){
		return typeof object[  arguments[1] ] != "undefined"? object[  arguments[1] ]: arguments[0];
	}).replace(fn, function(){
		args = arguments[1].split("|")
		if (args.length < 2 || typeof oo.grain.templatetags[ args[0] ] == "undefined"){
			return arguments[0]; // no templatetags...!
		}
		
		var func = oo.grain.templatetags[ args.shift() ];
		var item = object[ args.shift() ]
		
		return func( item, args );
		
	});
	el.replaceWith( str );
	return str;
}

oo.grain.Template = function( options ){
	var h = this;
	
	this.settings = $.extend({
		type:'',
		id:'',
		element:''
	}, options );

	this.init = function(){
		oo.log( "[oo.grain.Template:"+this.settings.type+"]", this.settings.type )
	}


	this.load = function( object ){
		var el = h.settings.element.clone()

		return oo.grain.transform( el.show(), object );
		// returna cloned element
	}

	this.html = ''

	h.init()
}