import csv
from django.core.management.base import BaseCommand
from transcript_app.models import GraduateAttribute, CharacterStrength, AttributeStrengthMap

class Command(BaseCommand):
    help = 'Load Attribute-Strength mappings from CSV'

    def handle(self, *args, **kwargs):
        path = 'transcript_app/mapping.csv'

        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                attribute_name = row['Column 1'].strip()
                attribute, _ = GraduateAttribute.objects.get_or_create(name=attribute_name)

                for strength_name, value in row.items():
                    if strength_name == 'Column 1':
                        continue
                    if value and value.strip().isdigit() and int(value) > 0:
                        strength, _ = CharacterStrength.objects.get_or_create(name=strength_name.strip())
                        AttributeStrengthMap.objects.update_or_create(
                            graduate_attribute=attribute,
                            character_strength=strength,
                            defaults={'weight': float(value)}  # ✅ match your model field
                        )



        self.stdout.write(self.style.SUCCESS('Mappings loaded successfully!'))
