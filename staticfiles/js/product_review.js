function validStar() {
    var s1 = document.getElementById('s1').checked,
        s2 = document.getElementById('s2').checked,
        s3 = document.getElementById('s3').checked,
        s4 = document.getElementById('s4').checked,
        s5 = document.getElementById('s5').checked;
    if (s1 === false && s2 === false && s3 === false && s4 === false && s5 === false) {
        document.getElementById('req_mes').style.display = 'inline';
    }
}