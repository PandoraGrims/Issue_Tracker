from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import DeleteView, TemplateView
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


class TaskCreateView(TemplateView):
    model = Task
    template_name = 'CRUD/task_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            types = form.cleaned_data.pop('types')
            task = Task.objects.create(
                summary=form.cleaned_data['summary'],
                description=form.cleaned_data['description'],
                status=form.cleaned_data['status'],
            )
            task.types.set(types)
            return redirect('webapp:task_detail', pk=task.pk)

        return render(request, 'CRUD/task_create.html', {'form': form})


class TaskUpdateView(View):
    model = Task
    template_name = 'CRUD/task_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TaskForm(initial={
            'summary': self.task.summary,
            'description': self.task.description,
            'status': self.task.status,
            'types': self.task.types.all()
        })
        return render(request, 'CRUD/task_update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            types = form.cleaned_data.pop('types')
            self.task.summary = form.cleaned_data.get('summary')
            self.task.description = form.cleaned_data.get('description')
            self.task.status = form.cleaned_data.get('status')

            self.task.save()
            self.task.types.set(types)
            return redirect('webapp:task_detail', pk=self.task.pk)
        return render(request, 'CRUD/task_update.html', {'form': form})


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
