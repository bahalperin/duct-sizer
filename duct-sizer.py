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
import ducts

input_range = {
               "air_flow": {"min": 30, "max": 100000},
               "static_pressure": {"min": 0.01, "max": 10},
               "velocity": {"min": 300, "max": 12000},
               "diameter": {"min": 3, "max": 90},
               "width": {"min": 4, "max": 120},
               "height": {"min": 4, "max": 120}
}

def validate_inputs(inputs):
	if inputs["diameter"] and (inputs["width"] or inputs["height"]):
		return False
	if inputs["width"] and not inputs["height"]:
		return False
	if inputs["height"] and not inputs["width"]:
		return False
	if inputs["static_pressure"] and inputs["velocity"]:
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

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
		
class MainPage(Handler):
    def get(self):
        self.render("duct-sizer.html")
		
    def post(self):
        user_inputs = {
                  "air_flow": self.request.get("air_flow"),
                  "static_pressure": self.request.get("static_pressure"),
                  "velocity": self.request.get("velocity"),
                  "diameter": self.request.get("diameter"),
                  "width": self.request.get("width"),
                  "height": self.request.get("height")
        }
		
		
        if validate_inputs(user_inputs):
            inputs = {key:float(value) for key, value in user_inputs.iteritems() if value}
            duct = ducts.Duct(inputs.get("air_flow"),inputs.get("static_pressure"),
                              inputs.get("velocity"),inputs.get("diameter"),
                              inputs.get("width"),inputs.get("height"))
			
            self.render("duct-sizer.html",duct=duct,
                        air_flow=user_inputs["air_flow"], static_pressure=user_inputs["static_pressure"],
                        velocity=user_inputs["velocity"], diameter=user_inputs["diameter"],
                        width=user_inputs["width"], height=user_inputs["height"])
			
        else:
            error = "Something went wrong..."
            self.render("duct-sizer.html",error=error)
		
		
	
app = webapp2.WSGIApplication([
    ('/', MainPage)], debug=True)
