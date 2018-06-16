var socket_message = io("http://localhost:3000/message");
var socket_private_message = io("http://localhost:3000/private-mesage");
var socket_player = io("http://localhost:3000/player");

$(document).ready(function(){

    // Hàm gửi tin nhắn cho server
    $('#text-message').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode: event.which);
        if(keycode == '13'){
            if ($('#text-message').val() != ""){
                socket_message.emit('Client-send-message', $('#text-message').val());
                $('#text-message').val('');
            }
        }
    });

    // Nhận tin nhắn server gửi vể
    socket_message.on('Server-send-message-all-client', function(data){
        $('#message-container').append('<li>'+ data + '</li>')
    });

    //Gửi user về server
    $('#send-username').click(function(){
        socket_private_message.emit('private-message-send-username', $('#username').val());
        $('#username').val('');
    });

    //Gửi tin nhắn private về server từ user gửi
    $('#send-privte-message').click(function(){
        var recipient = $('#send-to-username').val();
        var message_to_sent = $('#private-message').val();
        socket_private_message.emit('private-message-from-client',{'username':recipient, 'message': message_to_sent});
        $('#private-message').val('');

    });

    // In tin nhắn private cho user nhận
    socket_private_message.on('private-message-from-server-receipient', function(msg){
        $('#message-container').append('<li>' + msg + '</li>');
    });

    // In tin nhắn private cho user gửi
    socket_private_message.on('private-message-from-server-sender', function(msg){
        $('#message-container').append('<li>' + msg + '</li>');
    });

    // In tin nhắn cho tất cả user trong room
    socket_private_message.on('private-message-from-server-room', function(msg){
        $('#message-container').append('<li>' + msg + '</li>');
    });
});
