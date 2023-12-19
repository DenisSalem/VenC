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

var VENC_TREE = {
    button_show: '+',
    button_hide: '-',
    button_disabled: '○',
    ul_style: function(ul) {}
}

function VENC_TREE_SWITCH_NODE_VISIBILIY(button) {
    Array.from(button.parentNode.children).forEach(function(child, child_index, childs_array) {
        if (child.className.includes("__VENC_TREE_NODE__")) {
            if (button.innerHTML == VENC_TREE.button_hide) {
                VENC_TREE_UNHIDE_ELEMENT(child)
            }
            else {
                VENC_TREE_HIDE_ELEMENT(child)
            }
        }
    })
}

function VENC_TREE_SWITCH_BUTTON(button) {
    if (button.innerHTML == VENC_TREE.button_show) {
        button.innerHTML = VENC_TREE.button_hide;
        button.className = "__VENC_TREE_BUTTON_HIDE__"
    }
    else {
        button.innerHTML = VENC_TREE.button_show;
        button.className = "__VENC_TREE_BUTTON_SHOW__"
    }
}

function VENC_TREE_SWITCH_STATE(button) {
    VENC_TREE_SWITCH_BUTTON(button)
    VENC_TREE_SWITCH_NODE_VISIBILIY(button)
}

function VENC_TREE_ON_CLICK() {
    VENC_TREE_SWITCH_STATE(this)  
    return false;
}

function VENC_TREE_UNHIDE_ELEMENT(element) {
    element.style.transition = "0.25s ease all";
    element.style.height = "auto";
    element.style.opacity = "1";
    element.style.padding = "5px";
    element.setAttribute("data-venc-state", "visible")
}

function VENC_TREE_HIDE_ELEMENT(element) {
    element.style.height = "0px";
    element.style.overflow = "hidden";
    element.style.opacity = "0";
    element.style.padding = "0px";
    element.setAttribute("data-venc-state", "hidden")
}

function VENC_TREE_ADD_BUTTON(button) {
    a = document.createElement("a")
    a.href=''
    if ( !(button === VENC_TREE.button_disabled) ) {
        a.onclick = VENC_TREE_ON_CLICK
    }
    a.innerHTML = button
    switch(button) {
        case VENC_TREE.button_show:
            a.className = "__VENC_TREE_BUTTON_SHOW__"
            break
        case VENC_TREE.button_hide:
            a.className = "__VENC_TREE_BUTTON_HIDE__"
            break
        default:
            a.className = "__VENC_TREE_BUTTON_DISABLED__"
    }
    return a
}

function VENC_TREE_NODE_HAS(node, target) {
    childs = node.getElementsByClassName("__VENC_TREE_PATH__")
    for (i = 0; i < childs.length; i++) {
        if (target == childs[i]) {
            return true
        }
    }
    return false
}

function VENC_TREE_ON_LOAD() {    
    // Unhide current branch
    path_hrefs = document.getElementsByClassName("__VENC_TREE_PATH__");
    path_href = undefined
    for (i = 0; i < path_hrefs.length; i++) {
        if (window.location.pathname.includes(path_hrefs[i].pathname)) {
            console.log(path_hrefs[i].pathname, window.location.pathname)
            if (path_href === undefined || path_hrefs[1].pathname.length >= path_href.pathname.length) {
                path_href = path_hrefs[i];
            }
        }
    }
    
    roots = Array.from(document.getElementsByClassName("__VENC_TREE_ROOT__"))
    roots.forEach(function(root, root_index, roots_array) {
        nodes = Array.from(root.getElementsByClassName("__VENC_TREE_NODE__"))
        
        // First Pass: Setup the whole tree, and making visible active sublist
        nodes.forEach(function(node, node_index, nodes_array) {
            node_has_path_href = VENC_TREE_NODE_HAS(node, path_href)
            
            if (node.parentNode != root && !node_has_path_href) { 
                VENC_TREE_HIDE_ELEMENT(node)
            }
            else {
                VENC_TREE_UNHIDE_ELEMENT(node)
            }
            
            items = Array.from(node.children)
            items.forEach(function(item, item_index, items_array) {
                button = item.getElementsByClassName("__VENC_TREE_NODE__").length > 0 ? VENC_TREE.button_show : VENC_TREE.button_disabled
                item.insertBefore(
                    VENC_TREE_ADD_BUTTON(button),
                    item.firstChild
                )
            })
        })
        
        // Second Pass: Update button acordingly with sublist visibility
        nodes.forEach(function(node, node_index, nodes_array) {
            button = node.parentNode.firstChild
            if (node.getAttribute("data-venc-state") === "visible") {
                if( button.nodeType !== 3 && button.className.includes("__VENC_TREE_BUTTON_SHOW__")) {
                    VENC_TREE_SWITCH_BUTTON(button)
                }
            }
        })
    })
    
    // Apply style
    tree_nodes = document.getElementsByClassName("__VENC_TREE_NODE__");
    for (i = 0; i < tree_nodes.length; i++) {
        VENC_TREE.ul_style(tree_nodes[i]);    
    }
}

VENC_ON_LOAD_CALLBACK_REGISTER.push(VENC_TREE_ON_LOAD);
