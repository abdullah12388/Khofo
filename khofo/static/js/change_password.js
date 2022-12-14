let newPass = document.getElementById('new'),
    confirmPass = document.getElementById('confirm'),
    changePasswordBtn = document.getElementById('changePasswordBtn'),
    invalidSpan = document.getElementById('invalid_span'),
    validSpan = document.getElementById('valid_span');

function togglePass() {
    let _new = document.getElementById('new'),
        _confirm = document.getElementById('confirm'),
        _eye = document.getElementById('eye');
    if (_eye.className === 'fa fa-eye-slash show-password') {
        _eye.className = 'fa fa-eye show-password';
        _new.type = 'text';
        _confirm.type = 'text';
    } else {
        _eye.className = 'fa fa-eye-slash show-password';
        _new.type = 'password';
        _confirm.type = 'password';
    }
}

confirmPass.onkeyup = function () {
    if (newPass) {
        if (newPass.value.toString().trim() !== "") {
            comparePassword();
        }
    }
};

newPass.onkeyup = function () {
    if (confirmPass) {
        if (confirmPass.value.toString().trim() !== "") {
            comparePassword();
        }
    }
};

function comparePassword() {
    'use strict';
    if (newPass && confirmPass) {
        let newPassValue = newPass.value.toString().trim();
        let confirmPassValue = confirmPass.value.toString().trim();
        if (newPassValue !== "" && confirmPassValue !== "" && newPass.value.length === newPassValue.length
            && confirmPass.value.length === confirmPassValue.length) {
            if (newPassValue.length >= 8 && confirmPassValue.length >= 8) {
                if (confirmPassValue === newPassValue) {
                    changePasswordBtn.type = 'submit';
                    invalidSpan.style.display = 'none';
                    validSpan.style.display = 'block';
                } else {
                    changePasswordBtn.type = 'button';
                    invalidSpan.style.display = 'block';
                    validSpan.style.display = 'none';
                }
            }
        }
    }
}