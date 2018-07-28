from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='action',
                             db_index=True,
                             on_delete='CASCADE')
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,
                                     blank=True,
                                     null=True,
                                     related_name='target_obj',
                                   db_index=True,
                                  on_delete='CASCADE')
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)

    target = GenericForeignKey('target_ct', 'target_id')



    created = models.DateTimeField(auto_now_add=True,
                                db_index=True)

    class Meta:
        ordering = ('-created',)