#views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Booking, Room, CheckOut, FinancialTransaction
from .forms import BookingCheckInForm, BookingCheckOutForm
from django.utils import timezone
from django.db.models import Sum, Prefetch


def create_booking(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)

    if request.method == 'POST':
        form = BookingCheckInForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room  # Relacione o booking ao quarto
            booking.save()

            room.is_occupied = True
            room.current_booking = booking
            room.save()

            return redirect('dashboard')
    else:
        form = BookingCheckInForm(initial={'room_number': room_number})  # Pré-preenche o número do quarto

    return render(request, 'dashboard.html', {'form':form})


def room_details(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    booking = room.current_booking
    checkout_form = BookingCheckOutForm()  # Crie uma instância do formulário de checkout
    return render(request, 'room_details.html', {'booking': booking, 'form': checkout_form})


def checkout(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    booking = room.current_booking

    if request.method == 'POST':
        form = BookingCheckOutForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.booking = booking
            checkout.save()

            # Criar uma nova transação financeira
            FinancialTransaction.objects.create(
                transaction_type='check_out',
                description=f"Checkout para o quarto {room.room_number}",
                amount=checkout.total_paid,
                date=timezone.now()
            )


            # Atualizar o status do quarto
            room.is_occupied = False
            room.current_booking = None
            room.save()

        return redirect('dashboard')
    else:
        form = BookingCheckOutForm()

    return redirect(request, 'dashboard.html', {'form': form, 'room': room})

def dashboard(request):
    rooms = Room.objects.all()
    form = BookingCheckInForm()
    return render(request, 'dashboard.html', {'rooms':rooms,'form':form})



def financial_report(request):
    # Use Prefetch para obter informações relacionadas de Booking através de CheckOut
    checkouts_prefetch = Prefetch('check_out_info', queryset=CheckOut.objects.select_related('booking'))
    transactions = FinancialTransaction.objects.prefetch_related(checkouts_prefetch).all()
    total_amount = 0

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')

        if date_from and date_to:
            transactions = transactions.filter(date__range=[date_from, date_to])
            total_amount = transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'financial_report.html', {
        'transactions': transactions,
        'total_amount': total_amount
    })