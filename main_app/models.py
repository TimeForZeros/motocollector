from django.db import models
from django.urls import reverse

MAINT = (
    ('O', 'Oil Change'),
    ('L', 'Lube Chain'),
    ('T', 'Tire Check')

)


# Create your models here.
class Moto(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.make
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'moto_id': self.id})

class Maintenance(models.Model):
    date = models.DateField('maintenance date')
    maintenance = models.CharField(
        max_length=1,
        choices=MAINT,
        default=MAINT[0][0]
        )
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_maint_display()} on {self.date}'

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Photo for moto_id: {self.moto_id} @{self.url}'