import django_filters

from core.models import Teacher


class TeacherFilter(django_filters.FilterSet):
    last_name = django_filters.CharFilter(lookup_expr='startswith')
    subjects__name = django_filters.CharFilter(lookup_expr='startswith')
    
    class Meta:
        model = Teacher
        fields = [
            'last_name',
            'subjects__name',
        ]

    def __init__(self, *args, **kwargs):
        super(TeacherFilter, self).__init__(*args, **kwargs)
        self.filters['last_name'].label= 'Last Name'
        self.filters['subjects__name'].label = 'Subjects Taught'