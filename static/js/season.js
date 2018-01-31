$('.show').click(function(){
    $(this).parent().find( 'li.active' ).removeClass( 'active' );
});

var a = parseFloat(window.location.href.split('/season/')[1][0]);
$('.show','#season_nav').eq(a-1).addClass('active')

$('.showSingle').click(function(){
    $('.season_table').hide();
    $( this ).parent().find( 'li.active' ).removeClass( 'active' );
    $('.season_table').removeClass('active');
    $('#div'+$(this).attr('target')).show();
    $(this).addClass( 'active' );
});
