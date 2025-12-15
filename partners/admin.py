from django.contrib import admin
from .models import Partner, DonorProfile

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'user', 'website', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('organization_name', 'user__email', 'website')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Organization Info', {
            'fields': ('user', 'organization_name', 'website', 'logo')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_document')
        }),
        ('Description', {
            'fields': ('organization_description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'impact_score', 'total_donations', 'visibility')
    list_filter = ('visibility', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'impact_score')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('user', 'get_email', 'visibility')
        }),
        ('Donation Preferences', {
            'fields': ('preferred_categories',)
        }),
        ('Impact', {
            'fields': ('impact_score', 'total_donations')
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
