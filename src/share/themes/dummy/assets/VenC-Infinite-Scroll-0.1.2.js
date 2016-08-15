var __VENC_notBusy__ = 0;

function __VENC_pushColumns__() { // AJAX stuff
	var __VENC_xmlhttp__;
	if (window.XMLHttpRequest) { // code for IE7+, Firefox, Chrome, Opera, Safari
		__VENC_xmlhttp__ = new XMLHttpRequest();
	}
	else { // code for IE6, IE5
		__VENC_xmlhttp__ = new ActiveXObject("Microsoft.XMLHTTP");
	}
	__VENC_xmlhttp__.onreadystatechange= function() {
		if (__VENC_xmlhttp__.readyState == 4 && __VENC_xmlhttp__.status == 200) {
			xmlDoc = document.implementation.createHTMLDocument('');
			xmlDoc.body.innerHTML = __VENC_xmlhttp__.responseText;
			currentColumns = document.getElementsByClassName("__VENC_COLUMN__");
			newColumns = xmlDoc.getElementsByClassName("__VENC_COLUMN__");
			for (i=0; i < currentColumns.length; i++) {
				newEntries = newColumns[i].getElementsByClassName("entry");
				entriesClones = Array();
				for (j=0; j < newEntries.length; j++) {
					entriesClones.push( newEntries[j].cloneNode(true));
				}
				for(j=0; j < entriesClones.length; j++) {
					images = entriesClones[j].getElementsByTagName("img");
					for (k=0; k < images.length; k++) {
						images[k].parentNode.style.opacity = "0.0";
						window.__VENC_notBusy__++;
						images[k].onload = function(e) {
							e.target.parentNode.style.opacity = "1";
							window.__VENC_notBusy__--;
						}
					}
					currentColumns[i].appendChild(entriesClones[j]);
				}
			}
		}
	}
	__VENC_xmlhttp__.open("GET","index"+__VENC_pageNumber__+".html",true);
	__VENC_pageNumber__++;
	__VENC_xmlhttp__.send();
}

function __VENC_initPageOffset__() {
	currentFilename = window.location.pathname.split('/')[window.location.pathname.split('/').length-1];
	if (currentFilename == '' | currentFilename == "index.html")
		currentFilename = '0';
	else if (currentFilename.replace( /[.html0123456789]+/g, '') != "index") {
		return;
	}
        return parseInt(currentFilename.replace( /^\D+/g, '').replace( /[.html]+/g,''))+1;
}

function __VENC_InfiniteScroll__(e) { // Flow control
	console.log(window.__VENC_notBusy__);
        try {
	  if (window.__VENC_notBusy__ == 0) {
	    document.getElementById("__VENC_LOADING__").style.opacity = "0";
	  }
	  else {
	    document.getElementById("__VENC_LOADING__").style.opacity = "1";
	  }
        }
        catch (e) {
          console.log("There is no __VENC_LOADING__ element.");
        }
	currentColumns = document.getElementsByClassName("__VENC_COLUMN__");
	viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
	for (i=0; i < currentColumns.length; i++) {
		if (currentColumns[i].clientHeight <= viewPortHeight + window.pageYOffset) {
			if (window.__VENC_notBusy__ == 0) {
				__VENC_pushColumns__();
				return 1;
			}
		}
	}
	return 0;	
}

function __VENC_preLoading__() {
        try {
	  document.getElementById("__VENC_NAVIGATION__").setAttribute("style","display: none;");
	}
        catch (e) {
          console.log("There is no __VENC_NAVIGATION__ element.");
        }
        window.__VENC_timer__ = setInterval(__VENC_InfiniteScroll__, 250);
}

var __VENC_pageNumber__ = __VENC_initPageOffset__();

if (document.addEventListener) {
  document.addEventListener("DOMContentLoaded", __VENC_preLoading__, false);
}

else if (/WebKit/i.test(navigator.userAgent)) { // sniff
  var _timer = setInterval(function() {
    
    if (/loaded|complete/.test(document.readyState)) {
      __VENC_preLoading__();
    }
  }, 250);
}

window.onload = __VENC_preLoading__;
//window.onscroll = __VENC_InfiniteScroll__;
