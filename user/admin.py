from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile, Mobile, RefId

class CustomUserChange(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "ref_id")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    form = CustomUserChange

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Mobile)
admin.site.register(RefId)