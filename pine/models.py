from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True, unique=True)
	def __str__(self):
		return self.name
     
class PinePrice(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
     name = models.CharField(max_length=200, null=True)
     price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

     def __str__(self):
          return self.name
     
class PineValue(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
     value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
     date = models.DateField(auto_now_add=False, null=True)

     

class Crop(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
     number_planted = models.PositiveIntegerField(null=True)
     plant_date = models.DateField(auto_now_add=False, null=True)
     price = models.ForeignKey(PinePrice, on_delete=models.SET_NULL, null=True)

     

class Yield(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
     number_yield = models.PositiveIntegerField(null=True)
     harvest_date = models.DateField(auto_now_add=False, null=True)
     value = models.ForeignKey(PineValue, on_delete=models.SET_NULL, null=True)
     calculated_value = models.FloatField(null=True)

class WorkerPays(models.Model):
      name = name = models.CharField(max_length=200, null=True)
      price_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True)
      date = models.DateField(auto_now_add=False, null=True)

      def __str__(self):
            return self.name