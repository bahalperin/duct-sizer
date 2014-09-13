import math

class Duct:
	def __init__(self,air_flow=None,static_pressure=None,velocity=None,diameter=None,width=None,height=None):
		self.air_flow = air_flow
		self.static_pressure = static_pressure
		self.velocity = velocity
		self.diameter = diameter
		if (width and height) and not diameter:
			self.diameter = 1.3 * ((width*height)**0.625) / ((width+height)**0.25)
		self.calculate_properties()
		self.rectangular_dimensions = self.rectangular_dimensions()
		self.format_properties()
		
	def area(self):
		return math.pi * (0.5*self.diameter) ** 2
		
		
	def rectangular_dimensions(self,min_size=4,max_size=120,increment=1):
		dimensions = {}
		width = min_size
		height = 0
		while True:
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

		sorted_dimensions = sorted([(x,y) for x,y in dimensions.iteritems()])
		return sorted_dimensions
	
	def calculate_properties(self):			
		if self.air_flow and self.static_pressure:
			self.diameter = (0.109136*(self.air_flow**1.9)/self.static_pressure)**(1/5.02)
			self.velocity = self.air_flow/(self.area()/144)	
			return	
		if self.air_flow and self.velocity:
			self.diameter = ((((576*self.air_flow)/self.velocity)/math.pi))**0.5
			self.static_pressure = 0.109136*(self.air_flow**1.9)/(self.diameter**5.02)
			return
		if self.air_flow and self.diameter:
			self.static_pressure = 0.109136*(self.air_flow**1.9)/(self.diameter**5.02)
			self.velocity = self.air_flow/(self.area()/144)
			return
		if self.static_pressure and self.diameter:
			self.air_flow = ((self.static_pressure * (self.diameter ** 5.02))/0.109136)**(1/1.9)
			self.velocity = self.air_flow/(self.area()/144)	
			return
		if self.velocity and self.diameter:
			self.air_flow = self.velocity*(self.area()/144)
			self.static_pressure = 0.109136*(self.air_flow**1.9)/(self.diameter**5.02)
			return
			
	def format_properties(self):
		self.air_flow = self.air_flow and round(self.air_flow,1)
		self.static_pressure = self.static_pressure and round(self.static_pressure,3)
		self.velocity = self.velocity and round(self.velocity,1)
		self.diameter = self.diameter and round(self.diameter,1)


