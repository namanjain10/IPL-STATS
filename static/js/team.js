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