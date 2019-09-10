from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Moto
from .forms import MaintenanceForm

class MotoCreate(CreateView):
  model = Moto
  fields = '__all__'

class MotoUpdate(UpdateView):
  model = Moto
  fields = ['breed', 'description', 'age']

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
