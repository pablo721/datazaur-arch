
var chatarea = document.getElementById('chat_textarea');

function setScroll(){
    var $textarea = $('#chat_textarea');
    $textarea.scrollTop($textarea[0].scrollHeight);
}

function getMessages(){

    $.ajax({
        type: 'GET',
        url: '/messenger/getMessages/' + friend_id,
        success: function(response){
            chatarea.value = '';
            for (var key in response.messages){
                var temp = response.messages[key];
                let msg = temp.timestamp.replace('T', ' ').slice(0, 16) + ' ' + temp.sender_id + ': ' + temp.content + '\n';
                chatarea.value += msg;
                setScroll();
            }
        },
        error: function(response){
            alert('Error')
        }
    });
}


$(document).on('submit', '#msg_form', function(e){
    e.preventDefault();
    $.ajax({
    type: 'POST',
    url: '/messenger/send/',
    data: {
        sender_id: $('#sender_id').val(),
        recipient_id: $('#recipient_id').val(),
        msg_text: $('#msg_text').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function(data){
        getMessages();
    }
    });
    document.getElementById('msg_text').value = ''
});


$(document).ready(function(){
    getMessages();
    setInterval(getMessages, 2500);
    }
);