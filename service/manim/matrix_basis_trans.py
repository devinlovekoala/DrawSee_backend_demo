import os
import numpy as np
from manim import *

config.media_dir = os.path.join(os.getcwd(), 'static')
config.pixel_height = 446
config.pixel_width = 386

def sanitize_filename(filename):
    """移除或替换文件名中的非法字符"""
    return "".join(c if c.isalnum() or c in '._-' else '_' for c in filename)

def generate_basis_transformation_video(matrix_str1, matrix_str2):
    def parse_matrix_str(matrix_str):
        matrix_str = matrix_str.replace(';', '],[')
        return np.array(eval(f'[{matrix_str}]'))

    matrix1 = parse_matrix_str(matrix_str1)
    matrix2 = parse_matrix_str(matrix_str2)

    # 生成唯一的视频文件名
    sanitized_matrix_str1 = sanitize_filename(matrix_str1)
    sanitized_matrix_str2 = sanitize_filename(matrix_str2)
    video_filename = f'BasisTransformation_{sanitized_matrix_str1}_to_{sanitized_matrix_str2}.mp4'
    output_video_dir = os.path.join(config.media_dir, 'videos', '446p60', 'cache', 'BasisTransformation')
    os.makedirs(output_video_dir, exist_ok=True)
    
    target_video_path = os.path.join(output_video_dir, video_filename)

    # 如果视频文件已存在，则直接返回路径
    if os.path.exists(target_video_path):
        return target_video_path

    # 动态设置输出文件名
    config.output_file = target_video_path

    class BasisTransformation(Scene):
        def construct(self):
            # 创建初始坐标系
            plane1 = NumberPlane()
            self.add(plane1)
            self.wait(1)

            # 第一个画面：用黄色箭头展示第一个矩阵的列向量，并在末端显示坐标
            arrows1 = []
            coords1_list = []
            for i in range(2):
                arrow = Arrow(plane1.c2p(0, 0), plane1.c2p(*matrix1[:, i]), color=YELLOW, buff=0)
                arrows1.append(arrow)
                self.add(arrow)

                coords1 = MathTex("\\left[", f"{matrix1[0, i]}", ",", f"{matrix1[1, i]}", "\\right]").next_to(
                    arrow.get_end(), UR, buff=0.1)
                coords1_list.append(coords1)
                self.add(coords1)
            self.wait(1)

            # 变换坐标系以匹配第一个矩阵的基
            transformed_plane1 = plane1.copy().apply_matrix(matrix1)
            self.play(Transform(plane1, transformed_plane1), run_time=1)
            self.wait(1)

            # 从场景中移除第一个矩阵的向量和坐标
            self.remove(*arrows1, *coords1_list)

            # 创建一个新的坐标系，用于第二次变换
            plane2 = NumberPlane(
                axis_config={"stroke_color": ORANGE},
                background_line_style={
                    "stroke_color": ORANGE,
                }
            )
            self.add(plane2)
            self.wait(1)

            # 用蓝色箭头显示第二个矩阵的列向量，并在末端显示坐标
            arrows2 = []
            coords2_list = []
            for i in range(2):
                arrow = Arrow(plane2.c2p(0, 0), plane2.c2p(*matrix2[:, i]), color=BLUE, buff=0)
                arrows2.append(arrow)
                self.add(arrow)

                # 添加向量坐标
                coords2 = MathTex("\\left[", f"{matrix2[0, i]}", ",", f"{matrix2[1, i]}", "\\right]").next_to(
                    arrow.get_end(), UR, buff=0.1)
                coords2_list.append(coords2)
                self.add(coords2)
            self.wait(1)

            # 变换坐标系以匹配第二个矩阵的基
            transformed_plane2 = plane2.copy().apply_matrix(matrix2)
            self.play(Transform(plane2, transformed_plane2), run_time=1)
            self.wait(1)

    # 渲染场景
    scene = BasisTransformation()
    scene.render()

    # 重置输出文件名配置
    config.output_file = None
    
    return target_video_path
