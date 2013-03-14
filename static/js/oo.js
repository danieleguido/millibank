

var oo = oo || {};
oo.vars = oo.vars || {};
oo.urls = oo.urls || {};

/*


    Logs
    ====

*/
oo.log = function(){
	try{
		console.log.apply(console, arguments);
	} catch(e){
			
	}
}

/*


	WINDOW On / Trigger helpers
	===========================
*/
oo.on = function( eventType, callback ){
	$(window).on( eventType, callback );
};

oo.trigger = function ( eventType, data ){
	$(window).trigger( eventType, data );
};


/*


    Restful API
    ===========

*/
oo.api = { 
	settings:{
		'get':{dataType:"Json",type:"GET",fault:oo.fault } ,
		'post':{dataType:"Json",type:"POST",fault:oo.fault }
	}
};

oo.api.init = function(){
	oo.vars.csrftoken = oo.fn.get_cookie('csrftoken');
	$.ajaxSetup({
		crossDomain: false, // obviates need for sameOrigin test
		beforeSend: function(xhr, settings) { if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type))){ xhr.setRequestHeader("X-CSRFToken", oo.vars.csrftoken);}}
	});oo.log("[oo.api.init]");
}

oo.api.process = function( result, callback, namespace ){
	if( result.status == 'ok'){
		if (typeof callback == "object"){
			oo.toast( callback.message, callback.title );
		} else return callback( result );
	} else if( result.code == 'IntegrityError' ){
		$("#"+namespace+"_slug").addClass("invalid");
		oo.toast(  oo.i18n.translate("this slug is already used") , oo.i18n.translate("error"), {stayTime:3000, cleanup: true});
	} else if( typeof result.error == "object" ){
		oo.invalidate( result.error, namespace );
		oo.toast(  oo.i18n.translate("invalid form") , oo.i18n.translate("error"), {stayTime:3000, cleanup: true});
	} else {
		oo.toast( result.error , oo.i18n.translate("error"), {stayTime:3000, cleanup: true});
	}
}

oo.api.urlfactory = function( url, factor, pattern ){
	if( typeof factor == "undefined" ){ ds.log("[ds.m.api.urlfactory] warning'"); return url; };
	pattern = typeof pattern == "undefined"? "/0/":pattern ;
	return url.replace( pattern, ["/",factor,"/"].join("") )
}

/*
	Handle with care. 
	This function add a add+edit+remove+get function to oo.api.<your model>
	E.g to add a filter to oo.api.serie.get:

		oo.api.compile('serie');
		
		oo.magic.serie.list = function( result ){
			alert('list');
		}

		oo.api.serie.list({
			'filters': JSON.stringify({
				"language":"fr"
			})
		});

	Cfr. oo.api.Builder

	@param model	- your model, a.k.a oo.api namespace
 	
*/
oo.api.compile = function( model ){ oo.log( '[oo.api.compile ]', model );
	oo.api[ model ] = new oo.api.Builder( model )
}

oo.api.Builder = function( model ){

	var instance = this;
	
	this.methods = [ 'get', 'list', 'add', 'remove', 'edit' ];
	this.model = model;



	this.get = function( params, callback ){

		instance.ajax( 'get', 'get', params, oo.api.urlfactory( oo.urls[ 'get_' + instance.model ], params.id ), callback  );
	}

	this.list = function( params ){
		instance.ajax( 'get', 'list', params, oo.urls[ 'list_' + instance.model ] );
	}

	this.add = function( params ){
		instance.ajax( 'post', 'add', params, oo.urls[ 'add_' + instance.model ] );
	}

	this.remove = function( params ){
		instance.ajax( 'delete', 'remove', params, oo.api.urlfactory( oo.urls[ 'remove_' + instance.model ], params.id ) );
	}

	this.ajax = function( http_method, method, params, url, callback ){
		oo.log( '[oo.api.' + instance.model + '.' + method + '] url :', url, ", params :",params );
		$.ajax( $.extend( oo.api.settings[ http_method ],{
			url: url,
			data: params,
			success:function(result){ oo.log( '[oo.api.' + instance.model + '.' + method + '] result :', result );
				oo.api.process( result, typeof callback == "undefined" ? oo.magic[ instance.model ][ method ]: callback, typeof params.auto_id == "undefined"? "id_" + method + "_" + instance.model: params.auto_id );
		}}));
	}

	// check urls availability
	for( i in instance.methods ){
		oo.log('[oo.api.Builder:' + instance.model +']', 'urls ', instance.methods[i] + '_' + instance.model, ":", typeof oo.urls[ instance.methods[i] + '_' + instance.model ] != "undefined" )
	}

}


/*


    Modals (Bootstrap)
    ==================

*/
oo.modals = {}
oo.modals.init = function(){ 
	$(".modal").each( function( i, el ){ var $el = $(el); $(el).css("margin-top",- Math.round( $(el).height() / 2 )); }); oo.log("[oo.modals.init]");
};


/*


    Tooltip
    =======

*/
oo.tooltip = {}
oo.tooltip.init = function(){
	$('body').tooltip({ selector:'[rel=tooltip]', animation: false, placement: function( tooltip, caller ){ var placement = $(caller).attr('data-tooltip-placement'); return typeof placement != "undefined"? placement: 'top'; } }); oo.log("[oo.tooltip.init]");};


