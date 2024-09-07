# from django.core.management.base import BaseCommand
# from chatbot.models import UserSession,Car

# class Command(BaseCommand):
#     help = 'Import car models into the database'

#     def handle(self, *args, **kwargs):
#         car_models = [
#             'Ford F-150 Lightning', 'Chevrolet Silverado EV', 'Toyota GR Corolla', 'Hyundai Ioniq 6', 'Kia EV9', 'Honda Civic Type R', 'Nissan Z', 'Cadillac Lyriq', 'Lucid Air Pure', 'Genesis GV70 EV',
#             'BMW i7', 'Mercedes-Benz EQS SUV', 'Porsche 911 Dakar', 'Jeep Grand Wagoneer L',
#             'Tesla Cybertruck', 'Chevrolet Corvette E-Ray', 'Ford Mustang (2024 Model)', 'Polestar 3', 'Hyundai Ioniq 7', 'BMW XM', 'Acura ZDX', 'Ram 1500 REV', 'Toyota Land Cruiser', 'Audi Q8 e-tron',
#             'Maserati GranTurismo Folgore', 'Subaru Crosstrek Wilderness', 'GMC Sierra EV', 'Lotus Eletre'
#         ]

#         for model_name in car_models:
#             car_model, created = CarModel.objects.get_or_create(name=model_name)
#             if created:
#                 self.stdout.write(self.style.SUCCESS(f'Model "{model_name}" created'))
#             else:
#                 self.stdout.write(self.style.WARNING(f'Model "{model_name}" already exists'))


from django.core.management.base import BaseCommand
from chatbot.models import UserSession,Car

class Command(BaseCommand):
    help = 'Load car data into the database'

    def handle(self, *args, **kwargs):
        car_data = [
            {
                "make": "Ford", 
                "year": 2025, 
                "model": "Escape", 
                "trim": "Active, PHEV, ST-Line, ST-Line Select, ST-Line Elite and Platinum", 
                "colours": "Space Silver Metallic, Rapid Red, Vapor Blue Metallic, Agate Black, Star White Metallic, Carbonized Gray"
            },
            {
                "make": "Toyota",
                "year": 2024,
                "model": "Camry",
                "trim": "LE, SE, XLE, XSE, TRD",
                "colours": "Super White, Predawn Gray Mica, Celestial Silver Metallic, Midnight Black Metallic, Blueprint"
            },
            {
                "make": "Honda",
                "year": 2023,
                "model": "Civic",
                "trim": "LX, Sport, EX, Touring",
                "colours": "Aegean Blue Metallic, Rallye Red, Lunar Silver Metallic, Crystal Black Pearl, Platinum White Pearl"
            },
            {
                "make": "Chevrolet",
                "year": 2025,
                "model": "Tahoe",
                "trim": "LS, LT, RST, Z71, Premier, High Country",
                "colours": "Black, Summit White, Empire Beige Metallic, Cherry Red Tintcoat, Dark Ash Metallic"
            },
            {
                "make": "BMW",
                "year": 2024,
                "model": "X5",
                "trim": "sDrive40i, xDrive40i, xDrive50e, M50i, M",
                "colours": "Alpine White, Jet Black, Phytonic Blue Metallic, Manhattan Green Metallic, Mineral White Metallic"
            },
            {
                "make": "Tesla",
                "year": 2025,
                "model": "Model S",
                "trim": "Long Range, Plaid",
                "colours": "Pearl White Multi-Coat, Solid Black, Midnight Silver Metallic, Deep Blue Metallic, Red Multi-Coat"
            },
            {
                "make": "Nissan",
                "year": 2024,
                "model": "Altima",
                "trim": "S, SV, SR, SL, Platinum",
                "colours": "Scarlet Ember Tintcoat, Gun Metallic, Pearl White Tricoat, Super Black, Brilliant Silver Metallic"
            },
            {
                "make": "Mercedes-Benz",
                "year": 2024,
                "model": "C-Class",
                "trim": "C 300, C 300 4MATIC, AMG C 43, AMG C 63 S",
                "colours": "Polar White, Obsidian Black Metallic, Mojave Silver Metallic, Selenite Grey Metallic, Lunar Blue Metallic"
            },
            {
                "make": "Audi",
                "year": 2023,
                "model": "A6",
                "trim": "Premium, Premium Plus, Prestige, S6, RS 6 Avant",
                "colours": "Ibis White, Mythos Black Metallic, Navarra Blue Metallic, Daytona Gray Pearl, Tango Red Metallic"
            },
            {
                "make": "Hyundai",
                "year": 2024,
                "model": "Tucson",
                "trim": "SE, SEL, N Line, XRT, Limited",
                "colours": "Phantom Black, Shimmering Silver, Calypso Red, Deep Sea, Amazon Gray"
            },
        ]

        for data in car_data:
            make = data['make']
            year = data['year']
            model = data['model']
            trims = data['trim'].split(', ')
            colours = data['colours'].split(', ')

            for trim in trims:
                for colour in colours:
                    car_record, created = Car.objects.get_or_create(
                        make=make,
                        year=year,
                        model=model,
                        trim=trim,
                        color=colour
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added {car_record}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'{car_record} already exists'))
