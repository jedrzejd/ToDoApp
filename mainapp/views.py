from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg, Max, Min, Sum
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ToDoApp.settings import EMAIL_HOST_USER
from .models import Task, TaskList
from .forms import NewUserForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


class ListListView(ListView):
    model = TaskList
    template_name = "mainapp/home.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return TaskList.objects.filter(owner=self.request.user)

    def get_context_data(self):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            countTaskInList = TaskList.objects.filter(owner=self.request.user).count()
            allTaskInList=0
            maxTaskInList=-1
            minTaskInList=-1
            for list in TaskList.objects.filter(owner=self.request.user):
                allTaskInList += Task.objects.filter(todo_list_id=list.id).count()
                if maxTaskInList == -1:
                    maxTaskInList = Task.objects.filter(todo_list_id=list.id).count()
                else:
                    maxTaskInList = max(Task.objects.filter(todo_list_id=list.id).count(), maxTaskInList)
                if minTaskInList == -1:
                    minTaskInList = Task.objects.filter(todo_list_id=list.id).count()
                else:
                    minTaskInList = min(Task.objects.filter(todo_list_id=list.id).count(), minTaskInList)
            if countTaskInList == 0:
                meanTaskInList = 0
            else:
                meanTaskInList = allTaskInList / countTaskInList
            if maxTaskInList == -1:
                maxTaskInList = 'Brak'
            if minTaskInList == -1:
                minTaskInList = 'Brak'
            context["countLists"] = countTaskInList
            context["countTasks"] = allTaskInList
            context["max"] = maxTaskInList
            context["min"] = minTaskInList
            context["mean"] = meanTaskInList
        return context


class TaskListView(ListView):
    model = Task
    template_name = "mainapp/list.html"

    def get_template_names(self):
        a = TaskList.objects.filter(owner=self.request.user, id=self.kwargs["list_id"])
        if len(a) > 0:
            return ['mainapp/list.html']
        else:
            return ['mainapp/home.html']

    def get_queryset(self):
        a = TaskList.objects.filter(owner=self.request.user, id=self.kwargs["list_id"])
        if len(a) > 0:
            return Task.objects.filter(todo_list_id=self.kwargs["list_id"]).order_by('end_date')

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = TaskList.objects.get(id=self.kwargs["list_id"])
        context["count"] = Task.objects.count()
        return context


class ListCreate(CreateView):
    model = TaskList
    fields = ['title']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Dodaj nową listę"
        return context


class TaskCreate(CreateView):
    model = Task
    fields = [
        'todo_list',
        'title',
        'description',
        'end_date',
    ]

    def get_initial(self):
        initial_data = super(TaskCreate, self).get_initial()
        todo_list = TaskList.objects.get(id=self.kwargs["list_id"])
        initial_data['todo_list'] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(TaskCreate, self).get_context_data()
        todo_list = TaskList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Stwórz nowe zadanie"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class TaskUpdate(UpdateView):
    model = Task
    fields = [
        "todo_list",
        "title",
        "description",
        "end_date",
    ]

    def get_context_data(self):
        context = super(TaskUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edytuj zadanie"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ListDelete(DeleteView):
    model = TaskList
    success_url = reverse_lazy("index")


class TaskDelete(DeleteView):
    model = Task

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Rejestracja zakończona sukcesem")
            return redirect("index")
        messages.error(request, "Niepoprawne dane")
    form = NewUserForm()
    return render(request=request, template_name="mainapp/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Jesteś zalogowany w aplikacji jako {username}.")
                return redirect("index")
            else:
                messages.error(request, "Niepoprawny login lub hasło/")
        else:
            messages.error(request, "Niepoprawny login lub hasło/")
    form = AuthenticationForm()
    return render(request=request, template_name="mainapp/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Wylogowałeś się z aplikacji.")
    return redirect("index")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Prośba o Reset Hasła"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '80284.pythonanywhere.com',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject=subject,
                            message=email,
                            from_email=EMAIL_HOST_USER,
                            recipient_list=[user.email]
                        )
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})
