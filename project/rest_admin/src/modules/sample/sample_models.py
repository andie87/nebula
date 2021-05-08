""" Sample Model. """
from django.db import models

class Sample(models.Model):
    """ Sample: for creating tbl_sample table."""
    objects = models.Manager()

    name = models.CharField("Name", max_length=60)
    age = models.IntegerField("Age")
    email = models.EmailField("Email", max_length=40)
    about = models.TextField("About", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta(object):
        """ Meta: for metadata sample."""
        db_table = "tbl_sample"
        verbose_name = "Sample"
        verbose_name_plural = "Samples"
