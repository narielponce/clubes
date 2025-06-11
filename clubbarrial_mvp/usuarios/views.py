from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('usuarios:login')

class RegistroView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('usuarios:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Usuario registrado exitosamente. Ahora puedes iniciar sesión.')
        return response

class PerfilView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'usuarios/perfil.html'
    context_object_name = 'usuario'
    
    def get_object(self):
        return self.request.user

class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'usuarios/editar_perfil.html'
    success_url = reverse_lazy('usuarios:perfil')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado exitosamente.')
        return super().form_valid(form)

class ListaUsuariosView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'usuarios/lista_usuarios.html'
    context_object_name = 'usuarios'
    paginate_by = 20
    
    def get_queryset(self):
        return CustomUser.objects.filter(activo=True).order_by('last_name', 'first_name')

@login_required
def dashboard(request):
    """Vista principal del dashboard según el rol del usuario"""
    user = request.user
    context = {
        'user': user,
        'role_display': user.get_role_display_name(),
    }
    
    if user.role == 'admin':
        # Dashboard para administradores
        context.update({
            'total_usuarios': CustomUser.objects.filter(activo=True).count(),
            'usuarios_recientes': CustomUser.objects.filter(activo=True).order_by('-fecha_ingreso')[:5],
        })
        return render(request, 'usuarios/dashboard_admin.html', context)
    
    elif user.role == 'coordinador':
        # Dashboard para coordinadores
        from disciplinas.models import Disciplina
        context.update({
            'disciplinas_coordinadas': Disciplina.objects.filter(coordinador=user),
        })
        return render(request, 'usuarios/dashboard_coordinador.html', context)
    
    else:
        # Dashboard general para socios, profesores, etc.
        return render(request, 'usuarios/dashboard_general.html', context)
