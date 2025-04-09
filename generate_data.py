import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcomRecomendation.settings')
django.setup()

from category.models import CategoryMain, SubCategory
from store.models import Product, Variation, ProductImage

def create_categories():
    # Danh mục chính
    main_categories = [
        {
            'name': 'Áo',
            'slug': 'ao',
            'description': 'Các loại áo thời trang'
        },
        {
            'name': 'Quần',
            'slug': 'quan',
            'description': 'Các loại quần thời trang'
        },
        {
            'name': 'Giày dép',
            'slug': 'giay-dep',
            'description': 'Các loại giày dép thời trang'
        },
        {
            'name': 'Phụ kiện',
            'slug': 'phu-kien',
            'description': 'Các loại phụ kiện thời trang'
        }
    ]

    # Danh mục phụ
    sub_categories = {
        'Áo': [
            {'name': 'Áo thun', 'slug': 'ao-thun'},
            {'name': 'Áo sơ mi', 'slug': 'ao-so-mi'},
            {'name': 'Áo khoác', 'slug': 'ao-khoac'},
            {'name': 'Áo len', 'slug': 'ao-len'}
        ],
        'Quần': [
            {'name': 'Quần jean', 'slug': 'quan-jean'},
            {'name': 'Quần kaki', 'slug': 'quan-kaki'},
            {'name': 'Quần tây', 'slug': 'quan-tay'},
            {'name': 'Quần short', 'slug': 'quan-short'}
        ],
        'Giày dép': [
            {'name': 'Giày thể thao', 'slug': 'giay-the-thao'},
            {'name': 'Giày tây', 'slug': 'giay-tay'},
            {'name': 'Sandal', 'slug': 'sandal'},
            {'name': 'Dép', 'slug': 'dep'}
        ],
        'Phụ kiện': [
            {'name': 'Thắt lưng', 'slug': 'that-lung'},
            {'name': 'Ví', 'slug': 'vi'},
            {'name': 'Túi xách', 'slug': 'tui-xach'},
            {'name': 'Mũ nón', 'slug': 'mu-non'}
        ]
    }

    created_categories = {}
    
    # Tạo danh mục chính
    for cat in main_categories:
        category, created = CategoryMain.objects.get_or_create(
            category_name=cat['name'],
            defaults={
                'slug': cat['slug'],
                'description': cat['description']
            }
        )
        created_categories[cat['name']] = category
        print(f"{'Created' if created else 'Retrieved'} main category: {category.category_name}")

        # Tạo danh mục phụ
        for sub_cat in sub_categories[cat['name']]:
            sub_category, created = SubCategory.objects.get_or_create(
                category=category,
                sub_category_name=sub_cat['name'],
                defaults={
                    'slug': sub_cat['slug'],
                    'description': f'Danh mục {sub_cat["name"]}'
                }
            )
            print(f"{'Created' if created else 'Retrieved'} sub category: {sub_category.sub_category_name}")

    return created_categories

def create_products(categories):
    brands = ['Nike', 'Adidas', 'Puma', 'Uniqlo', 'Zara', 'H&M']
    genders = ['Nam', 'Nữ', 'Unisex']
    seasons = ['Xuân', 'Hạ', 'Thu', 'Đông']
    years = list(range(2020, 2025))

    for main_cat in categories.values():
        for sub_cat in main_cat.subcategories.all():
            # Tạo 5 sản phẩm cho mỗi danh mục phụ
            for i in range(5):
                name = f"{sub_cat.sub_category_name} {i+1}"
                slug = f"{sub_cat.slug}-{i+1}"
                
                product, created = Product.objects.get_or_create(
                    product_name=name,
                    slug=slug,
                    defaults={
                        'category_main': main_cat,
                        'sub_category': sub_cat,
                        'mrp_price': Decimal(random.randint(100, 1000)),
                        'price': Decimal(random.randint(50, 900)),
                        'rating': random.randint(3, 5),
                        'short_desp': f'Mô tả ngắn cho {name}',
                        'description': f'Mô tả chi tiết cho {name}',
                        'stock': random.randint(0, 100),
                        'is_available': True,
                        'brand_name': random.choice(brands),
                        'gender': random.choice(genders),
                        'season': random.choice(seasons),
                        'year': random.choice(years)
                    }
                )
                print(f"{'Created' if created else 'Retrieved'} product: {product.product_name}")

                # Tạo biến thể màu sắc
                colors = ['Đen', 'Trắng', 'Xanh', 'Đỏ', 'Vàng']
                for color in colors:
                    variation, _ = Variation.objects.get_or_create(
                        Product=product,
                        Variation_category='Color',
                        Variation_value=color
                    )

                # Tạo biến thể kích thước
                sizes = ['S', 'M', 'L', 'XL', 'XXL']
                for size in sizes:
                    variation, _ = Variation.objects.get_or_create(
                        Product=product,
                        Variation_category='Size',
                        Variation_value=size
                    )

def main():
    print("Bắt đầu tạo dữ liệu mẫu...")
    categories = create_categories()
    create_products(categories)
    print("Hoàn thành tạo dữ liệu mẫu!")

if __name__ == '__main__':
    main() 