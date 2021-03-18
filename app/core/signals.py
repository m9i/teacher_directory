import os
import csv
import zipfile
from io import StringIO

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Teacher, TeacherBulkUpload

@receiver(post_save, sender=TeacherBulkUpload)
def create_bulk_teacher(sender, created, instance, *args, **kwargs):
  if created:
    opened = StringIO(instance.csv_file.read().decode())
    if instance.image_zip_file:
      with zipfile.ZipFile(instance.image_zip_file,'r') as zf:  
        zf.extractall(settings.MEDIA_ROOT)
    reading = csv.DictReader(opened, delimiter=',')
    to_create = []
    to_update = []
    
    for row in reading:
      if 'Email Address' in row and row['Email Address']:
        email = row['Email Address'].strip() 
        first_name = row['First Name'].strip()  if 'First Name' in row and row['First Name'] else ''
        last_name = row['Last Name'].strip()  if 'Last Name' in row and row['Last Name'] else ''
        room = row['Room Number'].strip()  if 'Room Number' in row and row['Room Number'] else ''
        phone = row['Phone Number'].strip()  if 'Phone Number' in row and row['Phone Number'] else ''
        profile_pic = row['Profile picture'].strip() if 'Profile picture' in row and row['Profile picture'] else ''
        subjects = row['Subjects taught'].strip()  if 'Subjects taught' in row and row['Subjects taught'] else ''
        
        check = Teacher.objects.filter(email=email).exists()
        if not check:
          to_create.append(
            Teacher(
                email=email,
                first_name=first_name,
                last_name=last_name,
                room=room,
                phone=phone,
                profile_pic=profile_pic,
                subjects=subjects,
            )
          )
        else:
            to_update.append(
              Teacher.objects.get(email=email)
          )
    fields = ['first_name','last_name','email','phone','room','subjects','profile_pic']
    Teacher.objects.bulk_create(to_create)
    Teacher.objects.bulk_update(to_update, 
                                fields=fields, 
                                batch_size=5000)

    instance.csv_file.close()
    instance.delete()


def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(post_delete, sender=TeacherBulkUpload)
def delete_csv_file(sender, instance, *args, **kwargs):
  if instance.csv_file:
    _delete_file(instance.csv_file.path)


@receiver(post_delete, sender=Teacher)
def delete_profiel_pic_on_delete(sender, instance, *args, **kwargs):
  if instance.profile_pic:
    _delete_file(instance.profile_pic.path)
    
    
# @receiver(post_save, sender=Teacher)
# def check_subjects_limit(sender, instance, **kwargs):
    # if set(instance.subjects.split(',')).__len__() > 5: 
        #  raise ValidationError(
            #  _("Can't add more than 5 subjects to a Teacher"))
     
