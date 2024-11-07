import os
import numpy as np
from manim import *

# 配置 Manim 输出路径和视频参数
config.media_dir = os.path.join(os.getcwd(), 'static')
config.pixel_height = 446
config.pixel_width = 386

def sanitize_filename(filename):
    """移除或替换文件名中的非法字符"""
    return "".join(c if c.isalnum() or c in '._-' else '_' for c in filename)

def matrix_eigen_transform(matrix):
    # 检查矩阵是否是2x2矩阵
    if matrix.shape != (2, 2):
        raise ValueError("矩阵需要是2x2的。")

    # 检查矩阵是否有特征值
    if np.linalg.det(matrix) == 0:
        raise ValueError("输入矩阵行列式为0，不可逆，不存在特征值")

    # 计算矩阵的特征值和特征向量
    eig_vals, eig_vecs = np.linalg.eig(matrix)

    # 生成唯一的视频文件名
    matrix_str = str(matrix).replace('\n', '').replace(' ', '')
    sanitized_matrix_str = sanitize_filename(matrix_str)
    video_filename = f'EigenTransformation_{sanitized_matrix_str}.mp4'
    output_video_dir = os.path.join(config.media_dir, 'videos', '446p60', 'cache', 'EigenTransformation')
    os.makedirs(output_video_dir, exist_ok=True)
    
    target_video_path = os.path.join(output_video_dir, video_filename)

    # 如果视频文件已存在，则直接返回路径
    if os.path.exists(target_video_path):
        return target_video_path

    # 动态设置输出文件名
    config.output_file = target_video_path

    class EigenTransformation(Scene):
        def construct(self):
            # 创建坐标系
            plane = NumberPlane()
            self.add(plane)

            # 创建特征向量，并将它们归一化为长度为2的向量，以适应屏幕大小
            eig_vec1 = eig_vecs[:, 0]
            eig_vec2 = eig_vecs[:, 1]
            vec1 = Vector(eig_vec1, color=RED).scale(2 / np.linalg.norm(eig_vec1))
            vec2 = Vector(eig_vec2, color=GREEN).scale(2 / np.linalg.norm(eig_vec2))

            # 特征值文本
            eig_val_text1 = MathTex(f"({eig_vals[0]:.2f})").next_to(vec1.get_end(), UP)
            eig_val_text2 = MathTex(f"({eig_vals[1]:.2f})").next_to(vec2.get_end(), UP)

            # 显示初始特征向量及其坐标
            vec1_label = MathTex(f"[{eig_vec1[0]:.2f},{eig_vec1[1]:.2f}]").next_to(vec1.get_end(), RIGHT)
            vec2_label = MathTex(f"[{eig_vec2[0]:.2f},{eig_vec2[1]:.2f}]").next_to(vec2.get_end(), RIGHT)

            self.play(GrowArrow(vec1), Write(vec1_label), GrowArrow(vec2), Write(vec2_label))
            self.wait(1)
            self.play(Write(eig_val_text1), Write(eig_val_text2))
            self.wait(1)

            # 根据矩阵和特征值缩放特征向量
            scaled_vec1 = vec1.copy().scale(eig_vals[0])
            scaled_vec2 = vec2.copy().scale(eig_vals[1])

            # 显示变换后的特征向量及其坐标
            scaled_vec1_label = MathTex(f"[{scaled_vec1.get_end()[0]:.2f},{scaled_vec1.get_end()[1]:.2f}]").next_to(scaled_vec1.get_end(), RIGHT)
            scaled_vec2_label = MathTex(f"[{scaled_vec2.get_end()[0]:.2f},{scaled_vec2.get_end()[1]:.2f}]").next_to(scaled_vec2.get_end(), RIGHT)

            self.play(
                Transform(vec1, scaled_vec1),
                Transform(vec2, scaled_vec2),
                Transform(vec1_label, scaled_vec1_label),
                Transform(vec2_label, scaled_vec2_label),
                run_time=2
            )

            # 展示整个坐标系的变换效果
            transformed_plane = plane.copy().apply_matrix(matrix)
            self.play(Transform(plane, transformed_plane), run_time=2)
            self.wait(1)

            # 保持变换后的特征向量（伸缩后）不变，展示它们没有旋转
            self.add(scaled_vec1, scaled_vec2, scaled_vec1_label, scaled_vec2_label)
            self.wait(1)

    # 渲染场景
    scene = EigenTransformation()
    scene.render()
    
    # 重置输出文件名配置
    config.output_file = None
    
    return target_video_path
