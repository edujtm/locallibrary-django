
window.onload = function() {
    initCollapBooks();
};

if (document.readyState === "complete") {
    initCollapBooks();
}

function initCollapBooks() {
    console.log("Called collapsing books initializer");
    options = {accordion : true};
    const elem = document.querySelectorAll('.collapsible');
    const instances = M.Collapsible.init(elem, options);
}