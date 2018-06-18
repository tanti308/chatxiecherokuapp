var socket_message = io("http://localhost:3000/message");
var socket_private_message = io("http://localhost:3000/private-mesage");
var socket_player = io("http://localhost:3000/player");

$(document).ready(function(){

    // Chọn file tải lên màn hình tạo room
    $('#drop-place').click(function(){
        var filepath = $('#inputGroupFile01').val();
        $('#inputGroupFile01').click();
        console.log(filepath);
        $('#file-selected').append(filepath);
    });
});
