from django.contrib import admin
from .models import Book, DailyRisk

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'pm', 'created_at', 'is_active')
    list_filter = ('pm', 'is_active', 'created_at')
    search_fields = ('name', 'pm__username')
    ordering = ('pm', 'name')
    list_editable = ('is_active',)  # optional: allows inline editing

@admin.register(DailyRisk)
class DailyRiskAdmin(admin.ModelAdmin):
    list_display = ( 'date','pm_name','book_name', 'risk', 'target', 'stop')
    list_filter = ('date', 'book__pm', 'book__name')
    search_fields = ('book__name', 'book__pm__username', 'comment')
    date_hierarchy = 'date'
    ordering = ('-date', 'book__name')
    autocomplete_fields = ('book',)

    # Custom display methods
    def book_name(self, obj):
        return obj.book.name
    book_name.admin_order_field = 'book__name'
    book_name.short_description = 'Book' 

    def pm_name(self, obj):
        return obj.book.pm.username
    pm_name.admin_order_field = 'book__pm__username'
    pm_name.short_description = 'PM'