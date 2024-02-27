#views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Booking, Room, CheckOut, FinancialTransaction
from .forms import BookingCheckInForm, BookingCheckOutForm
from django.utils import timezone
from django.db.models import Sum, Prefetch
from django.contrib.auth.decorators import login_required, permission_required


@login_required
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

@login_required
def room_details(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    booking = room.current_booking
    checkout_form = BookingCheckOutForm()  # Crie uma instância do formulário de checkout
    return render(request, 'room_details.html', {'booking': booking, 'form': checkout_form})

@login_required
def checkout(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    booking = room.current_booking

    if request.method == 'POST':
        form = BookingCheckOutForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.booking = booking
            checkout.save()

            # Criar descrição incluindo nome completo e CPF do hóspede
            description = (f"Checkout para {booking.full_name} (CPF: {booking.cpf}), "
                           f"Quarto: {room.room_number}, Total pago: R$ {checkout.total_paid}")

            # Criar uma nova transação financeira
            FinancialTransaction.objects.create(
                transaction_type='check_out',
                description=description,
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

@login_required
def dashboard(request):
    rooms = Room.objects.all()
    form = BookingCheckInForm()
    return render(request, 'dashboard.html', {'rooms':rooms,'form':form})

@login_required(login_url='/login/')
@permission_required('guest_management.can_view',raise_exception=True)
def financial_report(request):
    transactions = FinancialTransaction.objects.all()
    total_amount = 0
    search_performed = False  # Adicione esta linha

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')

        if date_from and date_to:
            transactions = transactions.filter(date__range=[date_from, date_to])
            total_amount = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
            search_performed = True  # Atualize esta variável quando a busca for realizada

    return render(request, 'financial_report.html', {
        'transactions': transactions,
        'total_amount': total_amount,
        'search_performed': search_performed  # Passe esta variável para o template
    })

@login_required
def all_stays(request):
    # Obtenha todas as informações de Booking e CheckOut
    bookings = Booking.objects.all()
    checkouts = CheckOut.objects.all()

    # Combine informações de Booking e CheckOut
    stays = []
    for booking in bookings:
        checkout = checkouts.filter(booking=booking).first()
        stays.append({
            'booking': booking,
            'checkout': checkout
        })

    return render(request, 'all_stays.html', {'stays': stays})

@login_required
def stay_details(request, booking_id):
    # Obtenha informações detalhadas de Booking e CheckOut
    booking = Booking.objects.get(id=booking_id)
    checkout = CheckOut.objects.filter(booking=booking).first()

    return render(request, 'stay_details.html', {
        'booking': booking,
        'checkout': checkout
    })

