var socket = io.connect('http://' + document.domain + ':' + location.port + '/');

socket.on('connect', function() {
    console.log('Socket.IO connection established');
    document.body.classList.add('socket-connected');
});

socket.on('disconnect', function() {
    document.body.classList.remove('socket-connected');
});

socket.on('file_processed', function(data) {
    console.log('File processed:', data.message);
    showNotification(data.message);
});

function showNotification(message) {
    console.log('Showing notification:', message);
    var notificationsContainer = document.getElementById('notifications-container');
    var notification = document.createElement('div');
    notification.className = 'notification alert alert-success';
    notification.innerHTML = `<strong>File Processed:</strong> ${message}`;
    notificationsContainer.appendChild(notification);
    console.log('Notification element created');

    setTimeout(function() {
        notification.classList.add('show');
        console.log('Notification shown');
    }, 100);

    setTimeout(function() {
        notification.classList.remove('show');
        console.log('Notification hidden');
        setTimeout(function() {
            notification.remove();
            console.log('Notification removed from DOM');
        }, 5000);
    }, 5000);
}

document.getElementById('test-notification').addEventListener('click', function() {
    showNotification('Converted TML File in processed_files folder');
});

console.log('notifications.js loaded and ready');
