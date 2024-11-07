# Rotation.py
import sys
import argparse

from manim import *
import numpy as np


def reflect_vector(vector_coords, reflect_axis):
    """
    根据反射轴计算向量的翻折结果。
    :param vector_coords: 输入的二维向量 [x, y]
    :param reflect_axis: 翻折的坐标轴 ('x', 'y', 'origin')
    :return: 翻折后的向量
    """
    if reflect_axis == 'x':
        reflection_matrix = [[1, 0], [0, -1]]  # 沿 x 轴翻折的矩阵
    elif reflect_axis == 'y':
        reflection_matrix = [[-1, 0], [0, 1]]  # 沿 y 轴翻折的矩阵
    elif reflect_axis == 'origin':
        reflection_matrix = [[-1, 0], [0, -1]]  # 相对于原点对称的矩阵
    else:
        raise ValueError("Invalid reflect_axis, must be 'x', 'y' or 'origin'")

    # 计算翻折后的向量
    reflected_vector_coords = [
        reflection_matrix[0][0] * vector_coords[0] + reflection_matrix[0][1] * vector_coords[1],
        reflection_matrix[1][0] * vector_coords[0] + reflection_matrix[1][1] * vector_coords[1]
    ]
    return reflected_vector_coords


# 创建 Manim 动画
class ReflectionAnimation(Scene):
    def construct(self):
        # 使用 argparse 解析命令行参数
        parser = argparse.ArgumentParser()
        parser.add_argument("vector_x", type=float, help="向量的X坐标")
        parser.add_argument("vector_y", type=float, help="向量的Y坐标")
        parser.add_argument("reflect_axis", type=str, help="反射轴 ('x', 'y', 'origin')")

        # 手动过滤掉不需要的参数，只保留自定义参数
        filtered_args = sys.argv[sys.argv.index("Rotation.py") + 1:]

        # 解析自定义参数
        args = parser.parse_args(filtered_args)

        # 获取参数
        vector_coords = [args.vector_x, args.vector_y]
        reflect_axis = args.reflect_axis

        # 后续逻辑保持不变
        reflected_coords = reflect_vector(vector_coords, reflect_axis)

        # Step 1: 创建二维坐标系
        plane = NumberPlane(x_range=[-7, 7], y_range=[-7, 7])
        self.play(Create(plane))

        # Step 2: 创建初始向量
        vector = Arrow(start=ORIGIN, end=[*vector_coords, 0], buff=0, color=BLUE)
        self.play(GrowArrow(vector))
        self.wait(1)

        # Step 3: 展示反射操作
        if reflect_axis == 'x':
            reflection_text = Text("沿 x 轴翻折").move_to(UP * 3)
        elif reflect_axis == 'y':
            reflection_text = Text("沿 y 轴翻折").move_to(UP * 3)
        elif reflect_axis == 'origin':
            reflection_text = Text("相对于原点对称").move_to(UP * 3)

        self.play(Write(reflection_text))

        # Step 4: 创建翻折后的向量
        reflected_vector = Arrow(start=ORIGIN, end=[*reflected_coords, 0], buff=0, color=GREEN)

        # Step 5: 展示翻折后的向量变化
        self.play(Transform(vector, reflected_vector))
        self.wait(2)

        # Step 6: 清除动画
        self.play(FadeOut(reflection_text), FadeOut(plane), FadeOut(vector))


# 生成 Manim 动画
