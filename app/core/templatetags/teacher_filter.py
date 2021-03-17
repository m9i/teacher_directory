from django import template

register = template.Library() 

@register.filter
def first_letter_value_initial(value):
    """ 
    Returns the first character of lastname or subjects in lowercase for a given name
    """
    if value.data:
        search_field = value.data
        return search_field[0].lower()
    else:
        return value

