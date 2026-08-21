from math import pi
import flet as ft
import flet.canvas as cv


class SemicircleProgress:
    def __init__(self):

        self.uv_index = 0 # Initially 0, but it will be able to change later with a setter
        self._max_uv = 13
        self.progress = self.uv_index / self._max_uv

        self._stops = [ # gradient colors
            (0, (0, 216, 63)),  # Green
            (3, (255, 255, 0)),  # Yellow
            (6, (255, 153, 0)),  # Orange
            (9, (255, 0, 0)),  # Red
            (13, (222, 0, 0)),  # Dark Red
        ]

        self._size = 180 # Semicircle width
        self._stroke = 16 # Semicircle thickness


        self.build_semicircle()

    def set_index(self, uv):
        self.uv_index = uv
        self.progress = self.uv_index / self._max_uv

        self.build_semicircle()





    def __lerp_color(self, c1, c2, t):
        # linear interpolation to get the middle color between to main colors
        return tuple(
            int(c1[i] + (c2[i] - c1[i]) * t)
            for i in range(3)
        )

    def __rgb_to_hex(self, rgb):
        # rgb to hex converter
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def __uv_to_color(self, uv, stops):
        # Defines the UV value and interpolates the colors
        for i in range(len(stops) - 1):
            u1, c1 = stops[i]
            u2, c2 = stops[i + 1]
            if uv <= u2:
                t = (uv - u1) / (u2 - u1)
                return self.__lerp_color(c1, c2, t)

        return stops[-1][1]



    def build_semicircle(self):

        # background no progress
        self.bg_paint = ft.Paint(
            style=ft.PaintingStyle.STROKE,
            stroke_width=self._stroke,
            color='#616161',
            stroke_cap=ft.StrokeCap.ROUND,
            stroke_join=ft.StrokeJoin.ROUND
        )

        # arc creation

        self._arc_segments = []
        self._segments = 120

        self.color = 'FFFFFF'

        for i in range(self._segments):
            start_uv = self._max_uv * i / self._segments
            end_uv = self._max_uv * (i + 1) / self._segments
            if end_uv > self.uv_index:
                end_uv = self.uv_index
            # Arc proportion
            start_prop = start_uv / self._max_uv
            end_prop = end_uv / self._max_uv
            if start_prop >= self.progress:
                break
            # Gradient color for the current segment
            rgb = self.__uv_to_color((start_uv + end_uv) / 2, self._stops)
            self.color = self.__rgb_to_hex(rgb)

            seg_paint = ft.Paint(
                style=ft.PaintingStyle.STROKE,
                stroke_width=self._stroke,
                color=self.color,
                stroke_cap=ft.StrokeCap.ROUND,
                stroke_join=ft.StrokeJoin.ROUND
            )
            start_angle = pi + pi * start_prop
            sweep_angle = pi * (end_prop - start_prop)
            self._arc_segments.append(
                cv.Arc(
                    x=(self._stroke / 2),
                    y=(self._stroke / 2),
                    width=self._size - self._stroke,
                    height=self._size - self._stroke,
                    start_angle=start_angle,
                    sweep_angle=sweep_angle,
                    use_center=False,
                    paint=seg_paint,
                )
            )

        # Добавляем серую дугу для всего фона
        self.shapes = [
                     cv.Arc(
                         x=(self._stroke / 2),
                         y=(self._stroke / 2),
                         width=self._size - self._stroke,
                         height=self._size - self._stroke,
                         start_angle=pi,
                         sweep_angle=pi,
                         use_center=False,
                         paint=self.bg_paint,

                     ),
                 ] + self._arc_segments

        gauge = cv.Canvas(
            shapes=self.shapes,
            width=self._size,
            height=self._size,
        )

        self.progress_bar = ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Container(
                    content=gauge,
                    width=self._size,
                    height=self._size // 2 + self._stroke // 2,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                ),
                ft.Container(
                    content=ft.Text(f"{self.uv_index}", size=36, weight=ft.FontWeight.W_700),
                    padding=ft.Padding(top=-42),
                    alignment=ft.Alignment.CENTER,
                ),
            ],
        )










