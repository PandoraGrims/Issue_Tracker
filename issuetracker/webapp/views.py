from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import DeleteView, TemplateView, FormView
from .models import Task
from .forms import TaskForm


class TaskListView(TemplateView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.all()
        context['tasks'] = tasks
        return context


class TaskDetailView(TemplateView):
    model = Task
    template_name = 'CRUD/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        context['task'] = task
        return context


class TaskCreateView(FormView):
    template_name = 'CRUD/task_create.html'
    form_class = TaskForm

    def form_valid(self, form):
        types = form.cleaned_data.pop('types')
        task = form.save()
        task.types.set(types)
        return redirect('webapp:task_detail', pk=task.pk)


class TaskUpdateView(FormView):
    template_name = 'CRUD/task_update.html'
    form_class = TaskForm

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get('pk'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.task
        return kwargs

    def form_valid(self, form):
        types = form.cleaned_data.pop('types')
        form.save()
        self.task.types.set(types)
        return redirect('webapp:task_detail', pk=self.task.pk)


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'CRUD/task_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        context['task'] = task
        return context

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        task.delete()
        return redirect('webapp:task_list')
