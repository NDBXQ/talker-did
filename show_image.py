import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def show_two_images(image_path1, image_path2):
    # 创建一个 figure 和两个子图（axes）
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))  # 创建一行两列的布局
    
    # 第一张图片
    img1 = mpimg.imread(image_path1)
    axes[0].imshow(img1)
    axes[0].axis('off')  # 关闭坐标轴
    axes[0].set_title('Image 1')  # 设置标题
    
    # 第二张图片
    img2 = mpimg.imread(image_path2)
    axes[1].imshow(img2)
    axes[1].axis('off')  # 关闭坐标轴
    axes[1].set_title('Image 2')  # 设置标题
    
    # 显示图片
    plt.tight_layout()  # 自动调整布局
    plt.show()