var readyStateCheckInterval = setInterval(function() {
    if (document.readyState === "complete") {
        clearInterval(readyStateCheckInterval);
        $(window).hashchange(updateNames);

        updateNames()
       
    }
}, 50);

function updateNames() {
    var server_ip = "http://159.203.71.54/";
        //this should be well formed
    var post_id = window.location.search.split("=")[1]
    $.ajax({
        type:'GET', 
        url: server_ip + "tag_good/" + post_id, 
        dataType: 'json', 
    }).done(function(data) {
        div = "<div >" + data["tag_good"].join() + "</div>"; 
        $('.do_good_note').after(div) ;
        div = "<div>" + data["tag_endorse"].join() + "</div>"; 
        $('.do_good_answer').after(div);
    });
}
