import os
from PIL import Image
import math

def createWallpaper(image_folder, width=1920, height=1080):
    if not image_folder:
        return False
    
    # 定义输出文件夹路径
    output_folder = os.path.join(image_folder, 'output')
    os.makedirs(output_folder, exist_ok=True)

    # 获取所有图片文件
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(valid_extensions)]

    
    if not image_files:
        print("No valid images found in the folder.")
        return None

    # 输出图像的宽高比为 16:9
    output_width = width
    output_height = height
    aspect_ratio = output_width / output_height

    # 读取所有图片并调整为正方形
    images = []
    for file in image_files:
        img = Image.open(file)
 
        width, height = img.size
        min_dim = min(width, height)

        start_x = (width - min_dim) // 2
        start_y = (height - min_dim) // 2

        img_cropped = img.crop((start_x, start_y, start_x + min_dim, start_y + min_dim)) # 裁剪为正方形

        images.append(img_cropped)


    n = len(images)
    columns = round(math.sqrt(n * aspect_ratio))  # 列数根据宽高比调整
    rows = round(n / columns)



    # 每个正方形图片在最终拼接图中的大小
    cell_width = output_width // columns
    cell_height = output_height // rows
    cell_size = max(cell_width, cell_height)  # 保证没有黑边

    # 创建输出画布
    output_image = Image.new("RGB", (output_width, output_height))

    # 填充图片
    for idx, img in enumerate(images):
        row, col = divmod(idx, columns) # row 商， col 余数
        x = col * cell_width
        y = row * cell_height

        img_cropped = resize_img(img, cell_width, cell_height)
        # 粘贴到输出画布，居中裁剪
        output_image.paste(img_cropped, (x, y))

    if n % rows != 0 or n % columns != 0:
        left_num = columns - n % columns
        # print('left_num: ', left_num)
        for i in range(left_num):
            row = rows - 1
            col = n % columns + i

            x = col * cell_width
            y = row * cell_height

            img_cropped = resize_img(images[i], cell_width, cell_height)
            # 粘贴到输出画布，居中裁剪
            output_image.paste(img_cropped, (x, y))
            


    # 保存最终拼接结果
    output_path = os.path.join(output_folder, 'album_wall.jpg')
    output_image.save(output_path)
    print(f"Album wall created and saved to {output_path}")
    return output_path


def resize_img(img, cell_width, cell_height):
    max_mid = max(cell_width, cell_height)
        
    # 调整每张图片的大小以适应单元格
    img = img.resize((max_mid, max_mid), Image.Resampling.LANCZOS)

    width, height = img.size
    start_x = (width - cell_width) // 2
    start_y = (height - cell_height) // 2

    img_cropped = img.crop((start_x, start_y, start_x + cell_width, start_y + cell_height))
    return img_cropped

