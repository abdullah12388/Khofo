$(document).ready(function () {
    // executes when HTML-Document is loaded and DOM is ready
    let phone = document.getElementById("phone");
    let email = document.getElementById("email");
    let country_long = document.getElementById("country_long");
    let country_short = document.getElementById("country_short");
    let logo = document.getElementById("logo");
    let logo_2 = document.getElementById("logo_2");
    // get the client ipAddress only once
    if (phone.innerHTML === "") {
        let ipAddress = '';
        var jqxhr = $.getJSON("https://api.ipify.org?format=jsonp&callback=?", function (data) {
        }).done(function (data) {
            ipAddress = data['ip'];
            getSiteInfoIp(ipAddress);
        }).fail(function () {
            ipAddress = '105.34.43.43';
            getSiteInfoIp(ipAddress);
        });
    } else {
        getSiteInfo();
    }

    function getSiteInfo() {
        $.ajax({
            type: 'GET',
            url: '/support/ajax/get_site_info2/',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: {
                'a': 'a',
            },
            success: function (data) {
                "use strict";
                if (data.done) {
                    console.log("done 2");
                    // console.log("site_info = ", data.site_info);
                    phone.innerHTML = data.site_info.phone;
                    email.innerHTML = data.site_info.email;
                    country_long.innerHTML = data.site_info.country_long;
                    logo.setAttribute("src", data.site_info.logo);
                    logo_2.setAttribute("src", data.site_info.logo_2);
                    country_short.setAttribute("class", "flag-icon flag-icon-" + data.site_info.country_short.toLowerCase());
                    // console.log("site_phone = " + phone);
                    if (phone.innerHTML === "") {
                        location.reload();
                    }
                } else {
                    console.log("get_site_info ERROR: " + data);
                    getSiteInfoIp()
                }
            }
        });
    }

    function getSiteInfoIp(ipAddress) {
        $.ajax({
            type: 'GET',
            url: '/support/ajax/get_site_info/',
            data: {
                'ip': ipAddress,
            },
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                "use strict";
                if (data.done) {
                    console.log("done 1");
                    // console.log("site_info = ", data.site_info);
                    phone.innerHTML = data.site_info.phone;
                    email.innerHTML = data.site_info.email;
                    country_long.innerHTML = data.site_info.country_long;
                    logo.setAttribute("src", data.site_info.logo);
                    logo_2.setAttribute("src", data.site_info.logo_2);
                    country_short.setAttribute("class", "flag-icon flag-icon-" + data.site_info.country_short.toLowerCase());
                    // console.log("site_phone = " + phone);
                    if (phone.innerHTML === "") {
                        location.reload();
                    }
                } else {
                    console.log("get_site_info ERROR: " + data);
                }
            }
        });
    }

});