$(document).ready(function(){

    $("#game_box1").click(function(){
        if ($("#game_box2").hasClass("flipped") == false && $("#game_box3").hasClass("flipped") == false){
            $(this).addClass("flipped").addClass("cursor_disabled")
            $("#game_box2").addClass("cursor_disabled")
            $("#game_box3").addClass("cursor_disabled")
        }
    });

    $("#game_box2").click(function(){
        if ($("#game_box1").hasClass("flipped") == false && $("#game_box3").hasClass("flipped") == false){
            $(this).addClass("flipped").addClass("cursor_disabled")
            $("#game_box1").addClass("cursor_disabled")
            $("#game_box3").addClass("cursor_disabled")
        }
    });

    $("#game_box3").click(function(){
        if ($("#game_box1").hasClass("flipped") == false && $("#game_box2").hasClass("flipped") == false){
            $(this).addClass("flipped").addClass("cursor_disabled")
            $("#game_box1").addClass("cursor_disabled")
            $("#game_box2").addClass("cursor_disabled")
        }
    });

});