# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from common.managers import UserManager
from uuid import uuid4


class User(AbstractUser):
    email = models.EmailField(
        _('Email'), unique=True, blank=False, null=False,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    phone = models.IntegerField(_("Phone Number"), null=True)
    language = models.CharField(choices=settings.LANGUAGES, default='tr', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def get_full_name(self):
        if self.first_name and self.last_name:
            return ' '.join([self.first_name, self.last_name])
        return None

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_moderator(self):
        if self.is_staff:
            return True
        if self.groups.filter(name='Moderators').exists():
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(uuid4())
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('created_at',)
        indexes = [models.Index(fields=['email'], name='email_idx')]