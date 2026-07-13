from .models import Category

# create your context processors here.


def categories(request):
    context = {'categories': Category.objects.all()}
    return context