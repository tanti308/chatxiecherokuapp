
// 1. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


// 2. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
var isPlaying = false;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: 'geKpK_TyH9Y',
        playerVars: {
            'autoplay': 1,
            'controls': 0,
            'autohide': 1,
            'wmode': 'opaque',
            'rel': 0,
            'loop': 1
        },
        events: {
            'onReady': onPlayerReady
        }
    });
    // document.getElementById('play-pause').onclick = function () {
    //     player.playVideo();
    // };
    // document.getElementById('pause').onclick = function () {
    //     player.pauseVideo();
    // };
}

$(document).ready(
    function(){
        socket_player.emit('connect');
    }
);

// 3. The API will call this function when the video player is ready.
function onPlayerReady(event) {    
    socket_player.on('server-send-play-pause', function(data){
        // event.target.playVideo();
        // console.log('Có data play');
        // x = 1;
        // console.log(data);
        if(data.play) {
            event.target.playVideo();
            isPlaying = true;
            console.log(isPlaying);
        } else {
            event.target.pauseVideo();
            isPlaying = false;
            console.log(isPlaying);
        }
    });

    $('#play-pause').click(function() {
        if (isPlaying) {
            event.target.pauseVideo();
            isPlaying = false;
            // socket_player.emit('client-send-play-pause', event.target.playVideo());
        } else {
            event.target.playVideo();
            isPlaying = true;
            // socket_player.emit('client-send-play-pause', event.target.pauseVideo());
        }
        var status = { play: isPlaying };
        socket_player.emit("client-send-play-pause", status);
    });
}