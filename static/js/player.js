$('h3:contains(West)').css("color","rgb(193, 17, 17)");
$('h3:contains(India)').css("color","rgb(52, 132, 214)");
$('h3:contains(New)').css("color","rgb(5, 2, 2)");
$('h3:contains(Eng)').css("color","rgb(19, 32, 170)");
$('h3:contains(Pak)').css("color","rgb(56, 142, 4)");
$('h3:contains(South)').css("color","rgb(15, 177, 17)");
$('h3:contains(Sri)').css("color","rgb(13, 67, 117)");
$('h3:contains(Aus)').css("color","#f4ca1c");
$('h3:contains(Bang)').css("color","rgb(33, 99, 25)");
$('h3:contains(Zim)').css("color","rgb(180, 23, 23)");
$('h3:contains(Neth)').css("color","rgb(224, 122, 16)");

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
        $('<td>').text('Career'),
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

var bowlerWickets = 0, bowlerRuns = 0, bowlerExtras = 0, bowlerBalls = 0

$('.bowler_runs').each(function() {
    bowlerRuns += parseFloat($(this).text());
});

$('.bowler_wickets').each(function() {
    bowlerWickets += parseFloat($(this).text());
});

$('.bowler_extras').each(function() {
    bowlerExtras += parseFloat($(this).text());
});

$('.bowler_balls').each(function() {
    bowlerBalls += parseFloat($(this).text());
});

$('#bowler_table tbody').append(
    $('<tr>').css("font-weight","bold").append(
        $('<td>').text('Career'),
        $('<td>').text(bowlerWickets),
        $('<td>').text(bowlerRuns),
        $('<td>').text(bowlerExtras),
        $('<td>').text(bowlerBalls),
        $('<td>').text((bowlerRuns/(bowlerBalls/6)).toFixed(2)),
        $('<td>').text((bowlerRuns/bowlerWickets).toFixed(2)),
        $('<td>').text((bowlerBalls/bowlerWickets).toFixed(2))
    ),
);