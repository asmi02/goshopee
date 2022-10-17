from django.template.defaulttags import register

from productshopping.models import Category, SubCategory


@register.filter(name='times')
def times(number):
    return range(number)

@register.inclusion_tag("fetchmen.html")
def fetch_categories_men():
    # categoriesdata=SubCategory.objects.filter(category_type.category_name='Mens')
    catobj = Category.objects.get(category_name='Mens')
    categoriesdata=SubCategory.objects.filter(category_type=catobj)
    return {"categorydata":categoriesdata}


@register.inclusion_tag("fetchwomen.html")
def fetch_categories_women():
    # categoriesdata=SubCategory.objects.filter(category_type.category_name='Womens')
    catobj = Category.objects.get(category_name='Womens')
    categoriesdata = SubCategory.objects.filter(category_type=catobj)
    # categoriesdata=SubCategory.objects.filter(category_type=17)
    return {"categorydata":categoriesdata}