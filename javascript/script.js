/*$(document).ready(function() {
    $("#diameter").keyup(function() {
        if ($(this).val() !== "") {
        	$("#width_height").addClass('possum');
            $("#width_height").prop('disabled', true);
        } else {
            $('#width_height').prop('disabled', false);
            $("#width_height").removeClass('possum');
        }
    });
});

$(document).ready(function() {
    $("#width_height").keyup(function() {
        if ($(this).val() !== "") {
        	$("#diameter").addClass('possum');
            $("#diameter").prop('disabled', true);
        } else {
            $('#diameter').prop('disabled', false);
            $("#diameter").removeClass('possum');
        }
    });
});

$(document).ready(function() {
    $(".property").keyup(function() {
        var count = 0;
        $(".property").each(function(i, el) {
            if ($(el).val() !== "") {
              count += 1;
            }
        });
        if (count >= 2) {
        	$(".property").each(function(i, el) {
            if ($(el).val() == "") {
              $(el).prop('disabled', true);
            }
        });	
        }
        else {
        	$(".property:not(.possum)").prop('disabled', false);
        }
    });
});

$(document).ready(function() {
        var count = 0;
        $(".property").each(function(i, el) {
            if ($(el).val() !== "") {
              count += 1;
            }
        });
        if (count >= 2) {
        	$(".property").each(function(i, el) {
            if ($(el).val() == "") {
              $(el).prop('disabled', true);
            }
        });	
        }
        else {
        	$(".property:not(.possum)").prop('disabled', false);
        }
});

$(document).ready(function() {
    $(".property:not(#width_height)").keyup(function() {
        if ((!($.isNumeric($(this).val()))) && ($(this).val() != "")) {
        	$(this).addClass("red");
        	$("input[type=submit]").prop('disabled', true);
        }
        else {
        	$(this).removeClass("red");
        	$("input[type=submit]").prop('disabled', false);
        }
    });
});
*/
	
