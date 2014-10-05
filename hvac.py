"""This module currently only contains the class Duct which is used to calculate
all properties of a duct, assuming you know exactly two.  I plan to add more 
classes to aid in other HVAC calculations.
"""

import math

class Duct:
	"""Instances take duct properties as arguments and calculate all remaining properties."""
	def __init__(self,air_flow=None,pressure_loss=None,velocity=None,diameter=None,width=None,height=None):
		"""Defines instance properties using instance arguments, then calculates all missing properties.

		Args:
			(Note: all arguments are optional.  To get accurate results, only two arguments should be input
			into a duct instance (3 if using width and height)).

			air_flow (float): Air flow rate through duct in cubic feet per minute (CFM).
			pressure_loss (float): Pressure loss along duct in inches water gauge per 100 feet of duct. (in. wg/100 ft.).
			velocity (float): Velocity of air moving through duct in feet per minute (fpm).
			diameter (float): Diameter of duct (if round) in inches (in.).
			width (float): Width of duct (if rectangular) in inches (in.).
			height (float): Height of duct (if rectangular) in inches (in.).
		"""

		self.air_flow = air_flow
		self.pressure_loss = pressure_loss
		self.velocity = velocity
		self.diameter = diameter
		if (width and height) and not diameter:
			self.diameter = 1.3 * ((width*height)**0.625) / ((width+height)**0.25)
		self.calculate_properties()
		self.rectangular_dimensions = self.rectangular_dimensions()
		
	def area(self):
		"""Returns area of a round duct."""
		return math.pi * (0.5*self.diameter) ** 2
		
		
	def rectangular_dimensions(self,min_size=3,max_size=100,increment=1):
		"""Calculates equivalent rectangular duct dimensions (within a given range) for the duct instance's diameter.

		Args:
			min_size (int, optional): Smallest size a duct side can be, in inches (in.).
			max_size (int, optional): Largest size a duct side can be, in inches (in.).
			increment (int, optional): After width and height values are calculated, increase width by this amount and repeat calculation.
		"""
		dimensions = {}
		width = min_size
		height = 0
		while True:
			if 1.3 * (((max_size*width) ** .625)/((max_size+width) ** .25)) >= self.diameter:
				
				while (1.3 * (((height*width) ** .625)/((height+width) ** .25))) < self.diameter:
					height += 1
				while (1.3 * (((height*width) ** .625)/((height+width) ** .25))) > self.diameter:
					height -= 0.01
				

				height = round(height,1)
				if width > height:
					break
				
				if height <= max_size:
					dimensions[width] = height
			
			width += increment

		dimensions = {width:(int(height) if int(height) == height else height) for width, height in dimensions.iteritems()}
		
		return dimensions
	
	def calculate_properties(self):
		"""If duct instance has two properties, this method calculates the remaining properties."""			
		if self.air_flow and self.pressure_loss:
			self.diameter = (0.109136*(self.air_flow**1.9)/self.pressure_loss)**(1/5.02)
			self.velocity = self.air_flow/(self.area()/144)	
			return	
		if self.air_flow and self.velocity:
			self.diameter = ((((576*self.air_flow)/self.velocity)/math.pi))**0.5
			self.pressure_loss = 0.109136*(self.air_flow**1.9)/(self.diameter**5.02)
			return
		if self.air_flow and self.diameter:
			self.pressure_loss = 0.109136*(self.air_flow**1.9)/(self.diameter**5.02)
			self.velocity = self.air_flow/(self.area()/144)
			return
		if self.pressure_loss and self.diameter:
			self.air_flow = ((self.pressure_loss * (self.diameter ** 5.02))/0.109136)**(1/1.9)
			self.velocity = self.air_flow/(self.area()/144)	
			return
		if self.velocity and self.diameter:
			self.air_flow = self.velocity*(self.area()/144)
			self.pressure_loss = 0.109136*(self.air_flow**1.9)/(self.diameter**5.02)
			return
			
	def format_properties(self):
		"""Removes unnecessary decimal places from duct instance properties for displaying data."""
		self.air_flow = self.air_flow and round(self.air_flow,1)
		self.pressure_loss = self.pressure_loss and round(self.pressure_loss,3)
		self.velocity = self.velocity and round(self.velocity,1)
		self.diameter = self.diameter and round(self.diameter,1)


