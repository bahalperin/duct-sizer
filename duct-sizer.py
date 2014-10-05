#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import math
import hvac


input_range = {
    "air_flow": {"min": 30, "max": 100000},
    "pressure_loss": {"min": 0.01, "max": 10},
    "velocity": {"min": 300, "max": 12000},
    "diameter": {"min": 3, "max": 90},
    "width": {"min": 4, "max": 100},
    "height": {"min": 4, "max": 100}
}

options = {
    "air_flow": "Air Flow",
    "pressure_loss": "Pressure Loss",
    "velocity": "Velocity",
    "diameter": "Diameter",
    "width_height": "Width/Height"
}

compatibility = {
    "air_flow":  ["air_flow"],
    "pressure_loss": ["velocity","pressure_loss"],
    "velocity": ["velocity", "pressure_loss"],
    "diameter": ["diameter", "width_height"],
    "width_height": ["diameter", "width_height"]
}

units = {
    "air_flow": "CFM",
    "pressure_loss": "in. wg/100 ft.",
    "velocity": "fpm",
    "diameter": "in.",
    "width_height": "in."
}

# Function to break input input width_height into two values,
# width and height.  If splitting width_height doesn't give
# a list of length two, return None for width and height,
# which will cause validate_inputs to return False.
# (I should think of a more robust way to gaurantee a
# False result from validate_inputs)
def split_width_height(width_height):
	split_width_height = width_height.split('/')
	if len(split_width_height) == 2:
		width, height = width_height.split('/')
		return width, height
	return None, None

# Function to confirm no illegal inputs have been submitted.
# Values must be within the proper ranges (defined in input_range dictionary).
# Only two values can be submitted (technically 3 if one is width/height).
# Incompatible inputs can't be submitted together (defined in compatibility dictionary).
# (This function is messy and could use some refactoring when I have some time).
def validate_inputs(inputs):
	if inputs["diameter"] and (inputs["width"] or inputs["height"]):
		return False
	if inputs["width"] and not inputs["height"]:
		return False
	if inputs["height"] and not inputs["width"]:
		return False
	if inputs["pressure_loss"] and inputs["velocity"]:
		return False
	
	inputs = {key:value for key,value in inputs.iteritems() if value}
	
	if inputs.get("width") and len(inputs) != 3:
		return False
	if not inputs.get("width") and len(inputs) != 2:
		return False
	
	for key, value in inputs.iteritems():
		try:
			inputs[key] = float(value)
		except:
			return False

	for key, value in inputs.iteritems():
		if value < input_range[key]["min"] or value > input_range[key]["max"]:
			return False
	
	if inputs.get("width") > 80 and inputs.get("height") > 80:
		return False
	
	return True


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# Handler class to simplify rendering app.  Taken from Udacity Web Development course.
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

# Hander for duct sizer page		
class DuctSizer(Handler):
    def get(self):
        self.render("duct-sizer.html", options=options,dropdown_1="air_flow",
                    dropdown_2="pressure_loss",compatibility=compatibility, units=units)
		
    def post(self):
        # Get values from inputs and selects (dropdowns).
        dropdown_1 = self.request.get("dropdown_1")
        dropdown_2 = self.request.get("dropdown_2")
        input_1 = self.request.get("input_1")
        input_2 = self.request.get("input_2")

        user_inputs = {
               "air_flow": None,
               "pressure_loss": None,
               "velocity": None,
               "diameter": None,
               "width": None,
               "height": None
        }

        width = None
        height = None

        # If width_height was submitted, split it into width and height and save it in
        # user_inputs.  Save other input in user_inputs.  
        # If width_height wasn't submitted, just save both inputs in user_inputs.
        if dropdown_1 == "width_height":
           user_inputs["width"], user_inputs["height"] = split_width_height(input_1)
           user_inputs[dropdown_2] = input_2

        elif dropdown_2 == "width_height":
        	user_inputs["width"], user_inputs["height"] = split_width_height(input_2)
        	user_inputs[dropdown_1] = input_1
        else:
            user_inputs[dropdown_1] = input_1
            user_inputs[dropdown_2] = input_2

        # If inputs are valid, create a duct instance using user_inputs.  Then render
        # the duct-sizer.html with the duct instance and all user inputs and necessary
        # dictionaries.
        if validate_inputs(user_inputs):
            inputs = {key:float(value) for key, value in user_inputs.iteritems() if value}
            duct = hvac.Duct(inputs.get("air_flow"),inputs.get("pressure_loss"),
                              inputs.get("velocity"),inputs.get("diameter"),
                              inputs.get("width"),inputs.get("height"))
			
            duct.format_properties()
            self.render("duct-sizer.html",duct=duct,
                        options=options, input_1=input_1, input_2=input_2,
                        dropdown_1=dropdown_1, dropdown_2=dropdown_2,compatibility=compatibility,units=units)
		
        # Otherwise render page with user inputs and an error message.  
        else:
            error = "There was an error with some of your inputs.  Please try again."
            self.render("duct-sizer.html",error=error, options=options, input_1=input_1,
                        input_2=input_2, dropdown_1=dropdown_1, dropdown_2=dropdown_2, compatibility=compatibility, units=units)
		
		
app = webapp2.WSGIApplication([
    ('/', DuctSizer)], debug=True)
