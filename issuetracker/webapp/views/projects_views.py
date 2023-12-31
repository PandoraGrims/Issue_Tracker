from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.html import urlencode
from webapp.forms import TaskForm, SearchForm, ProjectForm, ProjectUsersForm
from webapp.models import Task, Project
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView


class ProjectListView(ListView):
    model = Project
    template_name = 'List/project_list_view.html'
    context_object_name = 'projects'
    ordering = ("-start_date",)
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["form"] = self.form
        if self.search_value:
            context["query"] = urlencode({'search': self.search_value})
            context["search_value"] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        search_value = self.request.GET.get('search')
        if search_value:
            queryset = queryset.filter(Q(name__icontains=search_value) | Q(description__icontains=search_value))
        return queryset


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'CRUDprojects/project_detail_view.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        tasks = project.tasks.all()
        context['tasks'] = tasks
        return context


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "CRUDprojects/project_create_view.html"
    permission_required = "webapp.add_project"

    def get_success_url(self):
        return reverse("webapp:task_create", kwargs={"pk": self.object.pk})


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "CRUDprojects/project_update_view.html"
    permission_required = "webapp.change_project"

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()

    def get_success_url(self):
        return reverse("webapp:project_detail_view", kwargs={"pk": self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = "CRUDprojects/project_delete_view.html"
    success_url = reverse_lazy("webapp:index")
    permission_required = "webapp.delete_project"


class ChangeUsersInProjectView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectUsersForm
    template_name = "change_users_in_project.html"
    permission_required = "webapp.add_users_in_project"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        project = form.save()
        project.users.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()

    def get_success_url(self):
        return reverse("webapp:index")
