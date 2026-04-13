from django.db import models
from hashlib import sha256

# Create your models here.
class StringAnalyzerModel(models.Model):
    # id = models. This field must have 'primay_key=True' to ensure it is used as primary key
    id = models.CharField(primary_key=True, editable=False)
    value = models.

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = sha256(self.value.encode('utf-8')).hexdigest()
        super.save(*args, **kwargs)

    class Meta:
        db_table = 'string_analyzer_model'