function ResetForm() {
        $(this).closest('form').find("input[type=text], textarea, input[type=password] select, input[type=url]").val("")
    }

    // CSRF handling
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
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    function LoadNotifications(param) {
        var books = $("#BOOKS");
        var notifs = $("#NOTIFS");
        var notif_master = $("#MYNOTIF");
        $.ajax({
            url: '/navbar/',
            data: {'notif': param},
            type: 'post',
            success: function (data, status) {
                console.log(data);

                // bind user books
                if (param == 1) {
                    str = '<option selected disabled>Choose Books here</option>';
                    for (var i = 0; i < data['books'].length; i++) {
                        str += ('<option>' + data['books'][i] + '</option>');
                    }
                    books.html(str);
                    books.material_select();
                }

                if (data['new_notifs'] === false) {
                    notif_master.removeClass('pulse');
                    notif_master.removeClass('blue');
                    notif_master.addClass('green');

                    if (param === 0) {
                        return;
                    }
                } else {
                    notif_master.removeClass('green');
                    notif_master.addClass('pulse');
                    notif_master.addClass('blue');
                }


                str = '';
                for (i = 0; i < data['notifs'].length; i++) {
                    if (data['notifs'][i]['unread']) {
                        //give shading here
                        str += '<li class=" notifications_unread collection-item">';
                    }
                    else {
                        str += '<li class="collection-item">';
                    }

                    str += ("<a style='max-width : 100%; padding : 1px; margin : 1px'  href=" + data['notifs'][i]['url'] + ">"
                    + "<img src=" + data['notifs'][i]['pic'] + " height=20px width=20px/> <span class='notifications_normal'>"
                    + data['notifs'][i]['text'] + "</span></a></li>");
                    str += '<li class="divider"></li>'
                }

                if (str === '') {
                    str = '<li>No notifications</li>';
                    notif_master.removeClass('pulse');
                    notif_master.removeClass('blue');
                    notif_master.addClass('green');
                }

                // bind notifications
                notifs.html(str);
            }
        });
    }


    $("#MYNOTIF").click(function () {
        var notif_master = $("#MYNOTIF");
        notif_master.removeClass('pulse');
        notif_master.removeClass('blue');
        notif_master.addClass('green');
        $.ajax({
            url: '/inbox/notifications/mark-all-as-read/',
            type: 'get'
        });
    });
