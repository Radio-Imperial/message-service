$(document).ready(function() { 
    $('#message-form').submit(function() { 
        $(this).ajaxSubmit({
            url: 'http://imperial-message-service.appspot.com/message',
            type: 'post',
            dataType: 'json',
            error: errorHandler
        });
        return false;
    });
});

function errorHandler(xhr, status, error) {
    alert("error" + status)
}