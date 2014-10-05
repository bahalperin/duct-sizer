//
var compatibility = {
    "air_flow":  ["air_flow"],
    "pressure_loss": ["velocity","pressure_loss"],
    "velocity": ["velocity", "pressure_loss"],
    "diameter": ["diameter", "width_height"],
    "width_height": ["diameter", "width_height"]
};

var options = {
    "air_flow": "Air Flow",
    "pressure_loss": "Pressure Loss",
    "velocity": "Velocity",
    "diameter": "Diameter",
    "width_height": "Width/Height"
};

var units = {
    "air_flow": "CFM",
    "pressure_loss": "in. wg/100 ft.",
    "velocity": "fpm",
    "diameter": "in.",
    "width_height": "in."
};

var exclusive_inputs_1 = function() {
    var selection = $("#dropdown_2").val();
    $("#dropdown_2").empty();
    $.each(options, function(val, text) {
        $("#dropdown_2").append($('<option></option>').val(val).html(text));
    });
    var first_input = $("#dropdown_1").val();
    for (var i=0; i<compatibility[first_input].length; i++) {
        $("#dropdown_2").find("option[value="+compatibility[first_input][i]+"]").remove();
    }
    $("#dropdown_2 option").prop("selected", false).filter("[value="+selection+"]").prop("selected",true);
    $("#dropdown_2").trigger("chosen:updated");

};

var exclusive_inputs_2 = function() {
    var selection = $("#dropdown_1").val();
    $("#dropdown_1").empty();
    $.each(options, function(val, text) {
        $("#dropdown_1").append($('<option></option>').val(val).html(text));
    });
    var first_input = $("#dropdown_2").val();
    for (var i=0; i<compatibility[first_input].length; i++) {
        $("#dropdown_1").find("option[value="+compatibility[first_input][i]+"]").remove();
    }
    $("#dropdown_1 option").prop("selected", false).filter("[value="+selection+"]").prop("selected",true);
    $("#dropdown_1").trigger("chosen:updated");
};

var update_units_1 = function() {
    $("#dropdown_1").change(function() {
        var selection = $("#dropdown_1").val();
        $("#units_1").html("("+units[selection]+")");
    })
};

var update_units_2 = function() {
    $("#dropdown_2").change(function() {
        var selection = $("#dropdown_2").val();
        $("#units_2").html("("+units[selection]+")");
    })
};

var exclusive_inputs = function() {
    $(document).ready(function() {
        $("#dropdown_1").change(exclusive_inputs_1);
    });
    $(document).ready(function() {
        $("#dropdown_1").change(exclusive_inputs_2);
    });
};

var update_units = function() {
    $(document).ready(update_units_1);
    $(document).ready(update_units_2);
};

exclusive_inputs();
update_units();
$(document).ready(function() {
    $("select").chosen({width: "80%"});
});
