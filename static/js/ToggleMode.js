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

    $("#Fire").on("click", function() {
        CurrentMode = $('#ControlOptions').val();
        url = window.location.protocol + "//" + window.location.host + "/TurretMode";
        $.ajax(url, {
            type: 'POST',
            data: {
                'TurretMode':'Start'
            }
        })
    });

    $("#Stop").on("click", function() {
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
