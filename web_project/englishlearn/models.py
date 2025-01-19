from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Level(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='levels')
    name = models.CharField(max_length=10)
    learning_resources = models.TextField(help_text="Comma-separated list of links")
    test_link = models.URLField()

    def __str__(self):
        return f"{self.language.name} - {self.name}"
# Create your models here.
