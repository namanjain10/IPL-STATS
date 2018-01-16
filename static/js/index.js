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

    // console.log(TotalRuns,TotalBalls);

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

// var TotalRuns = 0;
// var TotalBalls = 0;
//
// $("#runs").each(function() {
//     TotalRuns += parseFloat($(this).text());
// });
//
// $("#balls").each(function() {
//     TotalBalls += parseFloat($(this).text());
// });
// $('#runs').eq(0).css('color','blue');
// //console.log(TotalRuns,TotalBalls);
// //$("#data").append('<tr><td></td><td>' +TotalRuns+ '</td><td>' + TotalBalls +  '</td></tr>');
//
// $('#data').append(
//         $('<td>'),
//         $('<td>').TotalRuns,
//         $('<td>').TotalBalls);
