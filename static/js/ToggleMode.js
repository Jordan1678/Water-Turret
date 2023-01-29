$(document).ready(function() {

    $("#ModeToggle").on("click", function() {
        CurrentMode = $('#ControlOptions').val();
        url = window.location.protocol + "//" + window.location.host + "/TurretMode";
        $.ajax(url, {
            type: 'POST',
            data: {
                'TurretMode':CurrentMode
            }
        })
    });

    $("#ModeToggle").on("click", function() {
        CurrentMode = $('#ControlOptions').val();
        url = window.location.protocol + "//" + window.location.host + "/TurretMode";
        $.ajax(url, {
            type: 'POST',
            data: {
                'TurretMode':'Start'
            }
        })
    });

    $("#ModeToggle").on("click", function() {
        CurrentMode = $('#ControlOptions').val();
        url = window.location.protocol + "//" + window.location.host + "/TurretMode";
        $.ajax(url, {
            type: 'POST',
            data: {
                'TurretMode':'Stop'
            }
        })
    });
});