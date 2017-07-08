        $('img').on('error', function () {
            $('#card_image_div').css({'display' : 'none'});
        });
        function copyToClipboard(element) {


            var $temp = $("<input>");
            $("body").append($temp);
            $temp.val(element).select();
            document.execCommand("copy");
            $temp.remove();
            Materialize.toast('copied to clipboard', 2000);
        }

        function selectText(containerid)
        {
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

        $(function () {


            $('.DESCR').each(function () {


                var max_length = 150;
                if($(this).html().length > max_length)
                {

                    // console.log("Read_more");
                    var short_content = $(this).html().substr(0, max_length);
                    $(this).html(short_content);
                    // console.log($(this).next().children()[0]);
                    $(this).next().children().css({'display' : 'inline-block'});
                }

            });



            /* Events for edit and delete Comments */
            $('.editCommentButton').click(function () {

                // console.log("Edit comment called");
                var id = this.id;
                id = id.split('');
                // console.log(id);
                 id.splice(0, 17);
                id = id.join('');
                // console.log(id);
                var textAreaEditComment = $('#modalEditCommentTextarea'  +id);
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
                        $('#modalEditComment' + id).modal('close');
                        LoadComments(id);
                    }
                });
            });


            var show_url_button = $('.show_url_button');
            show_url_button.click(function () {
                var str = 'link_url' + (this.id);
                // console.log(str);
                selectText(str);
            });


            $('.deleteCommentButton').click(function () {

                var id = this.id;
                id = id.split('');
                // console.log(id);
                 id.splice(0, 19);
                id = id.join('');
                // console.log(id);

                 commentIndex = commentsOperationsVariable;
                $.ajax({
                    url : '/comment/'+commentIndex+'/delete/',
                    type: 'post',
                    success :function(data, status){
                        // console.log(data);
                        $('#modalEditComment' + id).modal('close');
                        LoadComments(id);
                    }
                });
            });
            $('.modal').modal();
            var copy = $('.copy');
            copy.click(function (){
                // console.log("Copied Called");
                var id = this.id;
                // console.log("id is " + id);
                var linkUrl = $('#link_url' + id).attr('href');
                // console.log("LinkUrl is");
                // console.log(linkUrl);
                copyToClipboard(linkUrl);
            });


        });


        // delete link
