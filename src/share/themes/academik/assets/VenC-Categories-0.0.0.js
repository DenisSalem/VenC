var VENC_CATEGORIES = {
    button: '',
}

function VENC_CATEGORIES_ON_LOAD() {
    nodes = document.getElementsByClassName("__VENC_CATEGORY_NODE__");
    for (i = 1; i < nodes.length; i++) {
        console.log(nodes[i]);
    }
}

