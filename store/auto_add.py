import os
import random
import shutil

from img.bulk_create_manager import BulkCreateManager
from category.models import Category
from store.models import Product, ProductImage

bulk_manager = BulkCreateManager(chunk_size=100)
directory = r'D:\ProgramFiles\PyCharm\projects\ecom\img\product'
images_path = r'D:\ProgramFiles\PyCharm\projects\ecom\media\images\products'

folders = [(f.name, f.path) for f in os.scandir(directory) if f.is_dir()]
categories = Category.objects.all()
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et " \
        "dolore magna aliqua. Natoque penatibus et magnis dis parturient montes nascetur ridiculus mus. Vel pharetra " \
        "vel turpis nunc eget. Risus nec feugiat in fermentum posuere. Ac tortor vitae purus faucibus. Gravida cum " \
        "sociis natoque penatibus et magnis dis parturient montes. Condimentum vitae sapien pellentesque habitant " \
        "morbi tristique senectus et. Enim ut sem viverra aliquet eget sit amet tellus. Dis parturient montes " \
        "nascetur ridiculus. Massa sapien faucibus et molestie ac feugiat sed lectus vestibulum. Aliquam faucibus " \
        "purus in massa tempor nec feugiat. Amet nisl purus in mollis. Fringilla ut morbi tincidunt augue interdum " \
        "velit. Metus dictum at tempor commodo ullamcorper a lacus vestibulum sed. Lacus suspendisse faucibus " \
        "interdum posuere. Nulla facilisi cras fermentum odio eu. "

for d in list(folders):
    if d[0] == 'machines':
        continue
    category_name = d[0]
    category = categories.get(slug=category_name)
    files = []
    for f in os.scandir(d[1]):
        file = f.name
        file_name = file.split('.')[0]
        file_name = file_name.replace('-', ' ')
        file_name = file_name.replace('_', ' ')
        file_name = file_name.title()
        file_name = file_name.replace('Eight', 'K8')
        file_name = file_name.replace('Six', 'K6')
        if file_name in files:
            continue

        shutil.copy(f.path, images_path)
        files.append(file_name)

        slug = file_name.lower()
        slug = slug.replace(' ', '-')

        product = Product(
            product_name=file_name,
            slug=slug,
            price=random.randrange(20, 200, 10),
            stock=100,
            category=category,
            description=lorem,
        )
        image = ProductImage(image=images_path + '\\' + file, product=product)
        bulk_manager.add(product)
        bulk_manager.add(image)
    print(category_name)
bulk_manager.done()
