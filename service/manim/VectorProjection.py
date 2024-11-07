import sys
import json
import numpy as np
from manim import *

class VectorProjection(Scene):
    def construct(self):
        # 获取输入的向量并转换为 numpy 数组
        with open('vector_inputs.json', 'r') as file:
            data = json.load(file)
        vec1 = np.array([data['vec1_x'], data['vec1_y'], 0])
        vec2 = np.array([data['vec2_x'], data['vec2_y'], 0])

        # 转换 numpy 类型为 Python 标准类型
        vec1_x = vec1[0].item()
        vec1_y = vec1[1].item()
        vec2_x = vec2[0].item()
        vec2_y = vec2[1].item()

        # 获取坐标轴范围
        x_max = max(6, vec1_x + vec2_x + 2)
        y_max = max(6, vec1_y + vec2_y + 2)

        # 设置坐标系
        axes = Axes(
            x_range=[-1, x_max, 1],
            y_range=[-1, y_max, 1],
            axis_config={"color": BLUE, "include_numbers": True},
            x_axis_config={"numbers_to_include": np.arange(-1, x_max + 1, 1)},
            y_axis_config={"numbers_to_include": np.arange(-1, y_max + 1, 1)},
            tips=True,
        )

        # 创建并添加网格线
        self.add(*[self.create_grid_line(axes, i, vertical=True) for i in
                   np.arange(-1, x_max + 1, 1)])
        self.add(*[self.create_grid_line(axes, i, vertical=False) for i in
                   np.arange(-1, y_max + 1, 1)])

        # 创建矩阵 A 作为线性变换
        A = np.array([[1, 2], [3, 4]])

        # 创建原始向量 v1 和 v2，使用坐标轴的原点作为起点
        vector_1 = Arrow(axes.c2p(0, 0), axes.c2p(vec1[0], vec1[1]), buff=0, color=YELLOW)
        vector_2 = Arrow(axes.c2p(0, 0), axes.c2p(vec2[0], vec2[1]), buff=0, color=GREEN)

        # 标注向量 v1 和 v2
        label_1 = MathTex(r"\vec{v}_1").next_to(vector_1.get_end(), RIGHT).set_color(YELLOW)
        label_2 = MathTex(r"\vec{v}_2").next_to(vector_2.get_end(), UP).set_color(GREEN)

        # 计算线性变换后的向量 A * v1 和 A * v2
        transformed_vec1 = A @ vec1[:2]  # 只使用二维部分进行线性变换
        transformed_vec2 = A @ vec2[:2]

        # 创建变换后的向量
        transformed_vector_1 = Arrow(axes.c2p(0, 0), axes.c2p(transformed_vec1[0], transformed_vec1[1]), buff=0, color=RED)
        transformed_vector_2 = Arrow(axes.c2p(0, 0), axes.c2p(transformed_vec2[0], transformed_vec2[1]), buff=0, color=BLUE)

        # 标注变换后的向量
        transformed_label_1 = MathTex(r"A \vec{v}_1").next_to(transformed_vector_1.get_end(), RIGHT).set_color(RED)
        transformed_label_2 = MathTex(r"A \vec{v}_2").next_to(transformed_vector_2.get_end(), UP).set_color(BLUE)

        # 动画顺序：绘制坐标系 -> 绘制原始向量 -> 线性变换 -> 绘制变换后的向量
        self.play(Create(axes))
        self.play(GrowArrow(vector_1), Write(label_1))
        self.play(GrowArrow(vector_2), Write(label_2))
        self.wait(1)

        # 展示线性变换，将 v1 和 v2 变换为 A*v1 和 A*v2
        self.play(Transform(vector_1, transformed_vector_1), Transform(label_1, transformed_label_1))
        self.play(Transform(vector_2, transformed_vector_2), Transform(label_2, transformed_label_2))
        self.wait(2)

    def create_grid_line(self, axes, position, vertical=True):
        if vertical:
            start_point = axes.c2p(position, axes.y_range[0])
            end_point = axes.c2p(position, axes.y_range[1])
        else:
            start_point = axes.c2p(axes.x_range[0], position)
            end_point = axes.c2p(axes.x_range[1], position)

        return DashedLine(start_point, end_point, color=LIGHT_GRAY, stroke_width=1, dash_length=0.1).set_opacity(0.5)

    def get_input_vectors(self):
        """
        从 JSON 文件获取用户输入的两个二维向量，并转换为 numpy 数组。
        """
        with open('vector_inputs.json', 'r') as file:
            data = json.load(file)

        vec1 = np.array([data['vec1_x'], data['vec1_y'], 0])
        vec2 = np.array([data['vec2_x'], data['vec2_y'], 0])

        return vec1, vec2
