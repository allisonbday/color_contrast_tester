# %%
from PIL import ImageColor
from colour import Color
import itertools


class ColorContrastGenerator:
    def get_luminance(color: Color) -> float:
        """_summary_

        Calculate the relative luminance of the supplied color.
        Source: https://github.com/ZugBahnHof/color-contrast/blob/main/color_contrast/contrast.py

        Args:
            color (Color): Color (HEX)

        Returns:
            float: luminance value
        """

        color = Color(color)

        RsRGB, GsRGB, BsRGB = color.get_rgb()

        R = RsRGB / 12.92 if RsRGB <= 0.04045 else ((RsRGB + 0.055) / 1.055) ** 2.4
        G = GsRGB / 12.92 if GsRGB <= 0.04045 else ((GsRGB + 0.055) / 1.055) ** 2.4
        B = BsRGB / 12.92 if BsRGB <= 0.04045 else ((BsRGB + 0.055) / 1.055) ** 2.4

        luminance = 0.2126 * R + 0.7152 * G + 0.0722 * B

        return luminance

    def get_contrast_ratio(color1: Color, color2: Color) -> float:
        """_summary_

        Calculate the contrast ratio between two colors.
        Source: https://github.com/ZugBahnHof/color-contrast/blob/main/color_contrast/contrast.py

        Args:
            color1 (Color): first color
            color2 (Color): second color

        Returns:
            float: contrast ratio
        """

        L1 = ColorContrastGenerator.get_luminance(color1)
        L2 = ColorContrastGenerator.get_luminance(color2)

        ratio = (L1 + 0.05) / (L2 + 0.05)
        ratio_i = (L2 + 0.05) / (L1 + 0.05)

        return round(max(ratio, ratio_i), 2)

    def all_palette_combos(palette: list) -> list:
        """_summary_

        Generate all possible combinations of colors in the palette.
        """

        return list(itertools.combinations(palette, 2))

    def all_palette_results(color_palette: list) -> list:
        """


        Args:
            palette (list): _description_

        Returns:
            list: _description_
        """
        all_results = []

        for pair in ColorContrastGenerator.all_palette_combos(color_palette):
            color1 = pair[0]
            color2 = pair[1]
            contrast_ratio = ColorContrastGenerator.get_contrast_ratio(color1, color2)

            all_results.append(
                {"color1": color1, "color2": color2, "contrast_ratio": contrast_ratio}
            )

        return all_results

    AccessibilityLevel = {
        "AA": 4.5,
        "AAA": 7.0,
        "AA Large": 3.0,
        "AAA Large": 4.5,
    }

    def get_accessibility_levels(contrast_ratio) -> str:
        return [
            {level: contrast_ratio >= size}
            for level, size in ColorContrastGenerator.AccessibilityLevel.items()
        ]


# # %%
# # CHECKS
# print(ColorContrastGenerator.get_contrast_ratio("#000000", "#ffffff"))  # 21.0
# print(ColorContrastGenerator.get_contrast_ratio("#506C60", "#C06145"))  # 1.38
# print(ColorContrastGenerator.get_contrast_ratio("#506C60", "#F8E3D2"))  # 4.63
# print(ColorContrastGenerator.get_contrast_ratio("#183425", "#F8E3D2"))  # 10.86


# color_palette = ["#506C60", "#C06145", "#DDBFA7", "#F8E3D2", "#183425"]
# ColorContrastGenerator.all_palette_combos(color_palette)

# ColorContrastGenerator.get_accessibility_levels(4.5)


# all_results = []

# for pair in ColorContrastGenerator.all_palette_combos(color_palette):
#     color1 = pair[0]
#     color2 = pair[1]
#     contrast_ratio = ColorContrastGenerator.get_contrast_ratio(color1, color2)

#     all_results.append(
#         {"color1": color1, "color2": color2, "contrast_ratio": contrast_ratio}
#     )
#     print(f"Contrast ratio between {color1} and {color2}: {contrast_ratio}")

# # %%
# all_results
