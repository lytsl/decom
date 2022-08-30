from django import template

register = template.Library()


@register.filter
def second_image(product):
    images = product.images.all()
    if len(images) == 1:
        return images[0].image.url
    return images[1].image.url
