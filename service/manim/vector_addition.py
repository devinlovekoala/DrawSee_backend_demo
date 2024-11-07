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

        # 创建两个向量，使用坐标轴的原点作为起点
        vector_1 = Arrow(axes.c2p(0, 0), axes.c2p(vec1[0], vec1[1]), buff=0, color=YELLOW)
        vector_2 = Arrow(axes.c2p(0, 0), axes.c2p(vec2[0], vec2[1]), buff=0, color=GREEN)

        # 标注向量
        label_1 = MathTex(r"\vec{v}_1").next_to(vector_1.get_end(), RIGHT).set_color(YELLOW)
        label_2 = MathTex(r"\vec{v}_2").next_to(vector_2.get_end(), UP).set_color(GREEN)

        # 计算结果向量
        result_vec = vec1 + vec2

        # 创建结果向量
        result_vector = Arrow(axes.c2p(0, 0), axes.c2p(result_vec[0], result_vec[1]), buff=0, color=RED)
        result_label = MathTex(r"\vec{v}_1 + \vec{v}_2").next_to(result_vector.get_end(), RIGHT).set_color(RED)

        # 把 v2 平移到 v1 的末端以展示相加过程
        vector_2_start = axes.c2p(vec1[0], vec1[1])  # vector_1 的终点
        vector_2_end = axes.c2p(result_vec[0], result_vec[1])  # 向量和的终点
        vector_2_moved = Arrow(vector_2_start, vector_2_end, buff=0, color=GREEN)

        # 动画顺序：绘制网格 -> 绘制坐标系 -> 绘制 v1 -> 绘制 v2 -> 移动 v2 -> 绘制结果向量
        self.play(Create(axes))
        self.play(GrowArrow(vector_1), Write(label_1))
        self.play(GrowArrow(vector_2), Write(label_2))
        self.wait(1)

        # 平移向量 v2
        self.play(Transform(vector_2, vector_2_moved))
        self.wait(1)

        # 绘制结果向量
        self.play(GrowArrow(result_vector), Write(result_label))
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
