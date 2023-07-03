from django.contrib import admin

from borrowings.models import Borrowing


class BorrowingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "book", "actual_return_date"]
    list_display_links = ["id"]
    readonly_fields = ["id"]


admin.site.register(Borrowing, BorrowingAdmin)
