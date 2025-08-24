"""Permissions used for different dashboard views."""

from django.contrib.auth import get_user_model

User = get_user_model()


class DashboardPermission:
    """Permissions used for different dashboard views."""

    # Only custom overrides. No standard permissions needed here.
    permissions = {}

    # Minimal set of common dashboard permissions
    # This is just for has_dashboard_perms()
    _common_dashboard_permissions = {
        "catalogue.view_product",
        "partner.view_partner",
        "order.view_order",
        "offer.view_conditionaloffer",
        f"{User._meta.app_label}.view_user",
        "reviews.view_productreview",
        "voucher.view_voucher",
    }

    staff = ["is_staff"]
    # Partner Access
    partner_dashboard_access = ["partner.dashboard_access"]

    @classmethod
    def get(cls, app_label, *codenames):
        """
        Get permissions for given app_label and codenames.
        Supports both explicit mappings and auto-generated permissions.
        """
        permissions = set()

        for codename in codenames:
            key = codename
            if key in cls.permissions:
                permissions.update(cls.permissions[key])
            else:
                permissions.add(f"{app_label}.{codename}")

        return list(permissions)

    @classmethod
    def get_all_permissions(cls):
        """
        Retrieve set of common dashboard permissions for permission checking.
        This is a minimal set used by has_dashboard_perms() to detect dashboard access.
        """
        all_permissions = set(cls._common_dashboard_permissions)

        for permissions in cls.permissions.values():
            all_permissions.update(permissions)

        return all_permissions

    @classmethod
    def has_dashboard_perms(cls, user):
        """
        Check if user has any of the dashboard permissions.
        """
        return len(cls.get_all_permissions() & user.get_all_permissions()) > 0
