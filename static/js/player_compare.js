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
    $.ajax({url: '/api/player-compare-api',
        data: {'player_name_1' : $("#search1").val(), 'player_name_2' : $("#search2").val()},
        cache: false,
        type: "GET",
        success: function(response){
            response = $.parseJSON(response);

            $.each(response, function(i, item) {
                var p = $('<tr>').append(
                            '<td><a href = "/player/' + item.player1.Player_Id+ '"><img src = "' + item.player1.url + '" height = "150px" width = "170px"></a></td>',
                            $('<td>').text(''),
                            '<td><a href = "/player/' + item.player2.Player_Id+ '"><img src = "' + item.player2.url + '" height = "150px" width = "170px"></a></td>',
                        );
                var q = $('<tr>').append(
                            $('<td>').text(item.player1.Batting_Hand),
                            $('<td>').css("font-weight","bold").text('Batting Hand'),
                            $('<td>').text(item.player2.Batting_Hand),
                        );
                var r = $('<tr>').append(
                            $('<td>').text(item.player1.Bowling_Skill),
                            $('<td>').css("font-weight","bold").text('Bowling Skill'),
                            $('<td>').text(item.player2.Bowling_Skill),
                        );
                var s = $('<tr>').append(
                            $('<td>').text(item.player1.matches),
                            $('<td>').css("font-weight","bold").text('Matches'),
                            $('<td>').text(item.player2.matches),
                        );
                var t = $('<tr>').append(
                            $('<td>').text(item.player1.runs),
                            $('<td>').css("font-weight","bold").text('Runs Scored'),
                            $('<td>').text(item.player2.runs),
                        );
                var u = $('<tr>').append(
                            $('<td>').text(item.player1.wickets),
                            $('<td>').css("font-weight","bold").text('Wickets'),
                            $('<td>').text(item.player2.wickets),
                        );
                var v = $('<tr>').append(
                            $('<td>').text(item.player1.catches),
                            $('<td>').css("font-weight","bold").text('Catches'),
                            $('<td>').text(item.player2.catches),
                        );
                var w = $('<tr>').append(
                            $('<td>').text(item.player1.fours),
                            $('<td>').css("font-weight","bold").text('4s'),
                            $('<td>').text(item.player2.fours),
                        );
                var x = $('<tr>').append(
                            $('<td>').text(item.player1.sixes),
                            $('<td>').css("font-weight","bold").text('6s'),
                            $('<td>').text(item.player2.sixes),
                        );
                var y = $('<tr>').append(
                            $('<td>').text(item.player1.Country),
                            $('<td>').css("font-weight","bold").text('Country'),
                            $('<td>').text(item.player2.Country),
                        );
                var z = $('<tr>').append(
                            $('<td>').append($('<a>').attr("href","/team-season/"+item.player1.Player_Id).text('Teams')),
                            $('<td>').css("font-weight","bold").text('Teams Played For'),
                            $('<td>').append($('<a>').attr("href","/team-season/"+item.player2.Player_Id).text('Teams')),
                        );
            $('tbody').html([p,y,z,q,r,s,t,w,x,u,v]);

            });
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
