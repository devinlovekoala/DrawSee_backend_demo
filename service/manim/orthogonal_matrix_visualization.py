#成功 实二次型及其矩阵表示
from manim import *

class RealQuadraticForm(Scene):
    def construct(self):
        # 创建标题
        title = Text("实二次型及其矩阵表示", font_size=50).to_edge(UP)

        # 创建一个二次型的例子
        quadratic_form = MathTex(r"Q(x, y) = ax^2 + bxy + cy^2")
        quadratic_form.next_to(title, DOWN)

        # 创建一个矩阵形式的例子
        matrix_form = MathTex(
            r"Q(x, y) = ",
            r"\begin{pmatrix} x & y \end{pmatrix} ",
            r"\begin{pmatrix} a & b/2 \\ b/2 & c \end{pmatrix} ",
            r"\begin{pmatrix} x \\ y \end{pmatrix}",
            substrings_to_isolate=[r"\begin{pmatrix} a & b/2 \\ b/2 & c \end{pmatrix}"]
        )

        # 展示标题
        self.play(Write(title))
        self.wait(1)

        # 展示二次型
        self.play(Write(quadratic_form))
        self.wait(2)

        # 展示从二次型到矩阵形式的转换
        self.play(TransformMatchingShapes(quadratic_form.copy(), matrix_form))
        self.wait(2)

        # 解释矩阵的意义
        explanation = Text("这是实二次型对应的矩阵，\n它表示了二次型的线性变换。")
        explanation.scale(0.75).next_to(matrix_form, DOWN)
        self.play(Write(explanation))
        self.wait(3)

        # 创建一个高亮矩形
        # 注意: 我们现在使用 matrix_form[2]，因为它包含了我们想要高亮的矩阵部分
        highlight_matrix = SurroundingRectangle(matrix_form[2], buff=0.1, color=YELLOW)
        self.play(Create(highlight_matrix))
        self.wait(2)

        # 结束场景
        self.play(FadeOut(title), FadeOut(matrix_form), FadeOut(explanation), FadeOut(highlight_matrix))

# 运行场景
if __name__ == "__main__":
    scene = RealQuadraticForm()
    scene.render()