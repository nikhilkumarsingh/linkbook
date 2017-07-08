
        $(function () {

            $('.modal').modal();

            $('.follow_button').click(function () {

                var username = this.id;
                var fButton = $(this);
                $.get('/follow/', {to_follow: username}, function (data) {
                    console.log(fButton);
                    console.log("hello");
                    console.log(data);
                    if (data['follow_button'] === '1') {
                        //$('#follow_button').removeClass('grey');
                        console.log("Condition 1");
                        fButton.removeClass('grey');
                        fButton.removeClass('lighten-3');
                        fButton.attr('title', 'follow');
                        fButton.html("follow");
                    }
                    else {
                        console.log("Condition2");
                        //$('#follow_button').addClass('grey');
                        fButton.addClass('grey');
                        fButton.addClass('lighten-3');
                        fButton.attr('title', 'unfollow');
                        fButton.html("followed");
                    }

                    $('#f' + username).html(data['follower_count'] + ' followers');
                });



            });

        });
