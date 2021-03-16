SELECT setval('django_content_type_id_seq', (SELECT MAX(id) FROM django_content_type));
select max(id) from django_content_type;
alter sequence django_content_type_id_seq restart with 295000;

    