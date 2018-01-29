function submit_data (event) {
    event.preventDefault();
    $.ajax({url: '/api/all-player-api/',
        data: {
            "category" : $('[name="category"]').find(":selected").val(),
            "country" : $('[name="country"]').find(":selected").val(),
        },
        cache: false,
        type: "GET",
        success: function(response){
            response = $.parseJSON(response);

                mytable = $('<table></table>').attr({class : "table table-striped table-bordered table-hover col-md-8" ,id: "allPlayerTable" });
                tr = $('<thead></thead>').append($('<tr>').append(
                    $('<td class = "col-md-3">').text('Player Name'),
                    $('<td class = "col-md-3">').text('Batting Hand'),
                    $('<td class = "col-md-3">').text('Bowling Skill'),
                    $('<td class = "col-md-2">').text('Country'),
                ));
                tr.appendTo(mytable);
                var bd = $('<tbody></tbody>')
                $.each(response, function(i, item) {
                    url = "/player/" + item.Player_Id + ""
                    s = "<a href='" + url + "'>" + item.Player_Name + "</a>"
                    var tr = $('<tr>').append(
                        $('<td>').html(s),
                        $('<td>').text(item.Batting_Hand),
                        $('<td>').text(item.Bowling_Skill),
                        $('<td>').text(item.Country),
                    );
                    tr.appendTo(bd);
            });
            bd.appendTo(mytable);
            $("#all_players").html(mytable);
        }
    });
}
