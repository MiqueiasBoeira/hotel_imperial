#models.py

from django.db import models
from django.utils import timezone


class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True, verbose_name="Número do Quarto")
    is_occupied = models.BooleanField(default=False, verbose_name="Está Ocupado?")
    current_booking = models.OneToOneField(
        'Booking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='room_booking',  # Adicione um related_name personalizado
        verbose_name="Reserva Atual"
    )

    def __str__(self):
        status = "Ocupado" if self.is_occupied else "Disponível"
        return f"Quarto {self.room_number} - {status}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True,
                      related_name='bookings')  # Adicione related_name
    full_name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    travel_reason = models.CharField(max_length=100)
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2)
    number_of_days = models.IntegerField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    companions = models.TextField(blank=True)

    def __str__(self):
        room_number = self.room.room_number if self.room else 'Sem quarto'
        return f"{self.full_name} - Quarto {room_number}"


class CheckOut(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='check_out_info')
    room_consumption = models.TextField()
    observations = models.TextField(blank=True)
    payment_method = models.CharField(max_length=50)
    total_paid = models.DecimalField(max_digits=8, decimal_places=2)
    #closing_date = models.DateTimeField()


    def __str__(self):
        return f"Check-out para {self.booking.full_name} - Quarto {self.booking.room.room_number if self.booking.room else 'Sem quarto'}"


class FinancialTransaction(models.Model):
    TRANSACTION_CHOICES = [
        ('check_out', 'Check-Out'),
        ('other', 'Outro Lançamento Financeiro'),
    ]

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_transaction_type_display()}: {self.description} - R$ {self.amount}"
