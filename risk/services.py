from django.forms import ValidationError
from django.contrib.auth.models import User
from django.db.models import Max

from risk.utils import _serialize_risks

from .models import Book, DailyRisk

def get_last_risk_data(pm, date):
    '''
    Fetch risks of the last available date for this pm
    '''

    books = Book.objects.filter(
        pm=pm,
        is_active=True,
        created_at__lte=date
    )
    last_risk_date = (
        DailyRisk.objects.filter(book__in=books, date__lt=date)
        .aggregate(last_date=Max('date'))['last_date']
    )
    if not last_risk_date:
        return {}  # no risk data found

    risks = {
        r.book_id: r
        for r in DailyRisk.objects.filter(book__in=books, date=last_risk_date)
    }
    result = _serialize_risks(books, risks)
    return result

def fetch_risk_data(pm, date):
    books = Book.objects.filter(
        pm=pm,
        is_active=True,
        created_at__lte=date
    )
    risks = {
        r.book_id: r
        for r in DailyRisk.objects.filter(book__in=books, date=date)
    }
    
    result = _serialize_risks(books, risks)
    return result


def validate_entry(entry):
    # Check that required fields exist
    if "book_id" not in entry:
        raise ValidationError("Missing book_id in entry")
    try:
        book = Book.objects.get(id=entry["book_id"])
    except Book.DoesNotExist:
        raise ValidationError(f"Invalid book_id: {entry['book_id']}")

    for field in ["risk", "target", "stop", "worst_case_bp", "worst_case_k"]:
        val = entry.get(field)
        if val is not None :
            try:
                float(val)
            except ValueError:
                raise ValidationError(f"{field} must be a number")
    return book

def save_risk_data(pm, date, entries):
    validated_objects = []
    for e in entries:
        book = validate_entry(e)
        
        validated_objects.append(
            DailyRisk(
                date=date,
                book=book,
                risk=e.get("risk"),
                target=e.get("target"),
                stop=e.get("stop"),
                worst_case_bp=e.get("worst_case_bp"),
                worst_case_k=e.get("worst_case_k"),
                comment=e.get("comment")
            )
        )

    book_ids = [obj.book.id for obj in validated_objects]

    existing_qs = DailyRisk.objects.filter(
        date=date,
        book__pm=pm
    ).delete()
    print(
        f"date={date}, book_ids={book_ids}"
    )
    DailyRisk.objects.bulk_create(validated_objects)
