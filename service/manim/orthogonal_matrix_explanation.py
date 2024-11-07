#正交矩阵的讲解视频
from manim import *


class OrthogonalMatrixExplanation(Scene):
    def construct(self):
        # 设置场景背景为白色
        self.camera.background_color = BLACK

        # 创建标题
        title = Text("正交矩阵的讲解", font_size=50).to_edge(UP)
        self.play(Write(title))
        self.wait(2)

        # 创建正交矩阵的定义
        definition_text = Text("正交矩阵是满足以下条件的方阵：", font_size=30).next_to(title, DOWN)
        self.play(Write(definition_text))
        self.wait(2)

        # 创建正交矩阵的数学表达式
        formula = MathTex(r"A^T A = I", font_size=40).next_to(definition_text, DOWN)
        self.play(Write(formula))
        self.wait(3)

        # 创建解释正交矩阵的文本
        explanation_text = Text(r"其中，(A^T) 表示 (A) 的转置，(I) 是单位矩阵。", font_size=30).next_to(formula, DOWN)

        self.play(Write(explanation_text))
        self.wait(3)

        # 创建正交矩阵的性质的标题
        properties_title = Text("正交矩阵的性质：", font_size=30).next_to(explanation_text, DOWN)
        self.play(Write(properties_title))
        self.wait(2)

        # 创建正交矩阵的性质列表
        properties_list = [
            ("1. 行列式的值为 &plusmn;1", DOWN),
            ("2. 逆矩阵等于转置矩阵", DOWN),
            ("3. 保持向量长度不变", DOWN),
            ("4. 保持向量之间的夹角不变", DOWN),
        ]
        temp=properties_title
        for prop, direction in properties_list:
            property_text = Text(prop, font_size=24).next_to(temp, direction)
            self.play(Write(property_text))
            self.wait(2)
            temp=property_text

        # # 创建结束语的文本
        # conclusion_text = Text("正交矩阵在几何和物理中有广泛应用。", font_size=30).next_to(property_text, DOWN)
        # self.play(Write(conclusion_text))
        # self.wait(2)

        # 清除屏幕上的所有元素
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)

        # 显示结束画面
        end_screen = Text("感谢观看！", font_size=50).to_edge(DOWN)
        self.play(Write(end_screen))
        self.wait(2)

# 如果你想要渲染这个场景，你需要运行以下命令
# manim -pql orthogonal_matrix_explanation.py OrthogonalMatrixExplanation
