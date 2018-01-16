function player(event) {

    if ($('#search').val() === '') {
        $('.dropdown-menu').hide();
    }

    else if ($('#search').val() !== '') {

        $.ajax({url: "http://127.0.0.1:8000/player-name-api",
            data: {'name' : ($('#search').val())},
            cache: false,
            type: "GET",
            success: function(response){

                list = $("<ul class='dropdown-menu' style='height: auto;max-height: 400px;    overflow-x: hidden;'></ul>");
                if (response.length == 2) {
                    var tr = $('<li>').text(" No such Player!!! Try his surname !!")
                    tr.appendTo(list);
                }
                else {
                    response = $.parseJSON(response);
                    $.each(response, function(i, item) {
                        //var tr = $('<li>').html("<a href='"+h+"'> "+ item.Player_Name + "</a>"),
                        var tr = $('<li class = "col-md-8">').text(item.Player_Name)
                        tr.appendTo(list);
                    });
                }
                $("#search_box").html(list);
                $('.dropdown-menu').show();
            }
        });
    }
}
