from django.contrib import admin
from reservation_app.models import IHA, Customers, Reservations

class IHAAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'weight', 'category', 'price', 'image_tag')
    search_fields = ('brand', 'model')
    list_filter = ('category',)

    def image_tag(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height:auto;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

class CustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'username')
    search_fields = ('name', 'surname', 'username')
    list_filter = ('name', 'surname')

class ReservationsAdmin(admin.ModelAdmin):
    list_display = ('iha', 'customer', 'start_date', 'finish_date', 'total_price', 'number')
    search_fields = ('iha__model', 'customer__name')
    list_filter = ('start_date', 'finish_date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('iha', 'customer')

admin.site.register(IHA, IHAAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Reservations, ReservationsAdmin)
