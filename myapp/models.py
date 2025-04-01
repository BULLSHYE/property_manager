from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils import timezone
import datetime

# Landlord Model
class Landlord(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_subscription = models.BooleanField(default= False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'landlord'
        ordering = ['created_at']
        verbose_name = "Landlord"
        verbose_name_plural = "Landlords"

# Property Model
class Property(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='properties')
    address = models.CharField(max_length=255)
    property_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.property_name

    class Meta:
        db_table = 'property'
        ordering = ['created_at']

# Room Model
class Room(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    # person_number = models.IntegerField()
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Room {self.room_number} in {self.property.property_name}"

    class Meta:
        db_table = 'room'
        ordering = ['room_number']


# Tenant Model
class Tenant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    total_person = models.IntegerField(default=1)
    aadhar_photo = models.TextField()
    other_images = models.TextField()
    assigned_room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='tenant')
    move_in_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tenant'
        ordering = ['name']

    # Override the save method to handle is_occupied logic
    def save(self, *args, **kwargs):
        # Check if the tenant is being assigned to a room
        if self.assigned_room:
            # If the tenant is active, set the room to occupied
            if self.is_active:
                self.assigned_room.is_occupied = True
            else:
                # If tenant is not active, set the room to not occupied
                self.assigned_room.is_occupied = False
        
        # Make sure to save the room status change before saving the tenant
        if self.assigned_room:
            self.assigned_room.save()

        super().save(*args, **kwargs)

    # Optional: To ensure that room is marked unoccupied when tenant is deleted
    def delete(self, *args, **kwargs):
        if self.assigned_room:
            self.assigned_room.is_occupied = False
            self.assigned_room.save()
        super().delete(*args, **kwargs)

# Payment Model
class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    is_paid = models.BooleanField(default=True)
    payment_date = models.DateField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return f"Payment for {self.tenant.name} - {self.month}/{self.year}"

    class Meta:
        db_table = 'payment'
        ordering = ['year', 'month']
        constraints = [
            models.UniqueConstraint(fields=['tenant', 'room', 'month', 'year'], name='unique_payment_per_month')
        ]

# Meter Reading Model
class Electricity(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='electrcitys')
    reading_date = models.DateField(default=timezone.now)
    last_reading = models.FloatField()
    current_reading = models.FloatField()
    consumption = models.FloatField(default=None)
    rate = models.FloatField(default=10.1)
    total_amount = models.FloatField(default=None)

    def save(self, *args, **kwargs):
        # Auto-calculate consumption
        if self.last_reading and self.current_reading:
            self.consumption = self.current_reading - self.last_reading
            self.total_amount = self.consumption * self.rate

        # # Auto-update last_reading for the next month
        # if not Electricity.objects.filter(room=self.room, reading_date__month=self.reading_date.month - 1).exists():
        #     self.last_reading = self.current_reading

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reading for {self.room} on {self.reading_date}"

    class Meta:
        db_table = 'electrcity'
        ordering = ['reading_date']


# @receiver(post_save, sender=Tenant)
# def assign_room(sender, instance, **kwargs):
#     if instance.is_active:
#         instance.room.is_occupied = True
#         instance.room.save()

# @receiver(post_delete, sender=Tenant)
# def unassign_room(sender, instance, **kwargs):
#     instance.room.is_occupied = False
#     instance.room.save()