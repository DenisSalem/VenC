var VENC_INFINITE_SCROLL = {
	queue: 0,
	end: false,
	hideVenCNavigation: true,
	pageHook : "",
	interval : 250,
	xmlhttp : Object,
	timer: Object,
	imageDefaultSetup: function(img) {},
	entryDefaultSetup: function(entry) {
		entry.style.opacity = "0.0";
	},
	onLoadImage: function(img) {},
	onLoadEntry: function(entry){
		entry.style.transition = "opacity 0.5s ease";
		entry.style.opacity = "1.0";
	},
	loading : function() {
		try {
			document.getElementById("__VENC_LOADING__").style.opacity = "1";
		}
		catch (e) {
			console.log("VenC: There is no __VENC_LOADING__ element.");
		}
	},
	idle : function() {
		try {
			document.getElementById("__VENC_LOADING__").style.opacity = "0";
		}
		catch (e) {
			console.log("VenC: There is no __VENC_LOADING__ element.");
		}
	},
	getPageHook : function() {
		v = document.querySelectorAll('[data-venc-api-infinite-scroll-hook]')
		if (v.length == 1) {
			this.pageHook = v[0].dataset.vencApiInfiniteScrollHook;
			console.log("VenC: Hook", this.pageHook);
		}
		else if (v.length > 1) {
			console.log("VenC: There is more than one infinite scroll hook in DOM. Aborting...")
		  	this.end = true;
			return

		}
		else {
		  	console.log("VenC: Infinite Scroll hook not found. Exiting...");
		  	this.end = true;
			return;
		}
	},
	getContent : function() {
		if (window.XMLHttpRequest) { // code for IE7+, Firefox, Chrome, Opera, Safari
			this.xmlhttp = new XMLHttpRequest();
		}
		else { // code for IE6, IE5
			this.xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
		}
		this.xmlhttp.onreadystatechange = this.domUpdate;
		this.xmlhttp.open("GET", this.pageHook, true);
		this.xmlhttp.send();
	},
	dontWait: false,
	currentLocation : Object,
	domUpdate : Object
};

function VENC_INFINITE_SCROLL_UPDATE_DOM() {
	if (VENC_INFINITE_SCROLL.xmlhttp.readyState == 4 && VENC_INFINITE_SCROLL.xmlhttp.status == 200) {
		xmlDoc = document.implementation.createHTMLDocument('');
		xmlDoc.body.innerHTML = VENC_INFINITE_SCROLL.xmlhttp.responseText;
		currentColumns = document.getElementsByClassName("__VENC_COLUMN__");
		newColumns = xmlDoc.getElementsByClassName("__VENC_COLUMN__");
		for (i=0; i < currentColumns.length; i++) {
			newEntries = newColumns[i].getElementsByClassName("entry");
			entriesClones = Array();
			for (j=0; j < newEntries.length; j++) {
				entriesClones.push( newEntries[j].cloneNode(true));
			}
			for(j=0; j < entriesClones.length; j++) {
				VENC_INFINITE_SCROLL.entryDefaultSetup(entriesClones[j]);
				images = entriesClones[j].getElementsByTagName("img");
				if (images.length == 0) {
					VENC_INFINITE_SCROLL.onLoadEntry(entriesClones[j]);
				}
				else {
					for (k=0; k < images.length; k++) {
						VENC_INFINITE_SCROLL.queue++;
						VENC_INFINITE_SCROLL.imageDefaultSetup(images[k]);
						images[k].loaded = false;
						images[k].onerror = function(e) {
							this.onload(e);
						}
						images[k].onload = function(e) {
					  		this.loaded = true;
							VENC_INFINITE_SCROLL.queue--;
							VENC_INFINITE_SCROLL.onLoadImage(this);

							for(l = 0; l < images.lenght; l) {
								if (images[l].loaded == false) {
									return;
								}
							}
							VENC_INFINITE_SCROLL.onLoadEntry(this.closest(".entry"));
						}

						d = new Date()
						images[k].src = images[k].src+"?uglyWorkAround="+d.getTime();
					}
				}
				currentColumns[i].appendChild(entriesClones[j]);
			}
		}
		// Update Hook
		new_hook = xmlDoc.querySelectorAll('[data-venc-api-infinite-scroll-hook]')
		old_hook = document.querySelectorAll('[data-venc-api-infinite-scroll-hook]')
		if (new_hook.length == 1) {
			// There is no verificaton because hook exists at this point of code.
			oh = old_hook[0];
			old_hook_parent = oh.parentNode;
			old_hook_parent.replaceChild(new_hook[0], oh);
			VENC_INFINITE_SCROLL.getPageHook();
		}
		else {
			console.log("VenC: Infinite Scroll hook not found. Exiting...");
			VENC_INFINITE_SCROLL.end = true;
		}

	}
};

function VENC_INFINITE_SCROLL_RUN() {
  	if (VENC_INFINITE_SCROLL.end) {
		clearInterval(VENC_INFINITE_SCROLL.timer);
		console.log("VenC: Done.")
		return;
	}
	if (VENC_INFINITE_SCROLL.queue == 0) {
		VENC_INFINITE_SCROLL.idle();
	}
	else {
		VENC_INFINITE_SCROLL.loading();
	}
	currentColumns = document.getElementsByClassName("__VENC_COLUMN__");
	viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
	for (i=0; i < currentColumns.length; i++) {
		if (currentColumns[i].clientHeight <= viewPortHeight + window.pageYOffset) {
			if ((VENC_INFINITE_SCROLL.queue == 0 || VENC_INFINITE_SCROLL.dontWait) && !VENC_INFINITE_SCROLL.end) {
				VENC_INFINITE_SCROLL.getContent();
				return 1;
			}
		}
	}
	return 0;
};

function VENC_INFINITE_SCROLL_ON_LOAD() {
	VENC_INFINITE_SCROLL.currentLocation = window.location.pathname.split('/')[window.location.pathname.split('/').length-1]
	VENC_INFINITE_SCROLL.getPageHook()
	if (VENC_INFINITE_SCROLL.hideVenCNavigation) {
       		try {
	 	 	document.getElementById("__VENC_NAVIGATION__").setAttribute("style","display: none;");
		}
       		catch (e) {
       			console.log("VenC: There is no __VENC_NAVIGATION__ element.");
       		}
	}
	if (VENC_INFINITE_SCROLL.end == false) {
	  	console.log("there")
		VENC_INFINITE_SCROLL.domUpdate = VENC_INFINITE_SCROLL_UPDATE_DOM;
		VENC_INFINITE_SCROLL.timer = setInterval(VENC_INFINITE_SCROLL_RUN, VENC_INFINITE_SCROLL.interval);
	}
};

