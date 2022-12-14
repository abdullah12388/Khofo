let forgetPassword = document.getElementById("forgetPassword");
let userEmail = document.getElementById("userEmail");
let forgetPasswordSend = document.getElementById("forgetPasswordSend");
let loginIconLoader = document.getElementById("loginIconLoader");
forgetPassword.onclick = function () {
    forgetPasswordSend.style.display = 'none';
    loginIconLoader.style.display = 'block';
    $.ajax({
        type: 'GET',
        url: '/user/forget-password/',
        data: {
            'email': userEmail.value,
        },
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            forgetPasswordSend.style.display = 'block';
            loginIconLoader.style.display = 'none';
            if (data.done) {
                console.log(data);
                notifyMe("We sent a new password to your e-mail, please check it");
            } else {
                notifyMe("Sorry, this e-mail has no account");
            }
        }
    });


};
