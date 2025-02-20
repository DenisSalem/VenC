/*
 * Copyright 2016, 2024 Denis Salem
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
 
var VENC_MEDIA_VIEWER = {
    version: "0.0.0",
    wrapper : null,
    image: null,
    video: null,
    close_button: null,
    carousel: null,
    title: null,
    image_extensions: ["jpg","jpeg","png","gif","apng","bmp","avif","svg","webp","jfif","pjpeg","pjp"],
    video_extensions: ["mp4","ogg","ogv","3gp","webm","mpeg","mov"],
    mesh_extensions: ["stl"],
    context: null,
    interval: 250,
    timer : null,
    medias : null,
    media_index : 0,
    item_index : 0,
    next_button : "→",
    previous_button : "←",
    items: [],
    x_touch_start: null,
    x_touch_diff: null
}

function VENC_MEDIA_VIEWER_REFRESH_CONTENTS() {
    VENC_MEDIA_VIEWER_BIND_CALLBACK(document);
}

function VENC_MEDIA_VIEWER_CAROUSEL_ONCLICK(event) {
    event.stopPropagation();
    VENC_MEDIA_VIEWER.media_index = this.dataset.media_index;
    return VENC_MEDIA_VIEWER_SET_MEDIA(this.dataset.media_index);
}

function VENC_MEDIA_VIEWER_SET_MEDIA(media_index) {
    // TODO : In up coming version allow consumer to write positionnment callback

    console.log(VENC_MEDIA_VIEWER.wrapper.className);
    
    VENC_MEDIA_VIEWER.medias = JSON.parse(
        VENC_MEDIA_VIEWER.context.dataset.vencMediaViewerContents
    )
    
    if ( VENC_MEDIA_VIEWER.item_index === 0 && media_index === 0) {
		    VENC_MEDIA_VIEWER.previous_button.className = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_PREVIOUS_DEACTIVATED";
    } else {
        VENC_MEDIA_VIEWER.previous_button.className = "";
    }
    
    VENC_MEDIA_VIEWER.carousel.innerHTML = "";

    has_title = VENC_MEDIA_VIEWER.context.dataset.hasOwnProperty("vencMediaViewerTitle") && VENC_MEDIA_VIEWER.context.dataset.vencMediaViewerTitle.length > 0;

    if (has_title) {
        VENC_MEDIA_VIEWER.title.innerHTML = VENC_MEDIA_VIEWER.context.dataset.vencMediaViewerTitle;
        VENC_MEDIA_VIEWER.title.style.bottom = VENC_MEDIA_VIEWER.medias.length > 1 ? "0.5em" : "1em";
    }

    if (VENC_MEDIA_VIEWER.medias.length > 1) {
        for (i = 0; i < VENC_MEDIA_VIEWER.medias.length; i++) {
            a = document.createElement('a');
            a.innerHTML = (i == media_index ?  "⬤" : "◯");
            a.className="VENC_MEDIA_VIEWER_CONTENTS_CAROUSEL_BUTTON";
            a.dataset.media_index = i;
            a.href="";
            a.onclick = VENC_MEDIA_VIEWER_CAROUSEL_ONCLICK;
            VENC_MEDIA_VIEWER.carousel.appendChild(a);
        }
        if (has_title) {
            VENC_MEDIA_VIEWER.carousel.style.bottom = has_title ? "2em" : "1em"; 
        }
    }

    var file_extension = VENC_MEDIA_VIEWER.medias[media_index].split('.').pop().toLowerCase();
    
    max_width = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) * 0.9;
    max_height = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0) * 0.9 - 32;
    
    if (VENC_MEDIA_VIEWER.image_extensions.includes(file_extension)) {
        VENC_MEDIA_VIEWER.video.style.display = "none";
        VENC_MEDIA_VIEWER.canvas.style.display = "none";
        VENC_MEDIA_VIEWER.image.style.display = "block";
        VENC_MEDIA_VIEWER.image.src = "";
        VENC_MEDIA_VIEWER.image.style.opacity = "0";
        VENC_MEDIA_VIEWER.image.title = VENC_MEDIA_VIEWER.context.dataset.vencMediaViewerTitle;
        
        var newImg = new Image;
        
        newImg.onload = function() {
            VENC_MEDIA_VIEWER.image.src = this.src;
            VENC_MEDIA_VIEWER.image.style.maxWidth = max_width.toString()+"px";
            VENC_MEDIA_VIEWER.image.style.maxHeight = max_height.toString()+"px";
            VENC_MEDIA_VIEWER.image.style.position = "fixed";
            VENC_MEDIA_VIEWER.image.style.marginLeft = (-VENC_MEDIA_VIEWER.image.width/2).toString()+"px";
            VENC_MEDIA_VIEWER.image.style.marginTop = (-VENC_MEDIA_VIEWER.image.height/2).toString()+"px";
            VENC_MEDIA_VIEWER.image.style.left = "50%";
            VENC_MEDIA_VIEWER.image.style.top = "50%";
            VENC_MEDIA_VIEWER.image.style.opacity = "1";
            VENC_MEDIA_VIEWER.wrapper.className = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_ACTIVATED" 
        }
        
        newImg.src = VENC_MEDIA_VIEWER.medias[media_index];

    }
    else if (VENC_MEDIA_VIEWER.video_extensions.includes(file_extension)) {
        VENC_MEDIA_VIEWER.image.style.display = "none";
        VENC_MEDIA_VIEWER.video.style.display = "none";
        VENC_MEDIA_VIEWER.canvas.style.display = "none";
        VENC_MEDIA_VIEWER.video.autoplay = true;
        VENC_MEDIA_VIEWER.video.loop = true;
        VENC_MEDIA_VIEWER.video.controls = true;

        VENC_MEDIA_VIEWER.video.addEventListener( "loadedmetadata", function (e) {
            VENC_MEDIA_VIEWER.video.style.display = "block";
        
            VENC_MEDIA_VIEWER.video.style.maxWidth = max_width.toString()+"px";
            VENC_MEDIA_VIEWER.video.style.maxHeight = max_height.toString()+"px";

            marginLeft = this.getBoundingClientRect().width >= max_width ? (-max_width/2) : (-this.getBoundingClientRect().width/2);
            marginTop =  this.getBoundingClientRect().height >= max_height ? (-max_height/2) : (-this.getBoundingClientRect().height/2);
            
            VENC_MEDIA_VIEWER.video.style.marginLeft = marginLeft.toString()+"px";
            VENC_MEDIA_VIEWER.video.style.marginRight = "0px";

            VENC_MEDIA_VIEWER.video.style.marginTop = marginTop.toString()+"px";
            
            VENC_MEDIA_VIEWER.video.style.left = "50%";
            VENC_MEDIA_VIEWER.video.style.top = "50%";
            VENC_MEDIA_VIEWER.video.style.opacity = "1";
            VENC_MEDIA_VIEWER.video.style.position = "fixed";

            VENC_MEDIA_VIEWER.wrapper.className = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_ACTIVATED" 

        }, false );
        
        VENC_MEDIA_VIEWER.video.src = VENC_MEDIA_VIEWER.medias[media_index];

    } else if (VENC_MEDIA_VIEWER.mesh_extensions.includes(file_extension)) {
        if (! (typeof VENC_WEB_GL === 'undefined')) {
            VENC_MEDIA_VIEWER.image.style.display = "none";
            VENC_MEDIA_VIEWER.video.style.display = "none";
            scale = Math.min(max_width, max_height);
            VENC_MEDIA_VIEWER.canvas.width = scale;
            VENC_MEDIA_VIEWER.canvas.height = scale;
            VENC_MEDIA_VIEWER.canvas.ready_callback = function() {
                this.style.left = "50%";
                this.style.top = "50%";
                this.style.display = "block";
                this.style.position = "fixed";
                this.style.marginLeft = (-this.width/2).toString()+"px";
                this.style.marginTop = (-this.height/2).toString()+"px";
                VENC_MEDIA_VIEWER.wrapper.className = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_ACTIVATED"
            };
            VENC_WEB_GL.init(canvas, VENC_MEDIA_VIEWER.medias[media_index]);
        }
    }

    VENC_MEDIA_VIEWER.wrapper.className = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_ACTIVATED VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_ON_LOAD";
    return false;
}

function VENC_MEDIA_VIEWER_CALLBACK() {
    VENC_MEDIA_VIEWER.context = this;
    VENC_MEDIA_VIEWER.media_index = 0;
    VENC_MEDIA_VIEWER.item_index = parseInt(this.dataset.vencMediaViewerItemIndex);
    return VENC_MEDIA_VIEWER_SET_MEDIA(0);
}

function VENC_MEDIA_VIEWER_BIND_CALLBACK(root) {
    nodes = document.evaluate('//*[@data-venc-media-viewer-contents]', root, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
    
    for (var i = 0; i < nodes.snapshotLength; i++) {
        if (i >= VENC_MEDIA_VIEWER.items.length) {
            VENC_MEDIA_VIEWER.items.push(nodes.snapshotItem(i));
            VENC_MEDIA_VIEWER.items[i].onclick = VENC_MEDIA_VIEWER_CALLBACK;
            VENC_MEDIA_VIEWER.items[i].dataset.vencMediaViewerItemIndex = i;
        }
    }
}

function VENC_MEDIA_VIEWER_CLOSE_CALLBACK() {
    VENC_MEDIA_VIEWER.wrapper.className = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_DEACTIVATED";
    VENC_MEDIA_VIEWER.context = null;
    return false;
}

function VENC_NAVIGATION_ARROW_CALLBACK(event) {
	if (this.id === "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_NEXT") {
		VENC_ACTION_CALLBACK("next");
	}
	else if (this.id === "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_PREVIOUS") {
		VENC_ACTION_CALLBACK("previous");
	}
	event.stopPropagation();
	return false;
}

function keyPress(e) {
    if(e.key === "Escape") {
        VENC_ACTION_CALLBACK("close")
    }
    if (VENC_MEDIA_VIEWER.context !== null) {
        if(e.key === "ArrowLeft") {
             VENC_ACTION_CALLBACK("previous")
        }
        else if(e.key === "ArrowRight") {            
             VENC_ACTION_CALLBACK("next")
        }
    }
}

function VENC_ACTION_CALLBACK(action) {
    if(action === "close") {
        VENC_MEDIA_VIEWER_CLOSE_CALLBACK();
    }
    if (VENC_MEDIA_VIEWER.context !== null) {

        if(action === "previous" && VENC_MEDIA_VIEWER.media_index > 0) {
            VENC_MEDIA_VIEWER.media_index--;
            VENC_MEDIA_VIEWER_SET_MEDIA(VENC_MEDIA_VIEWER.media_index);
        }
        else if(action === "next" && VENC_MEDIA_VIEWER.media_index >= 0 && VENC_MEDIA_VIEWER.media_index < VENC_MEDIA_VIEWER.medias.length-1) {
            VENC_MEDIA_VIEWER.media_index++;
            VENC_MEDIA_VIEWER_SET_MEDIA(VENC_MEDIA_VIEWER.media_index);
        }
        else if(action === "previous" && VENC_MEDIA_VIEWER.media_index == 0 && VENC_MEDIA_VIEWER.item_index > 0) {
            VENC_MEDIA_VIEWER.context = VENC_MEDIA_VIEWER.items[parseInt(VENC_MEDIA_VIEWER.context.dataset.vencMediaViewerItemIndex)-1];
            VENC_MEDIA_VIEWER.item_index = parseInt(VENC_MEDIA_VIEWER.context.dataset.vencMediaViewerItemIndex);
            VENC_MEDIA_VIEWER.media_index = 0;
            VENC_MEDIA_VIEWER_SET_MEDIA(0);
        }
        else if(action === "next" && VENC_MEDIA_VIEWER.media_index >= VENC_MEDIA_VIEWER.medias.length-1 && VENC_MEDIA_VIEWER.item_index+1 < VENC_MEDIA_VIEWER.items.length) {
            VENC_MEDIA_VIEWER.context = VENC_MEDIA_VIEWER.items[parseInt(VENC_MEDIA_VIEWER.context.dataset.vencMediaViewerItemIndex)+1];
            VENC_MEDIA_VIEWER.item_index = parseInt(VENC_MEDIA_VIEWER.context.dataset.vencMediaViewerItemIndex);
            VENC_MEDIA_VIEWER.media_index = 0
            VENC_MEDIA_VIEWER_SET_MEDIA(0);
        }
    }
}

function VENC_TOUCH_START(e) {
    if (e.touches.length === 1 && (e.target != VENC_MEDIA_VIEWER.canvas)) {
        VENC_MEDIA_VIEWER.x_touch_start = e.touches[0].clientX;
        VENC_MEDIA_VIEWER.x_touch_diff = e.touches[0].clientX;
    }
};                                                
                                                                         
function VENC_TOUCH_MOVE(e) {
    if (!VENC_MEDIA_VIEWER.x_touch_start) {
        return;
    }
    if (VENC_MEDIA_VIEWER.context !== null && e.touches.length === 1) {
        var x_move = e.touches[0].clientX;                                    
        VENC_MEDIA_VIEWER.x_touch_diff = VENC_MEDIA_VIEWER.x_touch_start - x_move;
    } else if (e.touches.length > 1) {
        VENC_MEDIA_VIEWER.x_touch_start = null;
        VENC_MEDIA_VIEWER.x_touch_diff = null;
    }
};

function VENC_TOUCH_END(e) {
    if (VENC_MEDIA_VIEWER.context !== null && VENC_MEDIA_VIEWER.x_touch_diff != VENC_MEDIA_VIEWER.x_touch_start) {
        if ( VENC_MEDIA_VIEWER.x_touch_diff > 64 ) {
            VENC_ACTION_CALLBACK("next");
        } else if (VENC_MEDIA_VIEWER.x_touch_diff < -64) {
            VENC_ACTION_CALLBACK("previous");
        }
        VENC_MEDIA_VIEWER.x_touch_start = null;
        VENC_MEDIA_VIEWER.x_touch_diff = null;
    }

    e.stopPropagation();
    return false;
}

function VENC_MEDIA_VIEWER_ON_LOAD() {    
    close_button = document.createElement('a');
    close_button.href = "";
    close_button.onclick = VENC_MEDIA_VIEWER_CLOSE_CALLBACK;
    close_button.innerText="⨯";
    close_button.id = "VENC_MEDIA_VIEWER_CONTENTS_CLOSE_BUTTON";

    carousel = document.createElement('div');
    carousel.id = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_CAROUSEL";

    title = document.createElement('div');
    title.id = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_TITLE";

    video = document.createElement('video');
    default_video_onclick = video.onclick;
    video.onclick = function(event) { event.stopPropagation(); return false;}

    image = document.createElement('img');
    image.onclick = function(event) { event.stopPropagation(); return false;}
    
    canvas = document.createElement('canvas');
    canvas.onclick = function(event) { event.stopPropagation(); return false;}
        
    next = document.createElement('a');
    next.id = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_NEXT";
    next.href = "";
    next.onclick = VENC_NAVIGATION_ARROW_CALLBACK;
    next.innerText = VENC_MEDIA_VIEWER.next_button;
    
    previous = document.createElement('a');
    previous.id = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_PREVIOUS";
    previous.href = "";
    previous.onclick = VENC_NAVIGATION_ARROW_CALLBACK;
    previous.innerText = VENC_MEDIA_VIEWER.previous_button;

    wrapper = document.createElement('div');
    wrapper.onclick = VENC_MEDIA_VIEWER_CLOSE_CALLBACK;
    wrapper.id = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER";
    wrapper.className = "VENC_MEDIA_VIEWER_CONTENTS_WRAPPER_DEACTIVATED";
    
    wrapper.appendChild(close_button);
    wrapper.appendChild(next);
    wrapper.appendChild(image);
    wrapper.appendChild(video);
    wrapper.appendChild(canvas);
    wrapper.appendChild(previous);
    wrapper.appendChild(carousel);
    wrapper.appendChild(title);

    document.onkeydown = keyPress;
    document.addEventListener('touchstart', VENC_TOUCH_START, false);        
    document.addEventListener('touchmove', VENC_TOUCH_MOVE, false);        
    document.addEventListener('touchend', VENC_TOUCH_END, false);

    document.body.appendChild(wrapper);
            
    VENC_MEDIA_VIEWER.wrapper = wrapper;
    VENC_MEDIA_VIEWER.close_button = close_button;
    VENC_MEDIA_VIEWER.image = image;
    VENC_MEDIA_VIEWER.video = video;
    VENC_MEDIA_VIEWER.canvas = canvas;
    VENC_MEDIA_VIEWER.carousel = carousel;
    VENC_MEDIA_VIEWER.title = title;
    VENC_MEDIA_VIEWER.previous_button = previous;
    VENC_MEDIA_VIEWER.next_button = next;
    
    VENC_MEDIA_VIEWER.timer = setInterval(VENC_MEDIA_VIEWER_REFRESH_CONTENTS, VENC_MEDIA_VIEWER.interval);
}

if (! (typeof VENC_SCRIPT_BOOTSTRAP === 'undefined')) {
    VENC_SCRIPT_BOOTSTRAP.callbacks_register.push(VENC_MEDIA_VIEWER_ON_LOAD);
}
