/*
 * Copyright 2016, 2023 Denis Salem
 * 
 * This file is part of VenC.
 * 
 * VenC is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.

 * VenC is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with VenC.  If not, see <http://www.gnu.org/licenses/>.
 */

var VENC_INFINITE_SCROLL = {
	queue: 0,
	end: false,
	hideVenCNavigation: true,
	pageHook : "",
	interval : 250,
	xmlhttp : Object,
	timer: Object,
    loading_image : undefined,
	imageDefaultSetup: function(img) {},
	entryDefaultSetup: function(entry) {
		entry.style.opacity = "0.0";
	},
	onLoadImage: function(img) {},
	onLoadEntry: function(entry){
		entry.style.opacity = "1.0";
	},
	loading : function(loading_image) {
        loading_image.style.opacity = "1.0";
    },
	idle : function(loading_image) {
        loading_image.style.opacity = "0";
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
        if (VENC_INFINITE_SCROLL.loading_image != undefined) {
            VENC_INFINITE_SCROLL.loading_image.style.display = "none";
        }
        return;
	}
	if (VENC_INFINITE_SCROLL.queue == 0) {
        if (VENC_INFINITE_SCROLL.loading_image != undefined) {
            VENC_INFINITE_SCROLL.idle(VENC_INFINITE_SCROLL.loading_image);
        }
	}
	else {
        if (VENC_INFINITE_SCROLL.loading_image != undefined) {
            VENC_INFINITE_SCROLL.loading(VENC_INFINITE_SCROLL.loading_image);
        }
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
    try {
        VENC_INFINITE_SCROLL.loading_image = document.getElementById("__VENC_LOADING__");
        VENC_INFINITE_SCROLL.loading_image.style.display = "block";
        VENC_INFINITE_SCROLL.loading_image.style.opacity = "0";

    }
    catch (e) {
        console.log("VenC: There is no __VENC_LOADING__ element.");
    }
	VENC_INFINITE_SCROLL.currentLocation = window.location.pathname.split('/')[window.location.pathname.split('/').length-1]
	VENC_INFINITE_SCROLL.getPageHook()
	if (VENC_INFINITE_SCROLL.hideVenCNavigation) {
        try {
	 	 	document.getElementById("__VENC_NAVIGATION__").style.display = "none";
		}
        catch (e) {
            console.log("VenC: There is no __VENC_NAVIGATION__ element.");
        }
	}
	if (VENC_INFINITE_SCROLL.end == false) {
		VENC_INFINITE_SCROLL.domUpdate = VENC_INFINITE_SCROLL_UPDATE_DOM;
		VENC_INFINITE_SCROLL.timer = setInterval(VENC_INFINITE_SCROLL_RUN, VENC_INFINITE_SCROLL.interval);
	}
};

VENC_ON_LOAD_CALLBACK_REGISTER.push(VENC_INFINITE_SCROLL_ON_LOAD);
