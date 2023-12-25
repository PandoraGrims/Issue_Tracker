from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, TemplateView, FormView, UpdateView, CreateView, DetailView
from webapp.models import Task, Project
from webapp.forms import TaskForm


class TaskListView(TemplateView):
    model = Task
    template_name = 'List/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.all()
        context['tasks'] = tasks
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'CRUDtask/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    form_class = TaskForm
    template_name = "CRUDtask/task_create.html"
    success_url = reverse_lazy("webapp:task_view")

    def get_success_url(self):
        return reverse("webapp:task_view", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        task = form.save(commit=False)
        task.project = project
        task.save()
        return redirect("webapp:project_detail_view", pk=project.pk)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "CRUDtask/task_update.html"

    def get_success_url(self):
        return reverse("webapp:project_detail_view", kwargs={"pk": self.object.project.pk})




class TaskDeleteView(DeleteView):
    model = Task
    template_name = "CRUDtask/task_delete.html"
    success_url = reverse_lazy("webapp:index")
