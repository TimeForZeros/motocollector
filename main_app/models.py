from django.db import models



# Create your models here.
class Moto(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(max_length=4)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'moto_id': self.id})

class Maintenance(models.Model):
    date = models.DateField('Maintenance date')
    maintenance = models.Charfield(
        max_length=1,
        choices=MAINT,
        default=MAINT[0][0]
        )
moto = models.ForeignKey(Moto, on_delete=models.CASCADE)

def __str__(self):
    return f'{self.get_meal_display()} on {self.date}'