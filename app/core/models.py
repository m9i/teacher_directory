from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.urls import reverse
from django.conf import settings
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _




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
    
    @classmethod
    def bulk_update_or_create(cls, common_keys, unique_key_name, unique_key_to_defaults):
        """
        common_keys: {field_name: field_value}
        unique_key_name: field_name
        unique_key_to_defaults: {field_value: {field_name: field_value}}
        
        ex. Event.bulk_update_or_create(
            {"organization": organization}, "external_id", {1234, {"started": True}}
        )
        """
        with transaction.atomic():
            filter_kwargs = dict(common_keys)
            filter_kwargs[f"{unique_key_name}__in"] = unique_key_to_defaults.keys()
            existing_objs = {
                getattr(obj, unique_key_name): obj
                for obj in cls.objects.filter(**filter_kwargs).select_for_update()
            }
            
            create_data = {
                k: v for k, v in unique_key_to_defaults.items() if k not in existing_objs
            }
            for unique_key_value, obj in create_data.items():
                obj[unique_key_name] = unique_key_value
                obj.update(common_keys)
            creates = [cls(**obj_data) for obj_data in create_data.values()]
            if creates:
                cls.objects.bulk_create(creates)
            
            update_fields = {"updated_on"}
            updates = []
            for key, obj in existing_objs.items():
                obj.update(unique_key_to_defaults[key], save=False)
                update_fields.update(unique_key_to_defaults[key].keys())
                updates.append(obj)
            if existing_objs:
                cls.objects.bulk_update(updates, update_fields)
        return len(creates), len(updates)

    
    def update(self, update_dict=None, save=True, **kwargs):
        """ Helper method to update objects """
        if not update_dict:
            update_dict = kwargs
        # This set should contain the name of the `auto_now` field of the model
        update_fields = {"updated_on"}
        for k, v in update_dict.items():
            setattr(self, k, v)
            update_fields.add(k)
        if save:
            self.save(update_fields=update_fields)


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
        upload_to="teacher_dir/teacher_profile_pic",
        default='avatar.png' , blank=True)
    
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
            return f'{settings.STATIC_URL}dist/img/avatar.png'      


@receiver(pre_save, sender=Teacher)
def check_subjects_limit(sender, instance, **kwargs):
    if instance.subjects.split(',').__len__() > 5: 
         raise ValidationError(
             _("Can't add more than 5 subjects to a Teacher"))
     
@receiver(pre_save, sender=Teacher)
def check_has_email(sender, instance, **kwargs):
    if not instance.email:
        raise ValidationError(_('The given email must be set'))


class TeacherBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(
        _('Date Uploaded'), auto_now=True)
    csv_file = models.FileField(
        _('File Upload'), 
        upload_to='teachers/bulkupload/')
    image_zip_file = models.FileField(
        _('zip File Image Upload'), 
        upload_to='teachers/bulkupload/images', blank=True)
    
    
    class Meta:
        ordering = ['date_uploaded', ]

    def __str__(self):
        return self.csv_file.name.split('/')[-1]

@receiver(pre_save, sender=TeacherBulkUpload)
def validate_file_extension(sender, instance, **kwargs):
    ext = os.path.splitext(instance.csv_file.name)[1]  
    valid_extensions = ['.csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            _("Uploaded file isn't in a right format!, it should be a .csv file."))
        
    
