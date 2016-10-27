/* global document, console, window, WebSocket */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        var socket = new WebSocket('ws://' + window.location.host + '/socket');
        socket.onmessage = function (e) {
            var msg = JSON.parse(e.data),
                wrapper = document.createElement('div');
            wrapper.className = 'line ' + msg.status;
            wrapper.textContent = 'Task (' + msg.uid + ') for ' + msg.project + '/' +
                msg.user + ' ' + msg.status + '.';
            document.getElementById('messages').appendChild(wrapper);
        };
    });

})();
