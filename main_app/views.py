from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3

from .models import Moto
from .forms import MaintenanceForm

S3_BASE_URL =  'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'motocollector'

class MotoCreate(CreateView):
  model = Moto
  fields = ['make', 'model', 'year']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

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

@login_required
def motos_index(request):
  motos = Moto.objects.all()
  return render(request, 'motos/index.html', { 'motos': motos })

@login_required
def motos_detail(request, moto_id):
  moto = Moto.objects.get(id=moto_id)
  maintenance_form = MaintenanceForm()
  return render(request, 'motos/detail.html',
    { 'moto': moto, 'maintenance_form': maintenance_form }
  )
@login_required
def add_maintenance(request, moto_id):
    form = MaintenanceForm(request.POST)
    if form.is_valid(): 
      new_maintenance = form.save(commit=False)
      new_maintenance.moto_id = moto_id
      new_maintenance.save()
    return redirect('detail', moto_id=moto_id)
@login_required
def add_photo(request, moto_id):
    photo_file = request.FILES.get('photo-file', NONE)
    if photo_file:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
