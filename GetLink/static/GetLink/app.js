$(document).ready(function () {

    var csrf = $("input[name=csrfmiddlewaretoken]").val();

    $(".add-list-btn").click(function () {
        var modal = document.getElementById('myModal');
        var span = document.getElementsByClassName("close")[0];
        var modalContent = document.getElementById('notice');
        var loadingimg = document.getElementById('loadingimg')

        $.ajax({
            url: '/ajax_post/',
            type: 'post',
            beforeSend: function () {
                modal.style.display = "flex";
            },
            data: {
                fileid: $(this).attr('id'),
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                loadingimg.style.display = 'none';
                modalContent.innerHTML = 'Done';
                modal.style.display = "None";
                $("#right").append('<li>' + response.mes + '</li>')
            }
        })
    });

    // change password close dialog button and hide the pop up
    var pop = document.getElementById('changepw');
    $(".close").click(function () {
        pop.style.display = 'None';
    });


    //show change password pop up
    $("#btn1").click(function () {
        pop.style.display = 'flex';
    });


    //save new password button click function
    $(".savepw").click(function () {
        var pw1 = document.getElementById('newpw1');
        var pw2 = document.getElementById('newpw2');
        if (pw1.value != pw2.value) {
            pw2.style.border = "solid 1px red";
            $(".message").text("Password does not match , please try again");
        } else {
            var pw = /^[A-Za-z]\w{7,14}$/;
            if (pw1.value.match(pw)) {
                $.ajax({
                    url: '/changepw/',
                    type: 'post',
                    data: {
                        csrfmiddlewaretoken: csrf,
                        newpw: pw1.value,
                    },
                    success: function (response) {
                        alert(response.mes);
                        window.location.replace('/accounts/login/');
                    }
                })
            } else {
                $(".message").text("Invalid password formation")
            }
        }
    })

    //delete file from subscribe list pop up close button
    var delete_close_btn = document.getElementsByClassName('delete_btn');
    $('.delete-sub-file').click(function () {
        var id = $(this).attr('id');
        $.ajax({
            url: '/deleteFile/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                fileid: id,
            },
            success: function (response) {
                alert(response.mes);
                var liid = 'li-' + id;
                var removeItem = document.getElementById(liid);
                $('#' + liid).fadeOut(500, function () {
                    removeItem.remove();
                });
                // removeItem.remove();
            }
        });
    })

});