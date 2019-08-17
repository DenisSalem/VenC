/*
 * Copyright 2016, 2019 Denis Salem
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

var VENC_CATEGORIES = {
    button_show: '+',
    button_hide: '-',
    button_disabled: '◦'
}

function VENC_CATEGORIES_ON_CLICK() {
    ul = this.parentElement.children[2];
    if (this.innerHTML == VENC_CATEGORIES.button_show) {
        if (ul != undefined) {
            ul.style.transition = "0.25s ease all";
            ul.style.height = "auto";
            ul.style.opacity = "1";
            ul.style.padding = "5px";
        }
        for (i = 0; i < ul.children.length; i++) {
            if (ul.children[i].children[1] != undefined) {
                if (ul.children[i].children[0].className != "__VENC_CATEGORY_BUTTON__") {
                    ul.children[i].innerHTML = "<a href=\"\" class=\"__VENC_CATEGORY_BUTTON__\">"+VENC_CATEGORIES.button_show+"</a>"+ ul.children[i].innerHTML;
                    ul.children[i].children[0].onclick = VENC_CATEGORIES_ON_CLICK;
                }
            }
            else {
                ul.children[i].innerHTML = "<span class=\"__VENC_CATEGORY_BUTTON__\">"+VENC_CATEGORIES.button_disabled+"</span>"+ ul.children[i].innerHTML;
            }
        }
        this.innerHTML = VENC_CATEGORIES.button_hide;
    }
    else {
        ul.style.height = "0px";
        ul.style.overflow = "hidden";
        ul.style.opacity = "0";
        ul.style.padding = "0px";
        this.innerHTML = VENC_CATEGORIES.button_show;
    }
    
    return false;
}

function VENC_CATEGORY_HIDE(nodes) {
    for (i = 1; i < nodes.length; i++) {
        nodes[i].style.height = "0px";
        nodes[i].style.overflow = "hidden";
        nodes[i].style.opacity = "0";
        nodes[i].style.padding = "0px";
    }
}

function VENC_CATEGORIES_ON_LOAD() {
    nodes = document.getElementsByClassName("__VENC_CATEGORY_NODE__");
    VENC_CATEGORY_HIDE(nodes);
    for (i = 0; i < nodes[0].children.length; i++) {
        if (nodes[0].children[i].children[1] != undefined) {
            nodes[0].children[i].innerHTML = "<a href=\"\" class=\"__VENC_CATEGORY_BUTTON__\">"+VENC_CATEGORIES.button_show+"</a>"+ nodes[0].children[i].innerHTML;
            nodes[0].children[i].children[0].onclick = VENC_CATEGORIES_ON_CLICK;
        }
        else {
            nodes[0].children[i].innerHTML = "<span class=\"__VENC_CATEGORY_BUTTON__\">"+VENC_CATEGORIES.button_disabled+"</span>"+ nodes[0].children[i].innerHTML;
        }
    }
}

