from django.contrib import admin

from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "status",
        "type",
        "borrowing_id",
        "money_to_pay"
    ]
    fieldsets = (
        ("Payment Information", {
            "fields": ("status", "type", "borrowing_id", "money_to_pay")
        }),
        ("Session Information", {
            "fields": ("session_url", "session_id"),
            "classes": ("collapse",),
            "description": "These fields are optional"
        })
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["session_url", "session_id"]
        else:
            return []
