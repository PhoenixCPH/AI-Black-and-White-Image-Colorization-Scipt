import argparse
import os
import cv2
import torch
from colorizers import load_colorizer, get_device
from colorizers.util import load_img, resize_img, preprocess_img, postprocess_tens

def colorize_image(input_path, output_path, model_name='eccv16'):
    """
    使用AI模型对黑白JPEG图像进行上色。

    Args:
        input_path (str): 输入黑白JPEG图像的路径。
        output_path (str): 上色后彩色图像的输出路径。
        model_name (str, optional): 使用的着色模型名称。默认为 'eccv16'。
                                     可选模型包括 'eccv16', 'siggraph17', 'colorization'。
    """

    if not os.path.exists(input_path):
        print(f"错误：输入文件路径 '{input_path}' 不存在。")
        return

    # 获取设备 (GPU 如果可用，否则使用 CPU)
    device = get_device()
    print(f"使用设备: {device}")

    # 加载着色模型
    try:
        colorizer = load_colorizer(name=model_name, device=device)
    except Exception as e:
        print(f"错误：加载模型 '{model_name}' 失败。请确保模型文件已下载。")
        print(f"详细错误信息: {e}")
        print("请参考 colorizers 库的文档下载模型文件。")
        return

    # 加载和预处理图像
    img = load_img(input_path)
    img_bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) # 确保是灰度图
    img_resized = resize_img(img_bw, HW=(256, 256)) # 模型通常在固定大小图像上训练
    img_l = preprocess_img(img_resized, device=device)

    # 进行着色
    try:
        with torch.no_grad():
            output_tens = colorizer(img_l)
    except Exception as e:
        print(f"错误：图像着色过程中发生错误。")
        print(f"详细错误信息: {e}")
        return

    # 后处理和保存图像
    output_img = postprocess_tens(output_tens, torch.device('cpu'))
    output_img_rgb = cv2.cvtColor(output_img, cv2.COLOR_LAB2RGB) # 转换回 RGB
    output_img_resized_original = cv2.resize(output_img_rgb, (img.shape[1], img.shape[0])) # 恢复原始大小

    try:
        cv2.imwrite(output_path, output_img_resized_original)
        print(f"上色完成！彩色图像已保存到 '{output_path}'")
    except Exception as e:
        print(f"错误：保存图像到 '{output_path}' 失败。")
        print(f"详细错误信息: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="使用AI对黑白JPEG图像进行上色。")
    parser.add_argument("input_image", help="输入黑白JPEG图像的路径")
    parser.add_argument("output_image", help="输出彩色图像的路径")
    parser.add_argument("-m", "--model", default="eccv16", help="使用的着色模型名称 (eccv16, siggraph17, colorization)")

    args = parser.parse_args()

    colorize_image(args.input_image, args.output_image, args.model)