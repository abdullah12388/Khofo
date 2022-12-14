let musicPlayer = document.getElementById('musicPlayer');
let myAudioParent = document.getElementById('myAudioParent');
let host = window.location.host;
let myStr1 = "<audio id='myAudio' class='myAudio' src=\"http://"+host.toString()+"/media/music/9.mp3\" controls>a</audio>";
             // "<audio src=\"http://127.0.0.1:8020/media/music/1.wav\" style=\"width: 150px;height: 28px;\" controls>Music 1</audio>"
let myStr2 = "<audio id='myAudio' class='myAudio' src=\"http://"+host.toString()+"/media/music/10.mp3\" controls>a</audio>";
let myStr3 = "<audio id='myAudio' class='myAudio' src=\"http://"+host.toString()+"/media/music/16.mp3\" controls></audio>";
let myStr4 = "<audio id='myAudio' class='myAudio' src=\"http://"+host.toString()+"/media/music/17.mp3\" controls></audio>";
let myStr5 = "<audio id='myAudio' class='myAudio' src=\"http://"+host.toString()+"/media/music/20.mp3\" controls></audio>";
let myStr6 = "<audio id='myAudio' class='myAudio' src=\"http://"+host.toString()+"/media/music/25.mp3\" controls></audio>";
musicPlayer.onclick = function () {
    'use strict';
    console.log("wikaaaaa");
    let myStr = myStr1.concat(myStr2, myStr3, myStr4, myStr5, myStr6);
    console.log(myStr);
    myAudioParent.innerHTML = myStr;
    let myAudio = document.getElementsByClassName('myAudio');
    myAudio[2].play();
    // for (let i=0; i < myAudio.length; i++) {
    //     myAudio[i].play();
    // }
    // myAudio.play();
};