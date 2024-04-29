from django.db import models

# Create your models here.
class DownloadLog2021(models.Model):
    class Meta:
        managed: False
        db_table = "download_log_2021"
        verbose_name = 'Download log 2021 entry'
        verbose_name_plural = 'Download logs 2021'   

    id = models.UUIDField(
        'ID',
        primary_key=True
    )

    date = models.DateField(
        "Date"
    )

    time = models.TimeField(
        "Time without timezone"
    )

    x_edge_result_type = models.CharField(
        "X Edge Result Type"
    )

    x_edge_detailed_result_type = models.TextField(
        "X Edge Detailed Result Type"
    )

    x_host_header = models.CharField(
        "X Host Header"
    )

    cs_uri_stem = models.TextField(
        "CS URI Stem"
    )

    collection_id = models.CharField(
        "Collection ID"
    )

    collection_shortname = models.CharField(
        "Collection Short Name"
    )

    area_type_id = models.CharField(
        "Area Type ID"
    )

    file_type = models.CharField(
        "File Type"
    )

    hist_band = models.CharField(
        "Hist Band"
    )

    hist_collective = models.CharField(
        "Hist Collective"
    )

    hist_mission = models.CharField(
        "Hist Mission"
    )

    hist_type = models.CharField(
        "Hist Type"
    )

    hist_product = models.CharField(
        "Hist Product"
    )

    hist_file = models.CharField(
        "Hist File"
    )

    def __str__(self):
        return str(self.id)
    
    def getYear():
        return 2021
    
class DownloadLog2022(models.Model):
    class Meta:
        managed: False
        db_table = "download_log_2022"
        verbose_name = 'Download log 2022 entry'
        verbose_name_plural = 'Download logs 2022'   

    id = models.UUIDField(
        'ID',
        primary_key=True
    )

    date = models.DateField(
        "Date"
    )

    time = models.TimeField(
        "Time without timezone"
    )

    x_edge_result_type = models.CharField(
        "X Edge Result Type"
    )

    x_edge_detailed_result_type = models.TextField(
        "X Edge Detailed Result Type"
    )

    x_host_header = models.CharField(
        "X Host Header"
    )

    cs_uri_stem = models.TextField(
        "CS URI Stem"
    )

    collection_id = models.CharField(
        "Collection ID"
    )

    collection_shortname = models.CharField(
        "Collection Short Name"
    )

    area_type_id = models.CharField(
        "Area Type ID"
    )

    file_type = models.CharField(
        "File Type"
    )

    hist_band = models.CharField(
        "Hist Band"
    )

    hist_collective = models.CharField(
        "Hist Collective"
    )

    hist_mission = models.CharField(
        "Hist Mission"
    )

    hist_type = models.CharField(
        "Hist Type"
    )

    hist_product = models.CharField(
        "Hist Product"
    )

    hist_file = models.CharField(
        "Hist File"
    )

    def __str__(self):
        return str(self.id)
    
    def getYear():
        return 2022    
    
class DownloadLog2023(models.Model):
    class Meta:
        managed: False
        db_table = "download_log_2023"
        verbose_name = 'Download log 2023 entry'
        verbose_name_plural = 'Download logs 2023'   

    id = models.UUIDField(
        'ID',
        primary_key=True
    )

    date = models.DateField(
        "Date"
    )

    time = models.TimeField(
        "Time without timezone"
    )

    x_edge_result_type = models.CharField(
        "X Edge Result Type"
    )

    x_edge_detailed_result_type = models.TextField(
        "X Edge Detailed Result Type"
    )

    x_host_header = models.CharField(
        "X Host Header"
    )

    cs_uri_stem = models.TextField(
        "CS URI Stem"
    )

    collection_id = models.CharField(
        "Collection ID"
    )

    collection_shortname = models.CharField(
        "Collection Short Name"
    )

    area_type_id = models.CharField(
        "Area Type ID"
    )

    file_type = models.CharField(
        "File Type"
    )

    hist_band = models.CharField(
        "Hist Band"
    )

    hist_collective = models.CharField(
        "Hist Collective"
    )

    hist_mission = models.CharField(
        "Hist Mission"
    )

    hist_type = models.CharField(
        "Hist Type"
    )

    hist_product = models.CharField(
        "Hist Product"
    )

    hist_file = models.CharField(
        "Hist File"
    )

    def __str__(self):
        return str(self.id)
    
    def getYear():
        return 2023
    
class DownloadLog2024(models.Model):
    class Meta:
        managed: False
        db_table = "download_log_2024"
        verbose_name = 'Download log 2024 entry'
        verbose_name_plural = 'Download logs 2024'   

    id = models.UUIDField(
        'ID',
        primary_key=True
    )

    date = models.DateField(
        "Date"
    )

    time = models.TimeField(
        "Time without timezone"
    )

    x_edge_result_type = models.CharField(
        "X Edge Result Type"
    )

    x_edge_detailed_result_type = models.TextField(
        "X Edge Detailed Result Type"
    )

    x_host_header = models.CharField(
        "X Host Header"
    )

    cs_uri_stem = models.TextField(
        "CS URI Stem"
    )

    collection_id = models.CharField(
        "Collection ID"
    )

    collection_shortname = models.CharField(
        "Collection Short Name"
    )

    area_type_id = models.CharField(
        "Area Type ID"
    )

    file_type = models.CharField(
        "File Type"
    )

    hist_band = models.CharField(
        "Hist Band"
    )

    hist_collective = models.CharField(
        "Hist Collective"
    )

    hist_mission = models.CharField(
        "Hist Mission"
    )

    hist_type = models.CharField(
        "Hist Type"
    )

    hist_product = models.CharField(
        "Hist Product"
    )

    hist_file = models.CharField(
        "Hist File"
    )

    def __str__(self):
        return str(self.id)
    
    def getYear():
        return 2024