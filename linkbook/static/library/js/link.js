

        $('img').on('error', function () {
            $('#card_image_div').css({'display' : 'none'});
        });


        function copyToClipboard(element) {
        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val($(element).text()).select();
        document.execCommand("copy");
        $temp.remove();
        }

        function selectText(containerid) {
            if (document.selection) {
                var range = document.body.createTextRange();
                range.moveToElementText(document.getElementById(containerid));
                range.select();
            } else if (window.getSelection) {
                 range = document.createRange();
                range.selectNode(document.getElementById(containerid));
                window.getSelection().removeAllRanges();
                window.getSelection().addRange(range);
            }
        }

        // delete link
        $('#deleteCompletely').click(function(){
            $.ajax({
                url: '/link/{{link.id}}/delete/',
                type: 'post',
                success: function(data, status){
                    // console.log(data);
                    window.location = "/{{request.user.username}}/";
                }

            });

        });

        $(function () {

            var show_url_button = $('#show_url_button');
            show_url_button.click(function () {
                selectText('link_url');
            });


            var comments_tab = $('#comments_tab');
            var comments_open = 0;


            comments_tab.click(function () {
                if(comments_open == 0){
                    $('#comments').css({'display' : 'block'});
                    comments_tab.html("Hide Comments");
                }
                else{
                    $('#comments').css({'display' : 'none'});
                    $('#comments_tab').html("<i class='material-icons' style='color: white; cbackground-color: transparent' >comment</i><span style='vertical-align: top;'> " +
                        globalCommentsObject.length + "</span>");
                }
                comments_open = 1 - comments_open;
                LoadComments();
            });


            $('.modal').modal();
            var copy = $('.copy');
            copy.click(function (){
                var linkUrl = $('#link_url');
                copyToClipboard(linkUrl);
                Materialize.toast('copied to clipboard', 2000);
            });





            /* Events for edit and delete Comments */
            $('#editCommentButton').click(function () {

                var textAreaEditComment = $('#modalEditCommentTextarea');
                var text = textAreaEditComment.val();
                if(!$.trim(text)){
                    alert("Can't add empty comments!");
                    commentsSubmitButton.removeClass('disabled');
                    return;
                }

                // Removing excess white spaces from text area.
                text.replace(/\s+/g, " ").replace(/^\s|\s$/g, "");

                // ID of comment to be edited
                var commentIndex = commentsOperationsVariable;

                $.ajax({
                    url : '/comment/'+commentIndex+'/edit/',
                    type: 'post',
                    data: {'text':text},
                    success :function(data, status){
                        // console.log(data);
                        $('#modalEditComment').modal('close');
                        LoadComments();
                    }
                });
            });

            $('#deleteCommentButton').click(function () {

                var commentIndex = commentsOperationsVariable;
                $.ajax({
                    url : '/comment/'+commentIndex+'/delete/',
                    type: 'post',
                    success :function(data, status){
                        // console.log(data);
                        $('#modalEditComment').modal('close');
                        LoadComments();
                    }
                });
            });

        });
