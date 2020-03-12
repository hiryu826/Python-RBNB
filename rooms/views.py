# from datetime import datetime
from django.shortcuts import render
from . import models


def all_rooms(request):
    all_rooms = models.Room.objects.all()  # room model 전체 object를 가지고 온다.

    return render(request, "rooms/home.html", context={"rooms": all_rooms})

    # now = datetime.now()
    # hungry = True
    # return render(request, "all_rooms.html")  # django에게 all_rooms.html 컴파일을 위한 명령
