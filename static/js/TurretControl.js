$(document).ready(function() {
    // Create XML Object
    var xhttp = new XMLHttpRequest();

    var CurrentMode;

    // GET TurretMode from Server
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        document.getElementById("Header").innerHTML =
        "Current Mode: " + this.responseText;
        CurrentMode = this.responseText
        }
    };
    xhttp.open("GET", "TurretMode", true);
    xhttp.send();

    // If in Manual Mode Click Image to Aim And Fire
    var loop = setInterval(function() {
        document.getElementById("Header").innerHTML =
        "Current Mode: " + CurrentMode;


    }, 250);


        $("img").on("click", function(event) {
            if (CurrentMode == "Manual") {
                var x = event.pageX - this.offsetLeft;
                var y = event.pageY - this.offsetTop;
                console.log("X Coordinate: " + x + " Y Coordinate: " + y);

                // POST x and y coordinates to Server
                url = window.location.protocol + "//" + window.location.host + "/TurretMode";
                $.ajax(url, {
                    type: 'POST',
                    data: {
                        'TurretMode':CurrentMode,
                        'x':x.toString(),
                        'y':y.toString()

                        }
                })
            }
        });


    // Toggle Mode
    $("#ModeToggle").on("click", function() {
        CurrentMode = $('#ControlOptions').val();


    });



});
