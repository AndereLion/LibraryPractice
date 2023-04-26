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
    # fields = [
    #     "status",
    #     "type",
    #     "borrowing_id",
    #     "money_to_pay",
    #     ("session_url", "session_id")
    # ]
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
        if obj:  # obj is not None, so this is an edit
            return ["session_url", "session_id"]
        else:  # obj is None, so this is an add
            return []
