# from datetime import datetime
# from math import ceil
# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage
# from django.utils import timezone
# from django.urls import reverse
# from django.http import Http404
from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from django_countries import countries
from . import models, forms


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 12
    paginate_orphans = 0
    ordering = "created"
    context_object_name = "rooms"
    # page_kwarg = "pg" //page 파라미터명 변경


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


# Django Form API로 구현한 search view
class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        country = request.GET.get("country")

        # form 내 데이터가 있을 경우
        if country:

            # GET으로 받은 모든 Data를 form에게 전달해준다.
            form = forms.SearchForm(request.GET)

            # form은 valid 하여야 계속 진행 된다.
            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                # 필터 조건 작성
                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    # roomtype foreignkey를 이용한 filter
                    # filter_args["room_type__pk__exact"] = room_type
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = {
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    }

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        # print(room.host.pk, self.request.user.pk)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    # print(f"Should delete {photo_pk} from {room_pk}")
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Cant delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Success Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Update"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        print(room_pk)
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):
    model = models.Photo
    template_name = "rooms/photo_create.html"
    fields = (
        "caption",
        "file",
    )
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Success Photo Upload")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


# -----------------------------------
# # Python으로 구현한 search view(function based)
# def search(request):
#     print(request.GET)
#     city = request.GET.get("city", "Anywhere")
#     city = str.capitalize(city)
#     country = request.GET.get("country", "KR")
#     room_type = int(request.GET.get("room_type", 0))
#     price = int(request.GET.get("price", 0))
#     guests = int(request.GET.get("guests", 0))
#     bedrooms = int(request.GET.get("bedrooms", 0))
#     beds = int(request.GET.get("beds", 0))
#     baths = int(request.GET.get("baths", 0))
#     instant = bool(request.GET.get("instant", False))
#     superhost = bool(request.GET.get("superhost", False))
#     s_amenities = request.GET.getlist("amenities")
#     s_facilities = request.GET.getlist("facilities")

#     form = {
#         "city": city,
#         "s_room_type": room_type,
#         "s_country": country,
#         "price": price,
#         "guests": guests,
#         "bedrooms": bedrooms,
#         "beds": beds,
#         "baths": baths,
#         "s_amenities": s_amenities,
#         "s_facilities": s_facilities,
#         "instant": instant,
#         "superhost": superhost,
#     }

#     room_types = models.RoomType.objects.all()
#     amenities = models.Amenity.objects.all()
#     facilities = models.Facility.objects.all()

#     choices = {
#         "countries": countries,
#         "room_types": room_types,
#         "amenities": amenities,
#         "facilities": facilities,
#     }

#     # 필터 조건 작성
#     filter_args = {}
#     if city != "Anywhere":
#         filter_args["city__startswith"] = city

#     filter_args["country"] = country

#     if room_type != 0:
#         # roomtype foreignkey를 이용한 filter
#         # filter_args["room_type__pk__exact"] = room_type
#         filter_args["room_type__pk"] = room_type

#     # 가격 필터링
#     if price != 0:
#         filter_args["price__lte"] = price

#     # 손님 수 필터링
#     if guests != 0:
#         filter_args["guests__gte"] = guests

#     # 방 수 필터링
#     if beds != 0:
#         filter_args["beds__gte"] = beds

#     # 화장실 필터링
#     if baths != 0:
#         filter_args["baths__gte"] = baths

#     if instant is True:
#         filter_args["instant_book"] = True

#     # Foreignkey를 이용한 필터(rooms의 host, users의 superhost)
#     if superhost is True:
#         filter_args["host__superhost"] = True

#     # amenity 필터 생성
#     if len(s_amenities) > 0:
#         print(len(s_amenities))
#         for s_amenity in s_amenities:
#             filter_args["amenities__pk"] = int(s_amenity)

#     # facility 필터 생성
#     if len(s_facilities) > 0:
#         print(len(s_facilities))
#         for s_facility in s_facilities:
#             filter_args["facilities__pk"] = int(s_facility)

#     # 필터 생성bool()
#     rooms = models.Room.objects.filter(**filter_args)

#     return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})

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
# return render(request, "all_rooms.html") # django에게 all_rooms.html 컴파일을 위한 명령
