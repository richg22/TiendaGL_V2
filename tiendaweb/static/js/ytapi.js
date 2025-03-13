$(document).ready(function() {

    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


    var player;
    window.onYouTubeIframeAPIReady = function() {
        createPlayer();
    };

 
    function createPlayer() {

        console.log('ID del video api:', videoId);
  
        player = new YT.Player('player', {
            height: '360',
            width: '640',
            videoId: videoId,
            events: {
                'onReady': onPlayerReady
            }
        });
    }


    function onPlayerReady(event) {
        event.target.playVideo();
    }
});