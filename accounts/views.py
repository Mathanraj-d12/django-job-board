from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import Profile
from django import forms


# def     register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()

#     return render(request, 'accounts/register.html', {'form': form})


# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()

#     for field in form.fields.values():
#         field.widget.attrs['class'] = 'form-control'

#     return render(request, 'accounts/register.html', {'form': form})


# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()

#             role = form.cleaned_data.get('role')
#             Profile.objects.create(user=user, role=role)

#             login(request, user)
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()

#     for field in form.fields.values():
#         if not isinstance(field.widget, forms.RadioSelect):
#             field.widget.attrs['class'] = 'form-control'

#     return render(request, 'accounts/register.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')

            # Update role created by signal
            profile = user.profile
            profile.role = role
            profile.save()

            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    for field in form.fields.values():
        if not isinstance(field.widget, forms.RadioSelect):
            field.widget.attrs['class'] = 'form-control'

    return render(request, 'accounts/register.html', {'form': form})





# def login_view(request):
    # if request.method == 'POST':
    #     form = AuthenticationForm(data=request.POST)
    #     if form.is_valid():
    #         user = form.get_user()
    #         login(request, user)
    #         return redirect('home')
    # else:
    #     form = AuthenticationForm()

    # return render(request, 'accounts/login.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()

    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'accounts/login.html', {'form': form})





def logout_view(request):
    logout(request)
    return redirect('home')
