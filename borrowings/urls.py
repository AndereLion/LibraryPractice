from django.urls import path

from borrowings.views import BorrowingList, BorrowingDetail

urlpatterns = [
    path("/", BorrowingList.as_view(), name="borrowing-list"),
    path("<int:pk>/", BorrowingDetail.as_view(), name="borrowing-detail"),
]

app_name = "borrowings"
