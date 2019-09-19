from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User

MAINT = (
    ('O', 'Oil Change'),
    ('L', 'Lube Chain'),
    ('T', 'Tire Check')

)
class Moto(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.make
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'moto_id': self.id})
    def maintained_recently(self):
        return self.maintenance_set.filter(date=date.today()).count() >= len(MAINT)
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

