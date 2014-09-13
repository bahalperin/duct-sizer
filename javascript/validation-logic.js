$.validator.addMethod("empty", function(value, element) {
	return (value === "");}, "This field must remain empyt!");
$("#propertyform").validate({
	errorLabelContainer: "#messageBox",
	wrapper: "li"
});
$("#air_flow").rules("add", {
	range: [30,100000],
	require_from_group_exact: [2, ".property"]
});
$("#static_pressure").rules("add", {
	range: [0.01, 10],
	empty: {
		depends: function() {
			return ($("#velocity").val() != "")
		}
	}
});
$("#velocity").rules("add", {
	range: [300, 12000],
	empty: {
		depends: function() {
			return ($("#static_pressure").val() != "")
		}
	},
	messages: {
		empty: "Can't input velocity with static pressure!"
	}
});
$("#diameter").rules("add", {
	range: [3, 90],
	empty: {
		depends: function() {
			return (($("#width").val() != "") || ($("#height").val() != ""))
		}
	}
});
$("#width").rules("add", {
	range: function() {
		if ($("#height").val() > 80) {
			return [4, 80]
		}
		else {
			return [4, 120]
		}
	},
	required: {
		depends: function() {
			return ($("#height").val() != "")
		}
	}
});
$("#height").rules("add", {
	range: function() {
		if ($("#width").val() > 80) {
			return [4, 80]
		}
		else {
			return [4, 120]
		}
	},
	required: {
		depends: function() {
			return ($("#width").val() != "")
		}
	}
});
