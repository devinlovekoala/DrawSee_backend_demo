import os
import numpy as np
from manim import *

# 配置manim输出目录为Flask项目的静态文件夹
config.media_dir = os.path.join(os.getcwd(), 'static')
config.pixel_height = 446
config.pixel_width = 386

def sanitize_filename(filename):
    """移除或替换文件名中的非法字符"""
    return "".join(c if c.isalnum() or c in '._-' else '_' for c in filename)

def inverse_trans(matrix_str):
    # 将字符串形式的矩阵转换为NumPy数组
    matrix_str = matrix_str.strip("[]")
    rows_str = matrix_str.split(";")
    matrix = [[float(num_str) for num_str in row_str.split(",")] for row_str in rows_str]
    matrix = np.array(matrix)

    # 生成唯一的视频文件名
    sanitized_matrix_str = sanitize_filename(matrix_str)
    video_filename = f'InverseTransformation_{sanitized_matrix_str}.mp4'
    output_video_dir = os.path.join(config.media_dir, 'videos', '446p60', 'cache', 'InverseTransformation')
    os.makedirs(output_video_dir, exist_ok=True)
    
    target_video_path = os.path.join(output_video_dir, video_filename)

    # 如果视频文件已存在，则直接返回路径
    if os.path.exists(target_video_path):
        return target_video_path

    # 动态设置输出文件名
    config.output_file = target_video_path

    class InverseTransformation(Scene):
        def construct(self):
            # 创建二维坐标系
            plane = NumberPlane().apply_matrix(matrix)
            # 将新的坐标系添加到场景中
            self.add(plane)

            # 创建表示矩阵列向量的向量
            vector1 = Vector(matrix[:, 0], color=YELLOW)
            vector2 = Vector(matrix[:, 1], color=YELLOW)

            # 创建表示向量坐标的标签
            label1 = MathTex(f"[{matrix[0, 0]}, {matrix[1, 0]}]").next_to(vector1, UP)
            label2 = MathTex(f"[{matrix[0, 1]}, {matrix[1, 1]}]").next_to(vector2, UP)

            # 将向量和标签组合在一起
            vector_and_label1 = VGroup(vector1, label1)
            vector_and_label2 = VGroup(vector2, label2)

            # 添加向量和标签到场景，并增加动画播放时长
            self.play(Create(vector_and_label1), Create(vector_and_label2), run_time=2)
            self.wait(1)

            # 移除标签
            self.remove(label1, label2)

            # 计算原矩阵的逆矩阵
            inverse_matrix = np.linalg.inv(matrix)

            # 应用矩阵变换，并增加动画播放时长
            self.play(Transform(plane, plane.copy().apply_matrix(inverse_matrix)),
                      Transform(vector1, vector1.copy().apply_matrix(inverse_matrix)),
                      Transform(vector2, vector2.copy().apply_matrix(inverse_matrix)),
                      run_time=2)
            self.wait(1)

    # 渲染场景
    scene = InverseTransformation()
    scene.render()
    
    # 重置输出文件名配置
    config.output_file = None
    
    return target_video_path
