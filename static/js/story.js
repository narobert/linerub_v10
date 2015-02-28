$('.regSize').click(function() {
    $('#hideLog').css("display", "none");
    $('#hideReg').css("display", "block");
    $(this).css({'color': 'black', 'cursor': 'auto', 'opacity': 1, 'margin-left': '56px'});
    $(this).html("Register");
    $('.logSize').css({'color': '#3a5795', 'cursor': 'pointer', 'opacity': 0.7});
    $('.logSize').html("or sign in");
});

$('.logSize').click(function() {
    $('#hideLog').css("display", "block");
    $('#hideReg').css("display", "none");
    $(this).css({'color': 'black', 'cursor': 'auto', 'opacity': 1});
    $(this).html("Sign in");
    $('.regSize').css({'color': '#3a5795', 'cursor': 'pointer', 'opacity': 0.7, 'margin-left': '40px'});
    $('.regSize').html("or register");
});
