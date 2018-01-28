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


function compare () {
    $.ajax({url: "http://127.0.0.1:8000/api/player-partnership-api/",
        data: {'player_name_1' : $("#search1").val(), 'player_name_2' : $("#search2").val()},
        cache: false,
        type: "GET",
        success: function(response){
            response = $.parseJSON(response);
            console.log(response.length);

            var p = $('<tr>').append(
                    '<td><a href = "/player/' + response[0].Player_Id1+ '"><img src = "' + response[0].url1 + '" height = "150px" width = "170px"></a></td>',
                    $('<td>').text(''),
                    '<td><a href = "/player/' + response[0].Player_Id2+ '"><img src = "' + response[0].url2 + '" height = "150px" width = "170px"></a></td>',
                );
                $('tbody').html([p]);

          if (response[0]['status'] == 0) {

              var head = $('<thead>').append($('<tr>').append(
                  $('<td>').css("font-weight","bold").text('Match Id'),
                  $('<td>').css("font-weight","bold").text($("#search1").val()),
                  $('<td>').css("font-weight","bold").text($("#search2").val()),
                  $('<td>').css("font-weight","bold").text('Extras'),
                  $('<td>').css("font-weight","bold").text('Total Runs')
              ));

              var body = $('<tbody>');

              $.each(response, function(i, item) {
                  var p = $('<tr>').append(
                            '<td><a href = "/match/' + item.match_id + '">' + item.match_id + '</a></td>',
                            $('<td>').text(item.run1),
                            $('<td>').text(item.run2),
                            $('<td>').text(item.extra1 + item.extra2),
                            $('<td id = "total">').css("font-weight","bold").text(item.run1 + item.run2 + item.extra1 + item.extra2)
                        );
                    body.append(p);
                });

          $('#part').html([head, body]);
        }
        else {
            $('#part').html('<p><strong>No Played Together !!! </strong></p>');
        }
        }
    });
}
