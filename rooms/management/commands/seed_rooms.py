import random
from django.core.management import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This is command creates rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many rooms you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "guests": lambda x: random.randint(1, 20),
                "price": lambda x: random.randint(1, 300),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))

        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()

        for pk in created_clean:  # 생성 된 모든 room
            room = room_models.Room.objects.get(pk=pk)  # primary key로 해당 room을 찾기
            for i in range(
                3, random.randint(10, 17)
            ):  # 루프를 돌며 3부터 최소 10에서 최대 17까지 사진을 만든다.
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,  # foreign key 를 만든다. 변수 이름이 같으면 안된다.
                    file=f"/room_photos/{random.randint(1, 6)}.webp",  # 파일을 준다.
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                # magic_number가 짝수일 경우 amenity를 추가한다. / ManyToMany 필드에서 무엇인가를 추가할 때 사용하는 방식
                if magic_number % 2 == 0:
                    # 다대다 관계를 유지하기 위해 .add 사용 amenity를 가져와 room에 추가한다.
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
