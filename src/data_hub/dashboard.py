"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'data_hub.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.AppList(
            title='Administration',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=('django.contrib.*',),
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            title='Collection Domains',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            exclude=('django.contrib.*',
                     'lcd.models.Collection',
                     'lcd.models.ResourceType',
                     'lcd.models.Resource',
                     'lore.models.Agency',
                     'lore.models.FrameSize',
                     'lore.models.Scale',
                     'lore.models.County',
                     'lore.models.Collection',
                     'msd.models.MapCollection',
                     'msd.models.MapDownload',
                     'msd.models.MapSize',
                     'msd.models.PixelsPerInch',
                     'tnris_org.models.TnrisImageUrl',
                     'tnris_org.models.TnrisDocUrl'),
        ))

        self.children.append(modules.AppList(
            title='Collection Catalog',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=('lcd.models.Collection',),
        ))

        self.children.append(modules.AppList(
            title='Master of Resources',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=('lcd.models.Resource','lcd.models.ResourceType'),
        ))

        self.children.append(modules.AppList(
            title='Historical Aerials',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=('lore.models.Agency',
                    'lore.models.FrameSize',
                    'lore.models.Scale',
                    'lore.models.County',
                    'lore.models.Collection'),
        ))

        self.children.append(modules.AppList(
            title='Map Collections/Series',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=('msd.models.MapCollection',
                    'msd.models.MapDownload',
                    'msd.models.MapSize',
                    'msd.models.PixelsPerInch'),
        ))

        self.children.append(modules.AppList(
            title='TNRIS.org',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=('tnris_org.models.TnrisImageUrl',
                    'tnris_org.models.TnrisDocUrl'),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title='Recent Actions',
            limit=5,
            collapsible=False,
            column=3,
        ))
