from manim import *
import os
import numpy as np

def sanitize_filename(filename):
    """移除或替换文件名中的非法字符"""
    return "".join(c if c.isalnum() or c in '._-' else '_' for c in filename)

def Schmidt_trans(v1, v2, v3):
    config.media_dir = os.path.join(os.getcwd(), 'static')
    config.pixel_height = 446
    config.pixel_width = 386

    # 生成唯一的视频文件名
    sanitized_v1 = sanitize_filename(str(v1))
    sanitized_v2 = sanitize_filename(str(v2))
    sanitized_v3 = sanitize_filename(str(v3))
    video_filename = f'SchmidtTransformation_{sanitized_v1}_{sanitized_v2}_{sanitized_v3}.mp4'
    output_video_dir = os.path.join(config.media_dir, 'videos', '446p60', 'cache', 'SchmidtTransformation')
    os.makedirs(output_video_dir, exist_ok=True)
    
    target_video_path = os.path.join(output_video_dir, video_filename)

    # 如果视频文件已存在，则直接返回路径
    if os.path.exists(target_video_path):
        return target_video_path

    # 动态设置输出文件名
    config.output_file = target_video_path

    class SchmidtTransformation(ThreeDScene):
        def construct(self):
            self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

            axes = (
                ThreeDAxes(
                    x_length=15,
                    y_length=15,
                    z_length=15,
                    axis_config={"include_numbers": True}
                )
                .add_coordinates()
                .set_color(GREY)
            )
            self.add(axes)

            vector_v1 = Arrow(start=ORIGIN, end=v1, color=BLUE)
            vector_v2 = Arrow(start=ORIGIN, end=v2, color=RED)
            vector_v3 = Arrow(start=ORIGIN, end=v3, color=GREEN)

            self.play(Create(vector_v1), Create(vector_v2), Create(vector_v3))
            self.wait(2)

            # 正交化过程
            u1 = v1
            proj_v2_on_u1 = np.dot(v2, u1) / np.dot(u1, u1) * u1
            u2 = v2 - proj_v2_on_u1

            proj_v3_on_u1 = np.dot(v3, u1) / np.dot(u1, u1) * u1
            proj_v3_on_u2 = np.dot(v3, u2) / np.dot(u2, u2) * u2
            u3 = v3 - proj_v3_on_u1 - proj_v3_on_u2

            vector_u2 = Arrow(start=ORIGIN, end=u2, color=YELLOW)
            vector_u3 = Arrow(start=ORIGIN, end=u3, color=PURPLE)

            self.play(Transform(vector_v2, vector_u2), Transform(vector_v3, vector_u3))
            self.wait(2)

            e1 = u1 / np.linalg.norm(u1)
            e2 = u2 / np.linalg.norm(u2)
            e3 = u3 / np.linalg.norm(u3)

            vector_e1 = Arrow(start=ORIGIN, end=e1, color=BLUE)
            vector_e2 = Arrow(start=ORIGIN, end=e2, color=YELLOW)
            vector_e3 = Arrow(start=ORIGIN, end=e3, color=PURPLE)

            self.play(Transform(vector_v1, vector_e1), Transform(vector_v2, vector_e2), Transform(vector_v3, vector_e3))

        def setup(self):
            Scene.setup(self)
            self.camera.frame_width = 12.0
            self.camera.frame_height = (config.pixel_height / config.pixel_width) * self.camera.frame_width

    # 渲染场景
    scene = SchmidtTransformation()
    scene.render()

    # 重置输出文件名配置
    config.output_file = None
    
    return target_video_path
