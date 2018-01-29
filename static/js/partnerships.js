function player(event,value) {

    if ($('#search'+value).val() === '') {
        $('.dropdown-menu','#search_box'+value).hide();
    }

    else if ($('#search'+value).val() !== '') {

        $.ajax({url: '/api/player-name-api/',
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
    $.ajax({url: '/api/player-partnership-api/',
        data: {'player_name_1' : $("#search1").val(), 'player_name_2' : $("#search2").val()},
        cache: false,
        type: "GET",
        success: function(response){
            response = $.parseJSON(response);

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
                            $('<td class = "run1">').text(item.run1),
                            $('<td class = "run2">').text(item.run2,10),
                            $('<td class = "extra">').text(item.extra1 + item.extra2),
                            $('<td class = "total">').css("font-weight","bold").text(item.run1 + item.run2 + item.extra1 + item.extra2)
                        );
                    body.append(p);
                });

          $('#part').html([head, body]);

          var TotalRuns = 0, Run1 = 0, Run2 = 0, Extra = 0;

          $('.run1').each(function() {
              Run1 += parseFloat($(this).text());
          })
          $('.run2').each(function() {
              Run2 += parseFloat($(this).text());
          })
          $('.extra').each(function() {
              Extra += parseFloat($(this).text());
          })
          $('.total').each(function() {
              TotalRuns += parseFloat($(this).text());
          })

          $('#part tbody').append($('<tr>').append($('<td>').css("font-weight","bold").text('Total'),
                              $('<td>').css("font-weight","bold").text(Run1 + " (" + Math.round(Run1/TotalRuns * 100,2) + "%)"),
                              $('<td>').css("font-weight","bold").text(Run2 + " (" + Math.round(Run2/TotalRuns * 100,2) + "%)"),
                              $('<td>').css("font-weight","bold").text(Extra),
                              $('<td>').css("font-weight","bold").text(TotalRuns)
                          ));

          var fixedTable = fixTable(document.getElementById('part'));

        }
        else {
            $('#part').html('<p><strong>Not Played Together !!!</strong></p>');
        }

        }
    });
}

$("#searchclear1").click(function(){
    $("#search1").val('');
    $('.dropdown-menu','#search_box1').hide();
});

$("#searchclear2").click(function(){
    $("#search2").val('');
    $('.dropdown-menu','#search_box2').hide();
});
