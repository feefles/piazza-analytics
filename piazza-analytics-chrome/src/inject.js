var lastPiazzaPost = -1;

$(document).ready(function() {
    $(window).unload(injectNames);
    // wait until a dom thing exists
    injectNames();
});

new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (!mutation.addedNodes) {
            return;
        }
        injectNames();
    });
}).observe(document.body, {
    childList: true,
    subtree: true,
    attributes: false,
    characterData: false
});

function makeDomNodeString(nameList) {
    return '<span class="post_actions_number">' +
        nameList.join(', ') +
        '</span>';
}

function injectNames() {
    var proxyUrl = 'https://cdn.moe/piazza/';
    // this should be well formed
    var postId = window.location.search.split('=')[1];
    if (postId === lastPiazzaPost) {
        return;
    }
    lastPiazzaPost = postId;
    classId = window.location.pathname.split('/class/')[1];

    $.ajax({
        type:'GET',
        url: proxyUrl + 'tag_good/'+ classId + "/" + postId,
    
        dataType: 'json',
    }).done(function(data) {
        $('.post_actions_number.good_note').
            after(makeDomNodeString(data['tag_good']));

        $('.post_actions_number.good_answer').
            after(makeDomNodeString(data['tag_endorse']));
    });
}
