import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from listings.models import Listing
from realtors.models import Realtor


class Command(BaseCommand):
    help = 'Create repeatable demo realtors and property listings.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of listings to create (default: 100).',
        )

    def handle(self, *args, **options):
        count = options['count']
        if count < 1:
            self.stderr.write('The listing count must be at least 1.')
            return

        image_names = ('building.jpg', 'about.jpg', 'showcase.jpg')
        media_image_names = []
        media_image_dir = Path(settings.MEDIA_ROOT) / 'photos'
        media_image_dir.mkdir(parents=True, exist_ok=True)
        for image_name in image_names:
            source_image = (
                Path(settings.BASE_DIR)
                / 'djangofirst'
                / 'static'
                / 'img'
                / image_name
            )
            media_image = media_image_dir / f'demo-{image_name}'
            if source_image.exists() and not media_image.exists():
                shutil.copyfile(source_image, media_image)
            if media_image.exists():
                media_image_names.append(f'photos/demo-{image_name}')

        if not media_image_names:
            self.stderr.write('No demo property images were found.')
            return

        realtors = []
        for index in range(1, min(10, count) + 1):
            realtor, _ = Realtor.objects.get_or_create(
                email=f'demo.realtor{index}@example.com',
                defaults={
                    'name': f'Demo Realtor {index}',
                    'photo': media_image_names[0],
                    'description': 'Certified real estate specialist with extensive regional expertise.',
                    'phone': f'+91-90000000{index:02d}',
                    'is_mvp': index <= 3,
                },
            )
            if not realtor.photo:
                realtor.photo = media_image_names[0]
                realtor.save(update_fields=['photo'])
            realtors.append(realtor)

        created = 0
        cities = ['Mumbai', 'Pune', 'Thane', 'Nashik']
        types = ['1 BHK Apartment', '2 BHK Modern Home', '3 BHK Luxury Flat', '4 BHK Penthouse', '5 BHK Luxury Villa']

        for index in range(1, count + 1):
            city_name = cities[index % len(cities)]
            # Distribute bedrooms cleanly from 1 to 5 so every bedroom filter works
            bedroom_count = 1 + (index % 5)
            prop_type = types[(bedroom_count - 1) % len(types)]
            garage_count = index % 3

            amenities = []
            if index % 2 == 0:
                amenities.append('private swimming pool')
            if garage_count > 0:
                amenities.append(f'{garage_count}-car covered garage')
            if index % 3 == 0:
                amenities.append('spacious sunlit balcony')
            if index % 4 == 0:
                amenities.append('landscaped private garden')
            if index % 5 == 0:
                amenities.append('rooftop terrace with panoramic skyline views')

            amenities_text = ', '.join(amenities) if amenities else 'open modular kitchen, premium fixtures'
            desc = (
                f'{prop_type} located in a prime neighborhood of {city_name}. '
                f'Features include {amenities_text}, premium architectural finishes, '
                f'and immediate access to local transit and shopping.'
            )

            listing, was_created = Listing.objects.get_or_create(
                title=f'Demo Property {index:03d}',
                defaults={
                    'realtor': realtors[(index - 1) % len(realtors)],
                    'address': f'{index} Demo Avenue',
                    'city': city_name,
                    'state': 'Maharashtra',
                    'zipcode': f'{400000 + index}',
                    'description': desc,
                    'price': 5000000 + (index * 125000),
                    'bedrooms': bedroom_count,
                    'bathrooms': 1.0 + (bedroom_count - 1) * 0.5,
                    'garage': garage_count,
                    'sqft': 550 + (bedroom_count * 250) + (index * 15),
                    'lot_size': 800 + (bedroom_count * 300) + (index * 10),
                    'photo_main': media_image_names[(index - 1) % len(media_image_names)],
                    'is_Published': True,
                },
            )
            if not was_created:
                listing.description = desc
                listing.bedrooms = bedroom_count
                listing.bathrooms = 1.0 + (bedroom_count - 1) * 0.5
                listing.sqft = 550 + (bedroom_count * 250) + (index * 15)
                listing.photo_main = media_image_names[
                    (index - 1) % len(media_image_names)
                ]
                listing.is_Published = True
                listing.save(update_fields=['description', 'bedrooms', 'bathrooms', 'sqft', 'photo_main', 'is_Published'])
            created += int(was_created)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded {count} demo listings ({created} newly created).'
            )
        )
