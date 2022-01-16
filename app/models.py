from django.db import models


class CorrelationResult(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    first_param = models.CharField(max_length=100)
    second_param = models.CharField(max_length=100)
    value = models.FloatField(null=True)
    p_value = models.FloatField(null=True)
