from manim import *


#manim -pql Scaling.py ScalingTransformation

class ScalingTransformation(Scene):
    def __init__(self, vector_coords=[2, 1], scale_factor=2, **kwargs):
        super().__init__(**kwargs)
        self.vector_coords = vector_coords  # 自定义向量坐标
        self.scale_factor = scale_factor  # 缩放比例

    def construct(self):
        # Step 1: 创建二维坐标系
        plane = NumberPlane(x_range=[-7, 7], y_range=[-7, 7])
        self.play(Create(plane))

        # Step 2: 创建初始向量
        vector = Arrow(start=ORIGIN, end=[*self.vector_coords, 0], buff=0, color=BLUE)
        self.play(GrowArrow(vector))
        self.wait(1)

        # Step 3: 说明缩放因子
        scaling_text = Text(f"放大或缩小：{self.scale_factor}").move_to(UP * 3)
        self.play(Write(scaling_text))

        # Step 4: 计算缩放后的向量终点
        scaled_vector_coords = [self.scale_factor * x for x in self.vector_coords]
        scaled_vector = Arrow(start=ORIGIN, end=[*scaled_vector_coords, 0], buff=0, color=GREEN)

        # Step 5: 展示缩放后的向量变化
        self.play(Transform(vector, scaled_vector))
        self.wait(2)

        # Step 6: 清除动画
        self.play(FadeOut(scaling_text), FadeOut(plane), FadeOut(vector))

    # 应用矩阵到向量和坐标系
    def apply_matrix(self, matrix, vector, plane):
        self.play(
            plane.animate.apply_matrix(matrix),
            vector.animate.apply_matrix(matrix),
            run_time=2
        )
