from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from risk.models import DailyRisk
from datetime import date

class Command(BaseCommand):
    help = "Create dummy DailyRisk records for testing"
    
    def handle(self, *args, **options):
        username = 'WLW_ZACK'
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={'email': 'zt@gmail.com'}
        )
        
        dummy_data = [
            {
                "book": "Emerging Mkts",
                "risk": 12500.00,
                "target": 8.00,
                "stop": 12.00,
                "worst_case_bp": 15.00,
                "worst_case_k": 1875.00,
                "comment": "High vol in EM FX"
            },
            {
                "book": "Global Macro",
                "risk": 8200.00,
                "target": 5.00,
                "stop": 7.00,
                "worst_case_bp": 10.00,
                "worst_case_k": 820.00,
                "comment": "Rates volatility elevated; long USD duration"
            },
            {
                "book": "Credit Arb",
                "risk": 5000.00,
                "target": 3.00,
                "stop": 5.00,
                "worst_case_bp": 6.00,
                "worst_case_k": 300.00,
                "comment": "Tight spreads; minimal stress expected"
            }
        ]
        count = 0 
        for data in dummy_data : 
            obj, created = DailyRisk.objects.get_or_create(
                pm=user,
                date=date.today(),
                book=data['book'],
                defaults=data
            )
            if created : 
                count +=1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} dummy risk records')
        )
            
            
        
        