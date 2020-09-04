/*
 * Copyright 2016, 2020 Denis Salem
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

var VENC_TREE = {
    button_show: '+',
    button_hide: '-',
    button_disabled: '○'
}

function VENC_TREE_ON_CLICK() {
    ul = this.parentElement.children[2];
    if (this.innerHTML == VENC_TREE.button_show) {
        if (ul != undefined) {
            ul.style.transition = "0.25s ease all";
            ul.style.height = "auto";
            ul.style.opacity = "1";
            ul.style.padding = "5px";
        }
        for (i = 0; i < ul.children.length; i++) {
            if (ul.children[i].children[1] != undefined) {
                if (ul.children[i].children[0].className != "__VENC_TREE_BUTTON__") {
                    ul.children[i].innerHTML = "<a href=\"\" class=\"__VENC_TREE_BUTTON__\">"+VENC_TREE.button_show+"</a>"+ ul.children[i].innerHTML;
                    ul.children[i].children[0].onclick = VENC_TREE_ON_CLICK;
                }
            }
            else {
                ul.children[i].innerHTML = "<span class=\"__VENC_TREE_BUTTON__\">"+VENC_TREE.button_disabled+"</span>"+ ul.children[i].innerHTML;
            }
        }
        this.innerHTML = VENC_TREE.button_hide;
    }
    else {
        ul.style.height = "0px";
        ul.style.overflow = "hidden";
        ul.style.opacity = "0";
        ul.style.padding = "0px";
        this.innerHTML = VENC_TREE.button_show;
    }
    
    return false;
}

function VENC_TREE_HIDE(nodes) {
    for (k = 1; k < nodes.length; k++) {
        nodes[k].style.height = "0px";
        nodes[k].style.overflow = "hidden";
        nodes[k].style.opacity = "0";
        nodes[k].style.padding = "0px";
    }
}

function VENC_TREE_ON_LOAD() {
    roots = document.getElementsByClassName("__VENC_TREE_ROOT__");
    console.log("Roots:",roots.length);
    for (i = 0; i < roots.length; i++) {
        console.log("Root index", i);
        nodes = roots[i].getElementsByClassName("__VENC_TREE_NODE__");
        console.log("Nodes:",nodes.length);
        VENC_TREE_HIDE(nodes);
        for (j = 0; j < nodes[0].children.length; j++) {
            if (nodes[0].children[j].children[1] != undefined) {
                nodes[0].children[j].innerHTML = "<a href=\"\" class=\"__VENC_TREE_BUTTON__\">"+VENC_TREE.button_show+"</a>"+ nodes[0].children[j].innerHTML;
                nodes[0].children[j].children[0].onclick = VENC_TREE_ON_CLICK;
            }
            else {
                nodes[0].children[j].innerHTML = "<span class=\"__VENC_TREE_BUTTON__\">"+VENC_TREE.button_disabled+"</span>"+ nodes[0].children[j].innerHTML;
            }
        }
    }
}

VENC_ON_LOAD_CALLBACK_REGISTER.push(VENC_TREE_ON_LOAD);
