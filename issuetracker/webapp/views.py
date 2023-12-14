from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskCreateForm, TaskUpdateForm


class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'CRUD/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'CRUD/task_create.html'
    success_url = reverse_lazy('webapp:task_list')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'CRUD/task_update.html'
    success_url = reverse_lazy('webapp:task_list')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'CRUD/task_delete.html'
    success_url = reverse_lazy('webapp:task_list')
