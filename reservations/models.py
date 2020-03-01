from django.db import models
from core import models as core_models


class Reservation(core_models.TimeStampedModel):

    """Reservatin Model Definition """

    STATUS_PENDING = "pending"  # 보류
    STATUS_CONFIRMED = "confirmed"  # 확인
    STATUS_CANCELED = "canceled"  # 취소

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.room} - {self.check_in}"

