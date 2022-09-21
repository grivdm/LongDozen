
function get_user_location() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function (position) {
            let latitude = position.coords.latitude;
            let longitude = position.coords.longitude;
            ajax_post(csrftoken, latitude, longitude);
        }, function (error){
            if(error.PERMISSION_DENIED){
                alert('Location permission is denied. Default location: 0,0')
                ajax_post(csrftoken, 0, 0);
            }
        }
        );
    } else {
        alert('Geolocation is not supported by this browser.')
        ajax_post(csrftoken, 0, 0);
    }

}

get_user_location()




$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});


var csrftoken = $("[name=csrfmiddlewaretoken]").val();



function ajax_post(csrftoken, latitude, longitude ){

    $ .ajax (
        {
            headers:{"X-CSRFToken": csrftoken},
            url: '/user_location/',
            method: 'post',
            dataType: 'html',
            data: {
                lat: latitude,
                lng: longitude,
            },
        }
    )

}
