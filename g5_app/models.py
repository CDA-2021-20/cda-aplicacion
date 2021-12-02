from django.db import models

# Create your models here.
class CsvFileUpload(models.Model):
    name = models.CharField(max_length=500)
    data_uploaded = models.DateTimeField(auto_now=True)
    csvfile = models.FileField(upload_to='csv_files', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.csvfile)