import os
import django
import random
from django.core.files import File
from django.conf import settings

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcomRecomendation.settings')
django.setup()

from store.models import Product, ProductImage

def add_sample_images():
    # Đường dẫn đến thư mục chứa ảnh mẫu
    sample_images_dir = os.path.join(settings.BASE_DIR, 'static', 'sample_images')
    
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(sample_images_dir, exist_ok=True)
    
    # Tạo các file ảnh mẫu cho từng loại sản phẩm
    categories = {
        'Áo': ['ao1.jpg', 'ao2.jpg', 'ao3.jpg'],
        'Quần': ['quan1.jpg', 'quan2.jpg', 'quan3.jpg'],
        'Giày dép': ['giay1.jpg', 'giay2.jpg', 'giay3.jpg'],
        'Phụ kiện': ['phukien1.jpg', 'phukien2.jpg', 'phukien3.jpg']
    }
    
    # Tạo file ảnh mẫu nếu chưa tồn tại
    for category, images in categories.items():
        for img_name in images:
            img_path = os.path.join(sample_images_dir, img_name)
            if not os.path.exists(img_path):
                # Tạo một ảnh trống 500x500 với màu ngẫu nhiên
                from PIL import Image
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                img = Image.new('RGB', (500, 500), color)
                img.save(img_path)

    # Thêm ảnh cho từng sản phẩm
    products = Product.objects.all()
    for product in products:
        # Xác định danh mục của sản phẩm
        category_name = product.category_main.category_name if product.category_main else 'Phụ kiện'
        category_images = categories.get(category_name, categories['Phụ kiện'])
        
        # Kiểm tra xem sản phẩm đã có ảnh chưa
        if not ProductImage.objects.filter(product=product).exists():
            # Thêm ảnh mặc định
            default_image = category_images[0]
            with open(os.path.join(sample_images_dir, default_image), 'rb') as img_file:
                ProductImage.objects.create(
                    product=product,
                    image_type='default',
                    image=File(img_file, name=f"{product.slug}_default.jpg")
                )
            
            # Thêm các ảnh khác
            for i, image_name in enumerate(category_images[1:], 1):
                image_type = ['front', 'back'][i-1]  # Chỉ thêm 2 ảnh phụ
                with open(os.path.join(sample_images_dir, image_name), 'rb') as img_file:
                    ProductImage.objects.create(
                        product=product,
                        image_type=image_type,
                        image=File(img_file, name=f"{product.slug}_{image_type}.jpg")
                    )
        
        print(f"Đã thêm ảnh cho sản phẩm: {product.product_name}")

if __name__ == '__main__':
    print("Bắt đầu thêm ảnh mẫu...")
    add_sample_images()
    print("Hoàn thành!") 