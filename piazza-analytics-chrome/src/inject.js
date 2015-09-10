var lastPiazzaPost = -1;

$(document).ready(function() {
    $(window).unload(updateNames);
    // wait until a dom thing exists
    updateNames();
});

new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (!mutation.addedNodes) {
            return;
        }
        updateNames();
    });
}).observe(document.body, {
    childList: true,
    subtree: true,
    attributes: false,
    characterData: false
});

function updateNames() {
    var proxyUrl = "https://cdn.moe/piazza/";

    // this should be well formed
    var postId = window.location.search.split("=")[1];
    if (postId === lastPiazzaPost) {
        return;
    }
    lastPiazzaPost = postId;

    $.ajax({
        type:'GET',
        url: proxyUrl + "tag_good/" + postId,
        dataType: 'json',
    }).done(function(data) {
        div = "<div >" + data["tag_good"].join() + "</div>";
        $('.do_good_note').after(div) ;
        div = "<div>" + data["tag_endorse"].join() + "</div>";
        $('.do_good_answer').after(div);
    });
}
