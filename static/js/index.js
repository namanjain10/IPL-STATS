// $(window).on('load',function(){
// var xhttp = new XMLHttpRequest();
// xhttp.onreadystatechange = function() {
//     if (this.readyState == 4 && this.status == 200) {
//         var arr = JSON.parse(this.responseText);
//         var name = Object.getOwnPropertyNames(arr[1])
//
//       var str = document.getElementById("player").innerHTML ;
//       str += '<table class = "table table-striped table-bordered table-hover" id = "data">'
//         str +=  '<thead> <td>Player Name</td> <td>Runs</td> <td>balls</td> <td>strike rate</td></thead><tbody>'
//
//         for (i=0; i<arr.length; i++) {
//             str += '<tr>'
//             str += '<td>' + '<a href = "/player/' + arr[i].Striker_Id + '/">' + arr[i].Player_Name + '</a></td>';
//             str += '<td id = "runs">' + arr[i].runs + '</td>';
//             str += '<td id = "balls">' + arr[i].balls + '</td>';
//             str += '<td>' + arr[i].str + '</td>';
//             str += '</tr>'
//         }
//        str += '</tbody></table>';
//        document.getElementById("player").innerHTML = str;
//     }
// };
// xhttp.open("GET", "http://127.0.0.1:8000/api", true);
// xhttp.send();
//
// });

//$.each(response, function(i, item) {
    //$('#player').append(
// $('#player').append(
//     $('<td>').text(item.Player_Name),
//     $('<td>').text(item.runs),
//     $('<td>').text(item.balls)
// );
//);
//});

$('h3:contains(West)').css("color","rgb(193, 17, 17)");
$('h3:contains(India)').css("color","rgb(52, 132, 214)");
$('h3:contains(New)').css("color","rgb(5, 2, 2)");
$('h3:contains(Eng)').css("color","rgb(19, 32, 170)");
$('h3:contains(Pak)').css("color","rgb(56, 142, 4)");
$('h3:contains(South)').css("color","rgb(15, 177, 17)");
$('h3:contains(Sri)').css("color","rgb(13, 67, 117)");
$('h3:contains(Aus)').css("color","rgb(219, 194, 27)");
$('h3:contains(Bang)').css("color","rgb(33, 99, 25)");
$('h3:contains(Zim)').css("color","rgb(180, 23, 23)");
$('h3:contains(Neth)').css("color","rgb(224, 122, 16)");

$("#dropdownMenuSeason").hover(function () {
    $("#dropdownMenuSeason").show();
    }
);

$(window).ready( function () {
    $.ajax({url: "http://127.0.0.1:8000/api",
        data: {
            "match_id": 419125
        },
        cache: false,
        type: "GET",
        success: function(response){
        response = $.parseJSON(response);

        div = $('<div></div>').attr({class : "container"});
        mytable = $('<table></table>').attr({class : "table table-striped table-bordered table-hover" ,id: "basicTable" });
        tr = $('<thead></thead>').append($('<tr>').append(
            $('<td>').text('Player_Name'),
            $('<td>').text('runs'),
            $('<td>').text('balls'),
            $('<td>').text('strike rate')
        ));
        tr.appendTo(mytable);
        var bd = $('<tbody></tbody>')
        $.each(response, function(i, item) {
            h = '/player/' + item.Striker_Id + '/'
            var tr = $('<tr>').append(
                $('<td>').html("<a href='"+h+"'> "+ item.Player_Name + "</a>"),
                $('<td>').text(item.runs).attr({class : 'runs'}),
                $('<td>').text(item.balls).attr({class : 'balls'}),
                $('<td>').text(item.str)
            );
            tr.appendTo(bd);
            });
        bd.appendTo(mytable);
        mytable.appendTo(div);
        div.appendTo("#player");
    },
    error: function(err){
        console.log(err);
    }});
});

$(document).ajaxComplete(function () {

    var TotalRuns = 0;
    var TotalBalls = 0;
    //alert('hey');

    $(".runs").each(function() {
        TotalRuns += parseFloat($(this).text());
    });

    $(".balls").each(function() {
        TotalBalls += parseFloat($(this).text());
    });

    //console.log(TotalRuns,TotalBalls);

    $('.runs').eq(0).css('color','red');

    $('#basicTable tbody').append(
            $('<td>'),
            $('<td>').TotalRuns,
            $('<td>').TotalBalls);

    $('<div></div>').appendTo('#player').text('Total : '+ TotalRuns);
});

$("#searchclear").click(function(){
    $("#search").val('');
    $('.dropdown-menu').hide();
});

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

var Total = 0, TotalWins = 0, TotalLosses = 0, TotalNr = 0;

$('.team_wins').each(function() {
    TotalWins += parseFloat($(this).text());
});

$('.team_losses').each(function() {
    TotalLosses += parseFloat($(this).text());
});

$('.team_nr').each(function() {
    TotalNr += parseFloat($(this).text());
});

$('.team_total').each(function() {
    Total += parseFloat($(this).text());
});

$('#team_table tbody').append(
    $('<tr>').css("font-weight","bold").append(
        $('<td>').text('Total'),
        $('<td>').text(Total),
        $('<td>').text(TotalWins),
        $('<td>').text(TotalLosses),
        $('<td>').text(TotalNr)
    ),
);


var playerInnings = 0, playerHighest = 0, playerRuns = 0, playerBalls = 0, playerNotOut = 0, playerHundred = 0, playerFifty = 0, playerFour = 0, playerSix = 0;

$('.player_innings').each(function() {
    playerInnings += parseFloat($(this).text());
});

$('.player_runs').each(function() {
    playerRuns += parseFloat($(this).text());
});

$('.player_balls').each(function() {
    playerBalls += parseFloat($(this).text());
});

$('.player_four').each(function() {
    playerFour += parseFloat($(this).text());
});

$('.player_six').each(function() {
    playerSix += parseFloat($(this).text());
});

$('.player_fifty').each(function() {
    playerFifty += parseFloat($(this).text());
});

$('.player_hundred').each(function() {
    playerHundred += parseFloat($(this).text());
});

$('.player_highest').each(function() {
    if (playerHighest < parseFloat($(this).text())) {
        playerHighest = parseFloat($(this).text());
    }
});

$('.player_notout').each(function() {
    playerNotOut += parseFloat($(this).text());
});

$('#player_table tbody').append(
    $('<tr>').css("font-weight","bold").append(
        $('<td>').text('Total'),
        $('<td>').text(playerInnings),
        $('<td>').text(playerNotOut),
        $('<td>').text(playerRuns),
        $('<td>').text(playerHighest),
        $('<td>').text((playerRuns/(playerInnings -  playerNotOut)).toFixed(2)),
        $('<td>').text(playerBalls),
        $('<td>').text((playerRuns/playerBalls * 100).toFixed(2)),
        $('<td>').text(playerHundred),
        $('<td>').text(playerFifty),
        $('<td>').text(playerFour),
        $('<td>').text(playerSix)
    ),
);

$('.showSingle').click(function(){
      $('.season_table').hide();
      $( this ).parent().find( 'li.active' ).removeClass( 'active' );
      $('.season_table').removeClass('active');
      $('#div'+$(this).attr('target')).show();
      $(this).addClass( 'active' );

});
