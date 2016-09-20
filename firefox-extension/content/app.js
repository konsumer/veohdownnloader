var veohdownloader_debug = true;
var veoh_downloader;

// runs veoh API function
veoh_api = function(method, params, options){
	var apiKey = '4D3E42EC-F10C-4172-A176-D30B468A6972';
	url = 'http://www.veoh.com/rest/v2/execute.xml?method=veoh.' + method + '&' + params + '&apiKey=' + apiKey;
	
	xmlHttpReq = new XMLHttpRequest();
	xmlHttpReq.open('GET', url , true);
	xmlHttpReq.overrideMimeType('text/xml');
	xmlHttpReq.setRequestHeader('User-Agent', 'veohplugin-1.1.1 service (NT 5.1; IE 7.0; en-US Windows)');
	xmlHttpReq.setRequestHeader('Content-Type', 'application/xml; charset=utf-8');
	for (o in options){
		xmlHttpReq[o] = options[o];
	}	
	xmlHttpReq.send(null);
	return xmlHttpReq;
}


// loaded on each page load
function veohdownloader_pageLoad(aEvent){	
	var doc = aEvent.originalTarget;
	try {
		// this only parses /videos/v6525744grmT6Jhz style URLs, for now
		// this is also really page-specific, maybe I could make this a status icon, instead...
		if (doc.location.host == 'www.veoh.com'){
			if (doc.location.pathname.search(/videos\/[0-9a-z]+/) != -1){			
				jQuery('div.feedback', doc).hide();
				jQuery('#actions', doc).append('<a style="margin:12px; padding: 2px 20px; background: #fff url(\'http://www.veoh.com/favicon.ico\') 0 0 no-repeat;" id="veohdownloaderlink" href="#">watch with Veoh Downloader</a>');
				jQuery("#veohdownloaderlink", doc).click(function(){
					// get info, use ipod url to download movie
					var options = {
						onreadystatechange : function(){
							if (this.readyState == 4) {
								$('video', this.responseXML).each(function(){
									for (a in this.attributes){
										if (this.attributes[a].name == 'ipodUrl'){
											// change user-agent, then location
											var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
                    						prefs.setCharPref("general.useragent.override", "Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3");
											
											content.location = this.attributes[a].value;
											break;
										}
									}
								});
							}
						}
					};
					veoh_api('video.findByPermalink','permalink=' + doc.location.pathname.split('/')[2], options);			
					return false;
				});
			}
		}
	}catch(e){
		if (Firebug.Console && veohdownloader_debug){
			Firebug.Console.log(e);
		}
	}
}

// add listener on first load (plugin start.)
try{window.addEventListener("load", function(){
	document.getElementById("appcontent").addEventListener("DOMContentLoaded", veohdownloader_pageLoad, true);
}, true);}catch(e){}