/*


    Toast
    =====

*/
oo.toast = function( message, title, options ){
	if(!options){options={}}if(typeof title=="object"){options=title;title=undefined}if(options.cleanup!=undefined)$().toastmessage("cleanToast");var settings=$.extend({text:"<div>"+(!title?"<h1>"+message+"</h1>":"<h1>"+title+"</h1><p>"+message+"</p>")+"</div>",type:"notice",position:"middle-center",inEffectDuration:200,outEffectDuration:200,stayTime:3e3},options);$().toastmessage("showToast",settings)
};


/*


    Invalidate, Fault
    =================

*/
oo.invalidate = function( errors, namespace ){ if (!namespace){ namespace = "id";} oo.log("[oo.invalidate] namespace:",namespace, " errors:",errors );
	for (var i in errors){
		if( i.indexOf("_date") != -1  ){
			$("#"+namespace+"_"+i+"_day").parent().addClass("invalid");	
			continue;
		} else if (i.indexOf("_type") != -1 ){
			$("#"+namespace+"_"+i).parent().addClass("invalid");
			continue;
		} else if( i.indexOf("_hours") != -1 || i.indexOf("_minutes") != -1  ) {
			$("#"+namespace+"_"+i).parent().addClass("invalid");
			continue;	
		} else if(i.indexOf("captcha") != -1 ) {
			$("#recaptcha_response_field").addClass("invalid");
			continue;
		}
		$("#"+namespace+"_"+i).addClass("invalid");
	}
}

oo.fault = function( message ){
	oo.log("[ds.m.handlers.fault] message:", message );	
	message = typeof message == "undefined"? "": message;
	oo.toast( message, oo.i18n.translate("connection error"), {stayTime:3000, cleanup: true});
}


/*


    Common function
    ===============

*/
oo.fn = {};
oo.fn.slug = function( sluggable ){
	return sluggable.replace(/[^a-zA-Z 0-9-]+/g,'').toLowerCase().replace(/\s/g,'-');
};

oo.fn.get_cookie = function (e){
	var t=null;if(document.cookie&&document.cookie!=""){var n=document.cookie.split(";");for(var r=0;r<n.length;r++){var i=jQuery.trim(n[r]);if(i.substring(0,e.length+1)==e+"="){t=decodeURIComponent(i.substring(e.length+1));break}}}return t
};


/*


    I18n
    ====

*/
oo.i18n = { lang:'fr-FR'};
oo.i18n.translate = function( key ){
	var l = oo.i18n.lang;
	if ( oo.i18n.dict[l][key] == undefined	)
		return key;
	return 	oo.i18n.dict[l][key];
}

oo.i18n.dict = {
	'fr-FR':{
		"connection error":"Connection error",
		"warning":"Attention",
		"delete selected absence":"Voulez-vous supprimer cette absence?",
		"offline device":"Échec de la connexion.",
		"check internet connection":"Veuillez vérifier la connexion internet de la tablette.",
		"welcome back":"welcome back",
		"loading":"chargement en cours…",
		"form errors":"Erreurs dans le formulaire",
		"error":"Erreur",
		"invalid form":"Veuillez vérifier les champs en rouge.",
		"empty dates":"Les dates de dé en rouge.",
		"empty message field":"Le message est vide.",
		"message sent":"Message envoyé",
		"timeout device":"Connexion trop lente.",
		"try again later": "Veuillez réessayer dans quelques instants.",
		"saving":"enregistrement en cours…",
		"changes saved":"Modifications Sauvegardées",
		"changes saved successfully":"Modifications Sauvegardées",
		"password should be at least 8 chars in length":"Le mot de passe doit faire au moins 8 caractères.",
		"password too short":"Le mot de passe est trop court",
		"password changed":"Le mot de passe a été changé",
		"new passwords not match":"Saisissez à nouveau le nouveau mot de passe.",
		"invalid password":"Veuillez vérifier votre ancien mot de passe en respectant les minuscules et les majuscules.",
		"sms message sent":"SMS envoyé(s) avec succès.",
		"sms message sent failed":"Le SMS n'a pas pu être envoyé.",
		"sms invalid message":"Le texte du SMS est invalide.",
		"sms invalid phone numbers":"Numéro(s) de téléphone invalide(s)",
		"list numbers sms failure":"Certains SMS n'ont pu être envoyés.",
		"to change password": "Veuillez changer votre <br/> <b>mot de passe</b>",
		"please check accepted terms": "Veuillez accepter les conditions d'utilisation",

	}
};


/*


    Bibtex
    ======

*/
oo.fn.bibtex = function ( bibtex ){
	var bibjson = bibtex.replace(/(\w+)\s*=\s*\{+/g,"\"$1\": \"")
		.replace(/\}+(?=\s*[,\}+])/g,"\"")
		.replace(/@(\w+)\s*\{([^,]*)/,"{\"bibtext_key\":\"$1\",\"$1\": \"$2\"");
	oo.log( bibjson )
	return JSON.parse(bibjson);
}