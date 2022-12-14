function notifyMe(msg) {
    // Let's check if the browser supports notifications
    if (!("Notification" in window)) {
        alert("**** \n \n" + msg.toString() + " \n \n ****");
    }

    // Let's check whether notification permissions have alredy been granted
    else if (Notification.permission === "granted") {
        let dts = Math.floor(Date.now());
        let options = {
            body: msg.toString(),
            dir: 'ltr',
            icon: "/static/images/new/LoginLogo.jpg",
            timestamp: dts,
        };
        // If it's okay let's create a notification
        let notification = new Notification("Khofu", options);
        // notification.onclick = function (event) {
        //     event.preventDefault(); // prevent the browser from focusing the Notification's tab
        //     window.open('http://www.mozilla.org', '_blank');
        // }
        notification.onerror = function () {
            alert("**** \n \n" + msg.toString() + " \n \n ****");
        };
    }
    // Otherwise, we need to ask the user for permission
    else if (Notification.permission !== 'denied' || Notification.permission === "default") {
        Notification.requestPermission(function (permission) {
            // If the user accepts, let's create a notification
            if (permission === "granted") {
                let options = {
                    body: msg.toString(),
                    dir: 'ltr',
                    icon: "/static/images/new/LoginLogo.jpg",
                };
                // If it's okay let's create a notification
                let notification = new Notification("Khofu", options);
                // notification.onclick = function (event) {
                //     event.preventDefault(); // prevent the browser from focusing the Notification's tab
                //     window.open('http://www.mozilla.org', '_blank');
                // };
                notification.onerror = function () {
                    alert("**** \n \n" + msg.toString() + " \n \n ****");
                };
            } else {
                alert("**** \n \n" + msg.toString() + " \n \n ****");
            }
        });
    } else if (Notification.permission === 'denied') {
        alert("**** \n \n" + msg.toString() + " \n \n ****");
    }

    // At last, if the user has denied notifications, and you
    // want to be respectful there is no need to bother them any more.
}
