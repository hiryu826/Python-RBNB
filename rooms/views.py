# from datetime import datetime
# from math import ceil
# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage
# from django.utils import timezone
# from django.urls import reverse
# from django.http import Http404
from django.views.generic import ListView, DetailView
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 0
    ordering = "created"
    context_object_name = "rooms"
    # page_kwarg = "pg" //page 파라미터명 변경


class RoomDetail(DetailView):

    model = models.Room


# -----------------------------------
# view 생성
# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         raise Http404()
# return redirect(reverse("core:home"))

# -----------------------------------
# # context date 생성을 이용한 datetime 출력
# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     now = timezone.now()
#     context["now"] = now

#     return context


# def all_rooms(request):

# -----------------------------------
# # [Paginator를 이용한 코드 작성 방법]
# page = request.GET.get("page", 1)

# room_list = models.Room.objects.all()
# paginator = Paginator(room_list, 10, orphans=0)

# try:
#     rooms = paginator.page(int(page))
#     return render(request, "rooms/home.html", {"page": rooms})
#     # rooms = paginator.get_page(page)
#     # print(vars(rooms.paginator))
# except EmptyPage:
#     return redirect("/")

# -----------------------------------
# [페이지네이션 수동 작성 코드]
# #페이지네이션 수동 작성을 위한 Page의 기본 값 선언
# page = request.GET.get("page", 1)
# page = int(page or 1)
# page_size = 10
# limit = page_size * page
# offset = limit - page_size

# #model Object 호출
# all_rooms = models.Room.objects.all()[offset:limit]  # room model 전체 object를 가지고 온다.
# page_count = ceil(models.Room.objects.count() / page_size)

# #페이지네이션 수동 작성 코드
# return render(
#     request,
#     "rooms/home.html",
#     context={
#         "rooms": all_rooms,
#         "page": page,
#         "page_count": page_count,
#         "page_range": range(1, page_count),
#     },
# )
# now = datetime.now()
# hungry = True
# return render(request, "all_rooms.html")  # django에게 all_rooms.html 컴파일을 위한 명령

