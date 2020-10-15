$(document).ready(function () {

    // csrf token get
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    $('[data-toggle="tooltip"]').tooltip();

    // reload div tag
    function updateDiv() {
        $('#my-message').load(document.URL + ' #my-alert');
        setTimeout(function () {
            $('.alert').delay(4000).fadeOut(500, function () {
                $(this).alert('close');
            });
        }, 2000)

    }

    //generate link download

    $('#btn-gen-link').click(function () {
        $.ajax({
            url: '/generate/',
            type: 'post',
            data: {
                parameter: $(this).attr('parameter'),
                csrfmiddlewaretoken: csrf,
            },
            success: function (response) {
                $('#myModal2').modal("hide");
                window.location.href = response.link;
            }
        })
    });


    // fade out message
    $(".alert").delay(4000).fadeOut(500, function () {
        $(this).alert('close');
    });

    // add file to list
    $(".addtolist").click(function () {
        $.ajax({
            url: '/ajax_post/',
            type: 'post',
            data: {
                fileid: $(this).attr('id'),
                csrfmiddlewaretoken: csrf,
            },
            success: function () {
                $('#myModal').modal('hide');
                updateDiv();
            }
        })
    });


    // deltete file from list
    $('.delfile').click(function () {
        var id = $(this).attr('itemid');
        $.ajax({
            url: '/deleteFile/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrf,
                fileid: id,
            },
            success: function (response) {
                updateDiv();
                var liid = 'li-' + id;
                var removeItem = document.getElementById(liid);
                $('#' + liid).fadeOut(500, function () {
                    removeItem.remove();
                });
            }
        });
    })
});