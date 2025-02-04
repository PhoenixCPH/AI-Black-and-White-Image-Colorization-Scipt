# AI黑白图片上色Python脚本

**请注意：**

- **需要安装库:**  你需要先安装 colorizers, torch, torchvision, 和 opencv-python。
- **需要下载模型:**  colorizers 库需要预先下载训练好的模型文件。
- **效果可能有限:**  AI上色效果取决于模型和图片的质量。对于复杂的图像或者模型未见过的场景，效果可能不尽如人意。

**使用方法:**

1. **安装依赖库:**
   打开终端或命令提示符，运行以下命令安装必要的Python库：
   ```bash
   pip install colorizers torch torchvision opencv-python
   ```

2. **下载模型文件:**
   你需要下载 `colorizers` 库使用的预训练模型。模型文件通常比较大。
   * **模型下载位置:**  `colorizers` 库的模型默认会下载到 `~/.cache/torch/hub/checkpoints/` 目录下 ( `~` 代表你的用户目录)。
   * **下载方法:**  通常在第一次运行 `load_colorizer()` 函数时，如果本地没有模型文件，`colorizers` 会尝试自动下载。  如果自动下载失败，你需要手动下载。  你可以参考 `colorizers` 库的文档或者GitHub仓库 (例如：[https://github.com/richzhang/colorization](https://github.com/richzhang/colorization)) 查找模型下载链接。
   * **常用模型:**  `eccv16`, `siggraph17`, `colorization`  是 `colorizers` 库提供的模型名称。  `eccv16` 是一个相对常用的模型。

3. **保存脚本:**
   将上面的Python代码保存到一个文件，例如 `colorize_script.py`。

4. **运行脚本:**
   在终端或命令提示符中，导航到脚本所在的目录，并运行以下命令：
   ```bash
   python colorize_script.py 输入图片路径.jpg 输出图片路径_彩色.jpg [-m 模型名称]
   ```
   * **`输入图片路径.jpg`**:  替换为你的黑白JPEG图片的路径。
   * **`输出图片路径_彩色.jpg`**:  替换为你想要保存彩色图片的路径。
   * **`[-m 模型名称]`**:  可选参数，如果你想使用不同的模型，可以使用 `-m 模型名称` 来指定。例如 `-m siggraph17`。  如果省略，默认使用 `eccv16` 模型。

   **示例:**
   ```bash
   python colorize_script.py black_white_photo.jpg colored_photo.jpg
   ```

**代码解释:**

* **导入库:** 导入必要的库，包括 `argparse` (用于命令行参数解析), `os` (文件路径操作), `cv2` (OpenCV用于图像处理), `torch` (PyTorch深度学习框架), 以及 `colorizers` 库的相关模块。
* **`colorize_image` 函数:**
    * 检查输入文件是否存在。
    * 使用 `get_device()` 获取可用的设备 (GPU或CPU)。
    * 使用 `load_colorizer()` 加载指定的着色模型。
    * 使用 `load_img()`, `resize_img()`, `preprocess_img()` 函数预处理输入图像，将其转换为模型可以接受的格式。
    * 使用 `colorizer(img_l)` 进行图像着色。
    * 使用 `postprocess_tens()` 后处理模型输出的张量，并将其转换为图像格式。
    * 使用 `cv2.cvtColor()` 将颜色空间转换回 RGB。
    * 使用 `cv2.resize()` 将图像大小恢复到原始大小。
    * 使用 `cv2.imwrite()` 保存上色后的彩色图像。
* **`if __name__ == '__main__':` 代码块:**
    * 使用 `argparse` 创建命令行参数解析器，允许用户通过命令行指定输入图片路径、输出图片路径和模型名称。
    * 获取命令行参数。
    * 调用 `colorize_image()` 函数执行图像上色操作。

**注意事项:**

* **模型下载:**  务必确保你下载了 `colorizers` 库所需的模型文件，并将其放置在正确的位置。
* **GPU加速:**  如果你的电脑有NVIDIA GPU，并且安装了CUDA和PyTorch的GPU版本，脚本会自动使用GPU进行加速，这将大大提高上色速度。
* **模型选择:**  `colorizers` 库提供了不同的模型 (`eccv16`, `siggraph17`, `colorization`)，你可以尝试不同的模型，看看哪个模型对你的图片效果更好。
* **图像质量:**  AI上色效果受到输入图像质量的影响。清晰的黑白图像通常能得到更好的上色结果。
* **局限性:**  AI上色并非完美，对于一些复杂的场景或纹理，可能会出现颜色不准确或不自然的情况。
