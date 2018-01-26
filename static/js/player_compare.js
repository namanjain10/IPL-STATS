function player(event,value) {
    
    if ($('#search'+value).val() === '') {
        $('.dropdown-menu','#search_box'+value).hide();
    }

    else if ($('#search'+value).val() !== '') {

        $.ajax({url: "http://127.0.0.1:8000/api/player-name-api/",
            data: {'name' : ($('#search'+value).val())},
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
                        var tr = $('<li class = "col-md-8">').html('<a>' + item.Player_Name + '</a>')
                        tr.appendTo(list);
                    });
                }
                $("#search_box"+(value)).html(list);
                $('.dropdown-menu','#search_box'+value).show();
            }
        });
    }
}

$("#search_box1").on('click','li',function() {
    $('.dropdown-menu','#search_box1').hide();
    $("#search1").val($(this).text());
});

$("#search_box2").on('click','li',function() {
    $('.dropdown-menu','#search_box2').hide();
    $("#search2").val($(this).text());
});


$.ajax({url: "http://127.0.0.1:8000/api/player-stats-api",
    data: {'name' : $(this).text()},
    cache: false,
    type: "GET",
    success: function(response){
         response = $.parseJSON(response);
            $.each(response, function(i, item) {
                var w = $('<tr>').append($("<td>").html('<img src =' + item.url+ ' width = "30%" height = "30%" >'));
                $('tbody').append(w);
            });
    }
});
