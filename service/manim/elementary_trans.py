import os
import numpy as np
from manim import config, Scene, NumberPlane, Vector, MathTex, VGroup, Create, Transform, YELLOW, UP

# 配置 Manim 输出目录
BASE_DIR = os.path.join(os.getcwd(), 'static')
config.media_dir = BASE_DIR
config.tex_dir = os.path.join(BASE_DIR, 'Tex')
config.image_dir = os.path.join(BASE_DIR, 'images')
config.video_dir = os.path.join(BASE_DIR, 'videos')
config.pixel_height = 446
config.pixel_width = 386

def sanitize_filename(filename):
    """移除或替换文件名中的非法字符"""
    return "".join(c if c.isalnum() or c in '._-' else '_' for c in filename)

def render_matrix_transformation(matrix_str, swap_rows, multiply_row, row_addition):
    # 处理用户输入的矩阵
    matrix_str = matrix_str.strip("[]")
    rows_str = matrix_str.split(";")
    matrix = np.array([[float(num_str) for num_str in row_str.split(",")] for row_str in rows_str])

    # 生成唯一文件名
    sanitized_matrix_str = sanitize_filename(matrix_str)
    filename = f"ElementaryTransformation_{sanitized_matrix_str}_{swap_rows}_{multiply_row}_{row_addition}.mp4"
    output_dir = os.path.join(config.video_dir, '446p60', 'cache', 'ElementaryTransformation')
    os.makedirs(output_dir, exist_ok=True)
    video_path = os.path.join(output_dir, filename)

    # 检查文件是否已存在
    if os.path.exists(video_path):
        return video_path

    # 动态设置 Manim 输出路径
    config.output_file = video_path

    # 创建 Manim 场景类
    class ElementaryMatrixOperations(Scene):
        def construct(self):
            plane = NumberPlane()
            self.add(plane)

            vector1 = Vector(matrix[:, 0], color=YELLOW)
            vector2 = Vector(matrix[:, 1], color=YELLOW)

            label1 = MathTex(f"[{matrix[0, 0]}, {matrix[1, 0]}]").next_to(vector1, UP)
            label2 = MathTex(f"[{matrix[0, 1]}, {matrix[1, 1]}]").next_to(vector2, UP)

            vector_and_label1 = VGroup(vector1, label1)
            vector_and_label2 = VGroup(vector2, label2)

            self.play(Create(vector_and_label1), Create(vector_and_label2), run_time=2)
            self.wait(1)
            self.play(Transform(plane.copy(), plane.apply_matrix(matrix)), run_time=4)
            self.wait(1)

    # 渲染动画
    try:
        scene = ElementaryMatrixOperations()
        scene.render()
    except Exception as e:
        print(f"Rendering error: {e}")
        raise

    # 重置输出配置
    config.output_file = None

    return video_path