from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import uuid
import boto3

from .models import Moto, Photo
from .forms import MaintenanceForm

S3_BASE_URL =  'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'motocollector'

class MotoCreate(CreateView):
  model = Moto
  fields = '__all__'

class MotoUpdate(UpdateView):
  model = Moto
  fields = ['make', 'model', 'year']

class MotoDelete(DeleteView):
  model = Moto
  success_url = '/motos/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def motos_index(request):
  motos = Moto.objects.all()
  return render(request, 'motos/index.html', { 'motos': motos })

def motos_detail(request, moto_id):
  moto = Moto.objects.get(id=moto_id)
  maintenance_form = MaintenanceForm()
  return render(request, 'motos/detail.html',
    { 'moto': moto, 'maintenance_form': maintenance_form }
  )

  def add_maintenance(request, moto_id):
    form = MaintenanceForm(request.POST)
    if form.is_valid(): 
      new_maintenance = form.save(commit=False)
      new_maintenance.moto_id = moto_id
      new_maintenance.save()
    return redirect('detail', moto_id=moto_id)

  def add_photo(request, moto_id):
    photo_file = request.FILES.get('photo-file', NONE)
    if photo_file:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
