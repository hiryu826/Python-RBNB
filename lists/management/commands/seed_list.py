import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


NAME = "lists"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help=f"How many {NAME} you want to"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()  # [4:10] #4 ~ 10번방만 줄 수 있도록 제한할 수 있음
        seeder.add_entity(
            list_models.List,
            number,
            {
                # "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )

        created = seeder.execute()
        cleaned = flatten(list(created.values()))

        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[
                random.randint(0, 5) : random.randint(6, 30)
            ]  # query set 으로 랜덤 리스트와 랜덤 엔드 얻기
            list_model.room.add(*to_add)  # array 안의 요소를 얻을 수 있다.

        # for user in users:
        #     list_model = list_models.List.objects.create(user=user, name="Favs.")
        #     to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
        #     list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
