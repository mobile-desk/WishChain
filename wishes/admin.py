from django.contrib import admin
from .models import WisherProfile

@admin.register(WisherProfile)
class WisherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'household_size', 'income_bracket', 'is_verified')
    list_filter = ('income_bracket', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'get_email', 'household_size', 'income_bracket')
        }),
        ('Verification', {
            'fields': ('verified_by', 'id_document', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'
    
    def is_verified(self, obj):
        return obj.verified_by is not None
    is_verified.boolean = True
    is_verified.short_description = 'Verified'
