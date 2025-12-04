from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, BookPermission, DailyRisk, User

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'pm', 'created_at', 'is_active')
    list_filter = ('pm', 'is_active', 'created_at')
    search_fields = ('name', 'pm__username')
    ordering = ('pm', 'name')
    list_editable = ('is_active',)  # optional: allows inline editing

@admin.register(DailyRisk)
class DailyRiskAdmin(admin.ModelAdmin):
    list_display = ( 'date','pm_name','book_name', 'risk', 'target', 'stop','worst_case_bp','worst_case_k')
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

@admin.register(BookPermission)
class BookPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'pm', 'permission')
    list_filter = ('permission', 'pm', 'user')
    search_fields = ('user__username', 'pm__username')
    autocomplete_fields = ('user', 'pm')


class BookPermissionInline(admin.TabularInline):
    model = BookPermission
    extra = 0
    autocomplete_fields = ('pm',)
    fk_name = "user"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'is_staff', 'pm_permissions')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        
        ('PM Permissions', {
            'fields': ('can_edit_all_pms','can_view_all_pms'),
        }),
    )

    inlines = [BookPermissionInline]

    def pm_permissions(self, obj):
        if obj.can_edit_all_pms:
            return "EDIT ALL"

        perms = list(
            BookPermission.objects
            .filter(user=obj)
            .select_related("pm")
        )

        if not perms and not obj.can_view_all_pms:
            return "—"

        if obj.can_view_all_pms:
            class _FakePerm:
                pm = type("P", (), {"username": ""})()
                permission = "VIEW ALL"
            perms.append(_FakePerm())

        if perms:
            return ", ".join(
                f"{p.pm.username} ({p.permission})"
                for p in perms
            )

        return ""

    pm_permissions.short_description = "PM Permissions"