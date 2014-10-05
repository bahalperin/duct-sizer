// Method to validate width and height.  Checks if two numbers, separated
// by a forward slash were entered.  Then checks if those numbers are in
// an acceptable range.
jQuery.validator.addMethod("split_width_height", function(value,element) {
	var width_height = value.split("/");
	if (width_height.length != 2) {
		return false;
	}
	var width = width_height[0];
	var height = width_height[1];

	if ((width >= 3 && width <= 100) && (height >= 3 && height <= 80)) {
		return true;
	}
	else if ((width >= 3 && width <= 80) && (height >= 3 && height <= 100)) {
		return true;
	}
	else {
		return false;
	}
});

$("#propertyform").validate({
	errorClass: "invalid",
    errorContainer: $("#messageBox"),
 	errorLabelContainer: $("#messageBox ul"),
	wrapper: "li",
	highlight: function(element, errorClass, validClass) {
					$(element).addClass(errorClass);
					$(element.form).find("label[for=" + element.id + "]").addClass(errorClass);
	},
	unhighlight: function(element, errorClass, validClass) {
				$(element).removeClass(errorClass);
					$(element.form).find("label[for=" + element.id + "]").removeClass(errorClass);
	}
});

// Objects storing rules for each property.
var air_flow_rules = {
    required: true,
    range: [30, 100000],
    messages: {
        required: "Air flow can't be left blank.",
        range: "Air flow must be between 30 and 100,000 CFM."
    }
};

var pressure_loss_rules = {
    required: true,
    range: [0.01, 10],
    messages: {
        required: "Pressure loss can't be left blank.",
        range: "Pressure loss must be between 0.01 and 10 in. wg/100 ft."
    }
};

var velocity_rules = {
    required: true,
    range: [300, 12000],
    messages: {
        required: "Velocity can't be left blank.",
        range: "Velocity must be between 300 and 12,000 fpm."
    
    }
};

var diameter_rules = {
    required: true,
    range: [3, 90],
    messages: {
        required: "Diameter can't be left blank.",
        range: "Diameter must be between 3 and 90 in."
    }
};

var width_height_rules = {
    required: true,
    split_width_height: true,
    messages: {
        required: "Width/Height can't be left blank.",
        split_width_height: "Enter width and height separated by a forward slash. (Ex. 12/12, 20/14, 100/80, etc). <br> Width must be between 100 and 3 in.  Height must be between 80 and 3 in."
    }
};

// Object mapping dropdown value (property) to  object
// containing rules for that property.
var the_rules = {
    "air_flow": air_flow_rules,
    "pressure_loss": pressure_loss_rules,
    "velocity": velocity_rules,
    "diameter": diameter_rules,
    "width_height": width_height_rules
};

// Functions that change the rules that apply
// to an input, when the input's corresponding
// dropdown changes values.
var change_rules_1 = function() {
    $("#input_1").rules("remove");
    
    var property = $("#dropdown_1").val();
    $("#input_1").rules("add", the_rules[property]);
};

var change_rules_2 = function() {
    $("#input_2").rules("remove");
    
    var property = $("#dropdown_2").val();
    $("#input_2").rules("add", the_rules[property]);
};

var change_rules = function () {
    $(document).ready(change_rules_1);
    $(document).ready(change_rules_2);
    $("#dropdown_1").change(change_rules_1);
    $("#dropdown_2").change(change_rules_2);
};

change_rules();
