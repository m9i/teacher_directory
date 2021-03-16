import os

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from django.core.validators import FileExtensionValidator



class Logged(models.Model):
    date_created = models.DateTimeField(
        _('Date Created'),  
        auto_now_add=True, null=True, blank=True)
    date_modified = models.DateTimeField(
        _('Date Modified'),  
        auto_now=True, null=True, blank=True)
    date_removed = models.DateTimeField(
        _('Date Removed'),
        null=True, blank=True)
    is_active = models.BooleanField(
        _('Active'), default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        return super(Logged, self).save(*args, **kwargs)

    def alive(self):
        return self.date_removed is None
    alive.boolean = True
    
    class Meta:
        abstract = True
    


class Teacher(Logged):
    email = models.EmailField(
        _('Email Address'),
         unique=True,
         db_index=True)
    first_name = models.CharField(
        _('First Name'), max_length=255, blank=True)
    last_name = models.CharField(
        _('Last Name'), max_length=255, blank=True)
    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", 
        message=_("Entered mobile number isn't in a right format!"))
    phone = models.CharField(
        _('Phone Number'),
        #  validators=[mobile_num_regex],
         max_length=255, blank=True)
    room = models.CharField(
        _('Room Number'), max_length=255, blank=True)
    subjects = models.CharField(
        _('Subjects taught'), max_length=255, blank=True)
    profile_pic = models.ImageField(
        _('Profile picture'),
        upload_to="",
        validators=[FileExtensionValidator(allowed_extensions=['JPG','jpg','png'])],
        default='avatar.png' , blank=True)
    validation_error=models.CharField(
        _('Validation Error'), max_length=255, blank=True)
    
    class Meta:
        ordering = ['first_name', 'last_name', 'email']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.room})'

    def get_absolute_url(self):
        return reverse('teacher-detail', kwargs={'pk': self.pk})

    def get_photo_url(self):
        try:
            if self.profile_pic.seek:
                return self.profile_pic.url
        except FileNotFoundError:
            return f'{settings.MEDIA_ROOT}avatar.png'      




@receiver(pre_save, sender=Teacher)
def check_subjects_limit(sender, instance, **kwargs):
    if instance.subjects.split(',').__len__() > 5: 
         return ValidationError(
             _("Can't add more than 5 subjects to a Teacher"))
     
@receiver(pre_save, sender=Teacher)
def check_has_email(sender, instance, **kwargs):
    if not instance.email:
        return ValidationError(_('The given email must be set'))


class TeacherBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(
        _('Date Uploaded'), auto_now=True)
    csv_file = models.FileField(
        _('File Upload'),
        validators=[FileExtensionValidator(allowed_extensions=['csv'])],
        upload_to='teachers/bulkupload')
    image_zip_file = models.FileField(
        _('zip File Image Upload'),
        validators=[FileExtensionValidator(allowed_extensions=['zip'])],
        upload_to='teachers/bulkupload/images', blank=True)
    
    
    class Meta:
        ordering = ['date_uploaded', ]

    def __str__(self):
        return self.csv_file.name.split('/')[-1]


        
    
