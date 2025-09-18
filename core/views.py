from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db.models import Max

from .forms import GenerateFeesForm
from .models import Member, Fee, Club
from users.models import Membership

# --- Mixins de Seguridad y Contexto ---

class ClubRequiredMixin(LoginRequiredMixin):
    """
    Verifica que un usuario esté logueado y tenga membresía en el club.
    Si el usuario está logueado para otro club, cierra su sesión.
    """
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request, 'club') or not request.club:
            return HttpResponseForbidden("Acceso denegado: Club no especificado o no encontrado.")

        # Si el usuario no está autenticado, deja que el padre (LoginRequiredMixin) maneje la redirección.
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        # Si el usuario SÍ está autenticado, verificamos la membresía.
        if not request.user.memberships.filter(club=request.club).exists():
            logout(request)
            messages.info(request, "Para acceder a este club, por favor, inicia sesión.")
            login_url = reverse('login')
            redirect_url = f'{login_url}?next={request.path}'
            return redirect(redirect_url)
        
        # Si todo está en orden, procede con la vista.
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(ClubRequiredMixin, UserPassesTestMixin):
    """
    Asegura que el usuario sea miembro del club y tenga el rol de ADMIN.
    """
    def test_func(self):
        return self.request.user.memberships.filter(
            club=self.request.club, 
            role=Membership.ROLE_ADMIN
        ).exists()

# --- Vistas Globales y de Club ---

class SelectClubView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        memberships = request.user.memberships.all()
        if memberships.count() == 1:
            membership = memberships.first()
            return redirect('club_home', club_slug=membership.club.subdomain)
        elif memberships.count() > 1:
            return render(request, 'core/select_club.html', {'memberships': memberships})
        else:
            messages.error(request, "No tienes membresía en ningún club.")
            return redirect('login')

class ClubHomeView(ClubRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect('dashboard', club_slug=kwargs['club_slug'])

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        club_slug = kwargs.get('club_slug')
        logout(request)
        messages.success(request, "Has cerrado sesión exitosamente.")
        return redirect('club_home', club_slug=club_slug)

class DashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.request.club
        context['club'] = club
        context['active_members_count'] = Member.objects.filter(club=club, status=Member.STATUS_ACTIVE).count()
        context['pending_fees_count'] = Fee.objects.filter(member__club=club, status=Fee.STATUS_PENDING).count()
        return context

class GenerateFeesView(AdminRequiredMixin, FormView):
    template_name = 'core/generate_fees.html'
    form_class = GenerateFeesForm

    def get_success_url(self):
        return reverse_lazy('generate_fees', kwargs={'club_slug': self.request.club.subdomain})

    def form_valid(self, form):
        club = self.request.club
        data = form.cleaned_data
        active_members = Member.objects.filter(club=club, status=Member.STATUS_ACTIVE)
        if not active_members.exists():
            messages.warning(self.request, f"No se encontraron socios activos en el club {club.name}.")
            return super().form_valid(form)

        fees_to_create = [Fee(member=member, description=data['description'], amount=data['amount'], period=data['period'], due_date=data['due_date']) for member in active_members]
        Fee.objects.bulk_create(fees_to_create)
        messages.success(self.request, f"¡Éxito! Se generaron {len(fees_to_create)} cuotas para el club {club.name}.")
        return super().form_valid(form)

# --- Vistas para la Gestión de Socios ---

class MemberListView(AdminRequiredMixin, ListView):
    model = Member
    template_name = 'core/member_list.html'
    context_object_name = 'members'

    def get_queryset(self):
        return Member.objects.filter(club=self.request.club)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.request.club
        return context

class MemberCreateView(AdminRequiredMixin, CreateView):
    model = Member
    template_name = 'core/member_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'join_date', 'status']

    def get_success_url(self):
        return reverse_lazy('member_list', kwargs={'club_slug': self.request.club.subdomain})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.club = self.request.club
        last_member_number = Member.objects.filter(club=self.object.club).aggregate(Max('member_number'))['member_number__max']
        self.object.member_number = (last_member_number or 0) + 1
        self.object.save()
        messages.success(self.request, f"Socio {self.object.full_name} creado con éxito con el número {self.object.member_number}.")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.request.club
        return context

class MemberUpdateView(AdminRequiredMixin, UpdateView):
    model = Member
    template_name = 'core/member_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'join_date', 'status']

    def get_queryset(self):
        return Member.objects.filter(club=self.request.club)

    def get_success_url(self):
        return reverse_lazy('member_list', kwargs={'club_slug': self.request.club.subdomain})

    def form_valid(self, form):
        messages.success(self.request, "Socio actualizado con éxito.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.request.club
        return context

class MemberDeleteView(AdminRequiredMixin, DeleteView):
    model = Member
    template_name = 'core/member_confirm_delete.html'
    context_object_name = 'member'

    def get_queryset(self):
        return Member.objects.filter(club=self.request.club)

    def get_success_url(self):
        return reverse_lazy('member_list', kwargs={'club_slug': self.request.club.subdomain})

    def form_valid(self, form):
        messages.success(self.request, "Socio eliminado con éxito.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.request.club
        return context
