import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models

# from . import managers


class BookedDay(core_models.TimeStampedModel):
    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)


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
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    # objects = managers.CustomReservationManager() # reservations.managers.py 를 core로 옮겼으므로 필요 하지 않음

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):  # 현재 날짜가 check_in 날짜보다 큰지 적은지 체크
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:  # None일 경우 새로운 Model
            start = self.check_in  # Start date 흭득
            end = self.check_out  # End date 흭득
            difference = end - start  # start와 end 사이의 BookedDay 탐색
            existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end)  # range로 BookedDay 확인 filter 수행
            ).exists()  # exists로 존재여부 확인 없을 경우 reservation 저장
            if not existing_booked_day:
                super().save(*args, **kwargs)  # reservation save
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)  # BookedDay 생성
                return
        return super().save(*args, **kwargs)
