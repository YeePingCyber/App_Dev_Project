$(document).ready(function(){

    $("#game_box1").click(function(){
        if ($("#game_box2").hasClass("flipped") == false && $("#game_box3").hasClass("flipped") == false){
            $(this).addClass("flipped").addClass("default_cursor")
            $("#game_box2").addClass("cursor_disabled")
            $("#game_box3").addClass("cursor_disabled")
            $("#button_box1").attr("disabled", true).addClass("default_cursor")
            $("#button_box2").attr("disabled", true).addClass("cursor_disabled")
            $("#button_box3").attr("disabled", true).addClass("cursor_disabled")
        }
    });

    $("#game_box2").click(function(){
        if ($("#game_box1").hasClass("flipped") == false && $("#game_box3").hasClass("flipped") == false){
            $(this).addClass("flipped").addClass("default_cursor")
            $("#game_box1").addClass("cursor_disabled")
            $("#game_box3").addClass("cursor_disabled")
            $("#button_box1").attr("disabled", true).addClass("cursor_disabled")
            $("#button_box2").attr("disabled", true).addClass("default_cursor")
            $("#button_box3").attr("disabled", true).addClass("cursor_disabled")
        }
    });

    $("#game_box3").click(function(){
        if ($("#game_box1").hasClass("flipped") == false && $("#game_box2").hasClass("flipped") == false){
            $(this).addClass("flipped").addClass("default_cursor")
            $("#game_box1").addClass("cursor_disabled")
            $("#game_box2").addClass("cursor_disabled")
            $("#button_box1").attr("disabled", true).addClass("cursor_disabled")
            $("#button_box2").attr("disabled", true).addClass("cursor_disabled")
            $("#button_box3").attr("disabled", true).addClass("default_cursor")
        }
    });

});