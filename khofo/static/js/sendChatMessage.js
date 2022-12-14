let messageInput = document.getElementById('messageInput');
let sendMessageButton = document.getElementById('sendMessageButton');

sendMessageButton.onclick = function () {
    'use strict';
    if (messageInput) {
        let messageValue = messageInput.value.toString().trim();
        if (messageValue !== '') {
            if (messageValue.length > 1) {
                console.log('messageInput = ', messageInput.value);
                $.ajax({
                    type: "GET",
                    url: '/export/send-message/',
                    dataType: 'json',
                    data: {
                        'message_value': messageValue,
                    },
                    traditional: true,
                    contentType: 'application/json; charset=utf-8',
                    success: function (data) {
                        console.log(data);
                    }
                });
            }
        }
    }

};

