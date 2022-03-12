import random

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import LabelForm, LoginForm
from .models import MessageMisconception, TelegramMessage, Misconception, User


def index(request):
    return HttpResponse("This is the survey app index page.")


def login(request):
    # In case of a POST request, create a form instance and populate it with data from
    # the request
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Get user ip to detect possible username collisions
            ip = None
            if "REMOTE_ADDR" in request.META:
                ip = request.META.get("REMOTE_ADDR")
            user_name = form.cleaned_data["user_name"]
            request.session["user"] = user_name
            if not User.objects.filter(name=user_name).exists():
                user = User(name=user_name, ip=ip)
                user.save()
            else:
                user = User.objects.filter(name=user_name)[0]
                if ip != user.ip:
                    return HttpResponseRedirect("confirm")
            return HttpResponseRedirect("label")
    # In case of a GET request (or any other method), create a blank form
    context = {"form": LoginForm()}
    return render(request, "labeling_app/login.html", context)


def logout(request):
    if "user" in request.session.keys():
        del request.session["user"]
    return render(request, "labeling_app/logout.html")


def confirm_name(request):
    return render(request, "labeling_app/confirm_name.html")


def welcome(request):
    return render(request, "labeling_app/welcome.html")


def warning(request):
    return render(request, "labeling_app/warning.html")


# def get_messages_not_labeled_by_user(request):
#     if not 'user' in request.session.keys():
#         # If the user is not logged in, go to login view
#         return HttpResponseRedirect('login')
#     user_name = request.session['user']
#     messages_not_labeled_by_user = TelegramMessage.filter()


def labelling(request):
    # If the user is not logged in, go to login view
    if "user" not in request.session.keys():
        return HttpResponseRedirect("login")
    # In case of a POST request, create a form instance and populate it with data from
    # the request
    if request.method == "POST":
        form_data = request.POST
        form = LabelForm(request.POST)
        if form.is_valid():
            selected_misconception_ids = form.cleaned_data["selected_misconception_ids"]
            for misconception_id in selected_misconception_ids:
                label = MessageMisconception(
                    message=TelegramMessage.objects.get(pk=form_data["message_id"]),
                    misconception=Misconception.objects.get(pk=misconception_id),
                    user=User.objects.get(pk=form_data["user_id"]),
                )
                label.save()
            # If no label was selected, create an entry indicating that the message was
            # labeled, even though no labels were assigned
            if len(selected_misconception_ids) == 0:
                label = MessageMisconception(
                    message=TelegramMessage.objects.get(pk=form_data["message_id"]),
                    misconception=None,
                    user=User.objects.get(pk=form_data["user_id"]),
                )
                label.save()
            return HttpResponseRedirect("label")
        else:
            print("Form invalid")
    # In case of a GET request (or any other method), retrieve a random message to show
    # and create a labeling form. Or if no message to label remains, redirect to 'done'
    # page.
    user = User.objects.filter(name=request.session["user"])[0]
    unlabeled_messages = list(
        TelegramMessage.objects.exclude(
            id__in=MessageMisconception.objects.filter(user_id=user.id).values(
                "message_id"
            )
        )
    )
    number_of_unlabeled_messages = len(unlabeled_messages)
    if number_of_unlabeled_messages > 0:
        random_message = random.sample(unlabeled_messages, 1)[0]
        context = {"user": user, "message": random_message, "form": LabelForm()}
        return render(request, "labeling_app/label.html", context)
    else:
        return HttpResponseRedirect("done")


def done(request):
    return render(request, "labeling_app/done.html")


def facts(request):
    return render(request, "labeling_app/facts.html")
