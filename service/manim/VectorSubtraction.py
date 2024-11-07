import sys
import json
import numpy as np
from manim import *

class VectorSubtraction(Scene):
    def construct(self):
        # 获取输入的向量并转换为 numpy 数组
        with open('vector_inputs.json', 'r') as file:
            data = json.load(file)
        vec1 = np.array([data['vec1_x'], data['vec1_y'], 0])
        vec2 = np.array([data['vec2_x'], data['vec2_y'], 0])

        # 计算结果向量
        result_vec = vec1 - vec2

        # 设置坐标系
        x_max = max(6, np.max(np.abs([vec1[0], vec2[0], result_vec[0]])) + 2)
        y_max = max(6, np.max(np.abs([vec1[1], vec2[1], result_vec[1]])) + 2)
        axes = Axes(
            x_range=[-1, x_max, 1],
            y_range=[-1, y_max, 1],
            axis_config={"color": BLUE, "include_numbers": True},
            x_axis_config={"numbers_to_include": np.arange(-1, x_max + 1, 1)},
            y_axis_config={"numbers_to_include": np.arange(-1, y_max + 1, 1)},
            tips=True,
        )

        # 创建并添加网格线
        self.add(axes)
        self.add(*[self.create_grid_line(axes, i, vertical=True) for i in
                   np.arange(-1, x_max + 1, 1)])
        self.add(*[self.create_grid_line(axes, i, vertical=False) for i in
                   np.arange(-1, y_max + 1, 1)])

        # 创建向量箭头
        vector_1 = Arrow(axes.c2p(0, 0), axes.c2p(vec1[0], vec1[1]), buff=0, color=YELLOW)
        vector_2 = Arrow(axes.c2p(0, 0), axes.c2p(vec2[0], vec2[1]), buff=0, color=GREEN)
        result_vector = Arrow(axes.c2p(0, 0), axes.c2p(result_vec[0], result_vec[1]), buff=0, color=RED)

        # 标注向量
        label_1 = MathTex(r"\vec{v}_1").next_to(vector_1.get_end(), RIGHT).set_color(YELLOW)
        label_2 = MathTex(r"\vec{v}_2").next_to(vector_2.get_end(), UP).set_color(GREEN)
        result_label = MathTex(r"\vec{v}_1 - \vec{v}_2").next_to(result_vector.get_end(), RIGHT).set_color(RED)

        # 动画显示
        self.play(Create(axes))
        self.play(GrowArrow(vector_1), Write(label_1))
        self.play(GrowArrow(vector_2), Write(label_2))
        self.wait(1)

        #结果向量的重点
        result_vec = vec1 - vec2

        #结构向量
        result_vec_end= axes.c2p(vec1[0], vec1[1])  # vector_1 的终点
        result_vec_start= axes.c2p(vec2[0], vec2[1])  # 向量和的终点
        result_vec_moved = Arrow(result_vec_start, result_vec_end, buff=0, color=GREEN)

        # 绘制结果向量
        self.play(GrowArrow(result_vec_moved), Write(result_label))
        self.wait(2)

        # 保持画面
        self.wait(2)
    def get_input_vectors(self):
        """
        从 JSON 文件获取用户输入的两个二维向量，并转换为 numpy 数组。
        """
        with open('vector_inputs.json', 'r') as file:
            data = json.load(file)

        vec1 = np.array([data['vec1_x'], data['vec1_y'], 0])
        vec2 = np.array([data['vec2_x'], data['vec2_y'], 0])

        return vec1, vec2

    def create_grid_line(self, axes, position, vertical=True):
        if vertical:
            start_point = axes.c2p(position, axes.y_range[0])
            end_point = axes.c2p(position, axes.y_range[1])
        else:
            start_point = axes.c2p(axes.x_range[0], position)
            end_point = axes.c2p(axes.x_range[1], position)

        return DashedLine(start_point, end_point, color=LIGHT_GRAY, stroke_width=1, dash_length=0.1).set_opacity(0.5)

    @staticmethod
    def get_dynamic_axis_range(vec1, vec2, base_range=6):
        max_x = max(abs(vec1[0]), abs(vec2[0]))
        max_y = max(abs(vec1[1]), abs(vec2[1]))
        max_val = max(max_x, max_y)

        if max_val > base_range:
            scale = max_val / base_range
            max_range = max_val + 2
            step = scale
        else:
            max_range = base_range
            step = 1

        return [-1, max_range, step]
