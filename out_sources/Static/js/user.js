let forgetPassword = document.getElementById("forgetPassword");
let userEmail = document.getElementById("userEmail");
forgetPassword.onclick = function () {

    $.ajax({
        type: 'GET',
        url: '/user/ForgetPassword/',
        data: {
            'email': userEmail.value,
        },
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            if (data.done) {
                console.log(data);
                notifyMe("We sent a new password to your e-mail, please check it");
            } else {
                notifyMe("Sorry, this e-mail has no account");
            }
        }
    });


};
