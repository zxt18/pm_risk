from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date
from risk.models import Book, DailyRisk
import random


def generate_risk_values():
    """Generate realistic risk values for a single book entry."""
    risk = round(random.uniform(4000, 15000), 2)
    target = round(random.uniform(2.0, 8.0), 2)
    stop = round(target * random.uniform(1.3, 1.8), 2)
    worst_case_bp = round(stop * random.uniform(1.3, 2.0), 2)
    worst_case_k = round(risk * (worst_case_bp / 1000), 2)
    
    comments = [
        "Monitoring market volatility",
        "Position sizing adjusted for event risk",
        "Stress test passed; no changes",
        "Tight spreads; minimal tail risk",
        "Exposure increased in defensive names",
        "Hedging active on rates moves"
    ]
    comment = random.choice(comments)
    
    return {
        "risk": Decimal(str(risk)),
        "target": Decimal(str(target)),
        "stop": Decimal(str(stop)),
        "worst_case_bp": Decimal(str(worst_case_bp)),
        "worst_case_k": Decimal(str(worst_case_k)),
        "comment": comment,
    }


class Command(BaseCommand):
    help = "Create dummy Book and DailyRisk records for testing"

    def handle(self, *args, **options):
        Book.objects.all().delete()
        DailyRisk.objects.all().delete()

        # Create users
        user1, _ = User.objects.get_or_create(
            username="WLW_USER1", defaults={'email': 'user1@gmail.com'}
        )
        user2, _ = User.objects.get_or_create(
            username="WLW_USER2", defaults={'email': 'user2@outlook.com'}
        )

        # Define books
        book_defs = {
            "Emerging Mkts": {"user": user1, "created_at": date(2025, 1, 1)},
            "Global Macro": {"user": user1, "created_at": date(2025, 11, 1)},
            "Credit Arb": {"user": user1, "created_at": date(2025, 1, 1)},
            "USD Bonds": {"user": user2, "created_at": date(2025, 1, 1)},
            "JPY Bonds": {"user": user2, "created_at": date(2025, 1, 1)},
            "BTC Book": {"user": user2, "created_at": date(2025, 1, 1)},
        }

        # Create Book instances
        books = {}
        for name, config in book_defs.items():
            book, created = Book.objects.get_or_create(
                name=name,
                pm=config["user"],
                defaults={"created_at": config["created_at"]}
            )
            books[name] = book

        # Generate dates: today, yesterday, 2 days ago
        today = timezone.localdate()
        dates = [ today - timedelta(days=1), today - timedelta(days=2), today - timedelta(days=3)]

        count = 0
        # For each book, create one DailyRisk entry for each date
        for name, book in books.items():
            for selected_date in dates:
                risk_data = generate_risk_values()
                DailyRisk.objects.get_or_create(
                    date=selected_date,
                    book=book,
                    defaults=risk_data
                )
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} dummy DailyRisk records for {len(books)} books across {len(dates)} dates.")
        )