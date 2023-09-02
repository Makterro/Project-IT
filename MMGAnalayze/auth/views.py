from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from auth.forms import UserRegistrationForm, UserLoginForm


class UserRegistrationView(View):

    def get(self, request, **kwargs):
        context = self.GetContext()
        return render(request, 'auth/register.html', context=context)

    def post(self, request, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('login')
        else:
            context = self.GetContext(form)
            return render(request, 'auth/login.html', context=context)

    @staticmethod
    def GetContext(baseForm=None):
        context = {
            'form': None
        }
        if baseForm:
            context['form'] = baseForm
        else:
            context['form'] = UserRegistrationForm()
        return context


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'auth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')
