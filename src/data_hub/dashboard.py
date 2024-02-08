"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'data_hub.dashboard.CustomIndexDashboard'
"""

# from django.utils.translation import ugettext_lazy as _
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
            models=('lcd.models.CategoryType',
                    'lcd.models.EpsgType',
                    'lcd.models.FileType',
                    'lcd.models.LicenseType',
                    'lcd.models.ResolutionType',
                    'lcd.models.SourceType',
                    'lcd.models.TemplateType',
                    'lcd.models.UseType'),
        ))

        self.children.append(modules.AppList(
            title='Collection Catalog',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=('lcd.models.Collection','lcd.models.CollectionFootprint'),
        ))

        self.children.append(modules.AppList(
            title='Master of Resources',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=('lcd.models.Resource',
                    'lcd.models.ResourceType',
                    'lcd.models.XlargeSupplemental',
                    'lcd.models.Quote'),
        ))

        self.children.append(modules.AppList(
            title='Historical Aerials',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=('lore.models.Agency',
                    'lore.models.FrameSize',
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
            title='Website Content',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=('tnris_org.models.TnrisImage',
                    'tnris_org.models.TnrisDocument',
                    'tnris_org.models.TnrisTraining',
                    'tnris_org.models.TrainingCategory',
                    'tnris_org.models.TnrisForumTraining',
                    'tnris_org.models.TnrisInstructorType',
                    'tnris_org.models.TnrisGioCalendarEvent'),
        ))

        self.children.append(modules.AppList(
            title='Contact!',
            collapsible=True,
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=(
                    'contact.models.DataHubContact',
                    'contact.models.DataHubOrder',
                    'contact.models.OrderType',
                    'contact.models.DataHubOutsideEntityContact',
                    'contact.models.EducationContact',
                    'contact.models.EmailTemplate',
                    'contact.models.ForumJobBoardSubmission',
                    'contact.models.GeneralContact',
                    'contact.models.GeorodeoCallForPresentationsSubmission',
                    'contact.models.GeorodeoRegistration',
                    'contact.models.LakesOfTexasContact',
                    'contact.models.OrderMap',
                    'contact.models.PosterGallerySubmission',
                    'contact.models.SurveyTemplate',
                    'contact.models.TexasImageryServiceContact',
                    'contact.models.TexasImageryServiceRequest',
                    'contact.models.CampaignSubcriber',
                    'contact.models.Campaign',
                    ),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title='Recent Actions',
            limit=5,
            collapsible=False,
            column=3,
        ))
