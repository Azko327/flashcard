import random
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from .forms import CardCheckForm
from .models import Card, BOXES
from django.views.generic import DeleteView


class CardListView(ListView):
    model = Card
    queryset = Card.objects.all()

class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer", "box"]
    success_url = reverse_lazy("card-list")

    def form_valid(self, form):
        messages.success(self.request, "Card created successfully.")
        return super().form_valid(form)

class CardUpdateView(UpdateView):
    model = Card
    fields = ["question", "answer", "box"]
    success_url = reverse_lazy("card-list")

    def form_valid(self, form):
        messages.success(self.request, "Card updated successfully.")
        return super().form_valid(form)

class BoxView(CardListView):
    template_name = "cards/box.html"
    form_class = CardCheckForm

    def get_queryset(self):
        return Card.objects.filter(box=self.kwargs["box_num"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["box_number"] = self.kwargs["box_num"]
        if self.object_list:
            context["check_card"] = random.choice(self.object_list)
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])
            card.move(form.cleaned_data["solved"])

        return redirect(request.META.get("HTTP_REFERER"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_cards = Card.objects.count()
        highest_box = max(BOXES)
        learned_cards = Card.objects.filter(box=highest_box).count()
        context['learned_percent'] = (learned_cards / total_cards * 100) if total_cards else 0
        context["box_number"] = self.kwargs["box_num"]
        if self.object_list:
            context["check_card"] = random.choice(self.object_list)
        return context


def my_view(request):
    messages.success(request, 'Success message here!')
    return redirect('redirect_view_name')
class CardDeleteView(DeleteView):
    model = Card
    success_url = reverse_lazy('card-list')
