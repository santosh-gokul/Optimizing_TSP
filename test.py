class test:
	def __init__(self,a,b):
		self.a = a
		self.b = b
		print(self)
	def printthem(self):
		print(self.a,self.b)
class t_test(test):
	def __init__(self,a,b):
		test.__init__(self,a,b)
a = t_test(1,2)
a.printthem()
