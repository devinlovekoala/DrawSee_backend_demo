from manim import *


#manim -pql LinearTransformation.py LinearTransformationComplete
class LinearTransformationComplete(Scene):
    def construct(self):
        # Step 1: 创建二维坐标系
        plane = NumberPlane(x_range=[-7, 7], y_range=[-7, 7])
        self.play(Create(plane))

        # Step 2: 创建初始向量
        vector = Arrow(start=ORIGIN, end=[2, 1,0], buff=0, color=BLUE)
        self.play(GrowArrow(vector))
        self.wait(1)

        # Step 3: 说明缩放（Scaling）
        scaling_text = Text("缩放").move_to(UP*3)
        self.play(Write(scaling_text))

        # 缩放变换：将向量扩大 2 倍
        scaling_matrix = [[2, 0], [0, 2]]
        self.apply_matrix(scaling_matrix, vector, plane)
        self.wait(1)

        # 移除缩放文字
        self.play(FadeOut(scaling_text))

        # Step 4: 说明旋转（Rotation）
        rotation_text = Text("旋转").move_to(UP*3)
        self.play(Write(rotation_text))

        # 旋转变换：旋转 45 度
        rotation_matrix = [[0.707, -0.707], [0.707, 0.707]]  # 45度旋转矩阵
        self.apply_matrix(rotation_matrix, vector, plane)
        self.wait(1)

        # 移除旋转文字
        self.play(FadeOut(rotation_text))

        # Step 5: 说明反射（Reflection）
        reflection_text = Text("反射").move_to(UP * 3)
        self.play(Write(reflection_text))

        # 反射变换：相对于 y 轴
        reflection_matrix = [[-1, 0], [0, 1]]  # 相对于 y 轴的反射
        self.apply_matrix(reflection_matrix, vector, plane)
        self.wait(1)

        # 移除反射文字
        self.play(FadeOut(reflection_text))

        # Step 6: 说明剪切（Shear）
        shear_text = Text("剪切").move_to(UP*3)
        self.play(Write(shear_text))

        # 剪切变换
        shear_matrix = [[1, 1], [0, 1]]  # x 方向的剪切
        self.apply_matrix(shear_matrix, vector, plane)
        self.wait(1)

        # 移除剪切文字
        self.play(FadeOut(shear_text))

        # Step 7: 说明复合变换（Combination of Transformations）
        self.play(Transform(Text("剪切"), Text("复合变换").move_to(UP * 3)))

        # 复合变换：旋转 + 缩放
        combined_matrix = np.dot(scaling_matrix, rotation_matrix)
        self.apply_matrix(combined_matrix, vector, plane)
        self.wait(1)

        # 完成所有动画
        self.play(FadeOut(plane), FadeOut(vector), FadeOut(Text("复合变换")))

    # 应用矩阵到向量和坐标系的方法
    def apply_matrix(self, matrix, vector, plane):
        self.play(
            plane.animate.apply_matrix(matrix),
            vector.animate.apply_matrix(matrix),
            run_time=2
        )
