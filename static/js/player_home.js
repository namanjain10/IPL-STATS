function player(event) {

    if ($('#search').val() === '') {
        $('.dropdown-menu').hide();
    }

    else if ($('#search').val() !== '') {

        $.ajax({url: "http://127.0.0.1:8000/api/player-name-api/",
            data: {'name' : ($('#search').val())},
            cache: false,
            type: "GET",
            success: function(response){

                list = $("<ul class='dropdown-menu' id='dropdownMenu1'></ul>");
                if (response.length == 2) {
                    var tr = $('<li>').text(" No such Player!!! Try his surname !!")
                    tr.appendTo(list);
                }
                else {
                    response = $.parseJSON(response);
                    $.each(response, function(i, item) {
                        h = '/player/' + item.Player_Id + '/'
                        var tr = $('<li class = "col-md-8">').html("<a href='"+h+"'> "+ item.Player_Name + "</a>")
                        //var tr = $('<li class = "col-md-8">').text(item.Player_Name)
                        tr.appendTo(list);
                    });
                }
                $("#search_box").html(list);
                $('.dropdown-menu').show();
            }
        });
    }
}