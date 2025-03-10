# IMPORTS ---------------------------------------------------------------------
import os
import streamlit as st
from PIL import Image
from datetime import date, timedelta
import itertools
import re
import colorsys

import numpy as np
import pandas as pd

from streamlit_extras.stylable_container import stylable_container

# import from src
# path = os.path.dirname(__file__)
from functions.ColorContrastGenerator import ColorContrastGenerator


# PAGE SET UP -----------------------------------------------------------------

st.set_page_config(
    page_icon="🌈",
    page_title="F1 Custom Points System TESTING",
    # icon=":material/sports_motorsports:",
    # layout="wide",
    menu_items={
        # "Get Help": "",
        # 'Report a bug': "",
    },
)


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


hide_expander_border = """
<style>
[data-testid="stExpander"] details {
    border-style: none;
    }
</style>
"""

# VARIABLES -------------------------------------------------------------------

# CONSTANTS -------------------------------------------------------------------


color_palette = ["#1d190f", "#8d3427", "#daa99a", "#8c753b", "#ccd6d5"]
# https://www.pinterest.com/pin/774124930386098/ 🌠🌠🌠🌠


default_palettes = [
    {
        "p": ["#1d190f", "#8d3427", "#daa99a", "#8c753b", "#ccd6d5"],
        "cap": "tomato patch",
        "url": "https://www.pinterest.com/pin/774124930386098/",
    },
    {
        "p": ["#c5c0aa", "#7f3025", "#44201c", "#4d8a8b", "#83b8a2"],
        "cap": "summer night",
        "url": "https://www.pinterest.com/pin/6192518232003047/",
    },
    {
        "p": ["#442d1c", "#743014", "#84592b", "#9d9167", "#e8d1a7"],
        "cap": "autumn walk",
        "url": "https://www.pinterest.com/pin/585116176621379638/",
    },
    {
        "p": ["#1c172a", "#654bb0", "#ac78cb", "#bf79b6", "#aab1ad"],
        "cap": "purple haze",
        "url": "https://www.pinterest.com/pin/24558760464099841/",
    },
    {
        "p": ["#2c2c3b", "#633d43", "#d87c65", "#cfb881", "#e9969e"],
        "cap": "orange sunset",
        "url": "https://www.pinterest.com/pin/4292562139747347/",
    },
    {
        "p": ["#2c2c3b", "#F17105", "#D11149", "#6610F2", "#1A8FE3"],
        "cap": "bright lights",
        "url": "https://coolors.co/e6c229-f17105-d11149-6610f2-1a8fe3",
    },
    {
        "p": ["#606c38", "#283618", "#fefae0", "#dda15e", "#bc6c25"],
        "cap": "classic",
        "url": "https://coolors.co/palette/606c38-283618-fefae0-dda15e-bc6c25",
    },
    {
        "p": ["#252819", "#58421a", "#c68c3e", "#ffedd2", "#dce6e9", "#62807f"],
        "cap": "grand teton",
        "url": "https://www.pinterest.com/pin/37365871903237048/",
    },
    {
        "p": ["#353227", "#897e46", "#edd9b8", "#b3a8a2", "#f09560", "#c46d52"],
        "cap": "yosemite",
        "url": "https://www.pinterest.com/pin/778982066831467763/",
    },
    {
        "p": [
            "#35201B",
            "#ab482d",
            "#caa19c",
            "#7b786b",
            "#c17c3e",
            "#F9EBDD",
        ],
        "cap": "blood orange",
        "url": "https://www.pinterest.com/pin/68748393834/",
    },
    {
        "p": [
            "#274048",
            "#164d5c",
            "#258ea6",
            "#549f93",
            "#9faf90",
            "#deb1e2",
            # "#e2c2ff",
            "#EDF9F7",
        ],
        "cap": "pink dreams",
    },
]


# FUNCTIONS --------------------------------------------------------------------


def list_unique(palette):
    """Remove duplicate colors from the palette."""
    return list(dict.fromkeys(palette))


def convert_rgb_palette(palette):
    return [tuple(int(color[i : i + 2], 16) for i in (1, 3, 5)) for color in palette]


# ['#f8ff00', '#ff8300', '#ff0096', '#00d5ff', '#7cff00', '#e500ff', '#00ffd4', '#000000', '#0022ff', '#ff3b00']
def reorder_as_ombre(palette):
    """Reorder a list of hex colors to create an ombre effect."""

    # Convert hex to RGB
    rgb_palette = convert_rgb_palette(palette)

    # Convert RGB to HLS
    hls_palette = [
        colorsys.rgb_to_hls(*[x / 255.0 for x in color]) for color in rgb_palette
    ]

    # Sort by lightness (HLS[1]) and then by hue (HLS[0])
    hls_palette.sort(key=lambda x: (x[1], x[0]))

    # Convert back to RGB
    sorted_rgb_palette = [colorsys.hls_to_rgb(*color) for color in hls_palette]

    # Convert RGB back to hex
    sorted_palette = [
        "#{:02x}{:02x}{:02x}".format(
            int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
        )
        for color in sorted_rgb_palette
    ]

    return sorted_palette


def gen_palette_img(color_palette):

    # color_palette = list_unique(color_palette)

    max_width = 1000

    images = [
        Image.new("RGB", (int(max_width / len(color_palette)) + 1, 100), color=x)
        for x in color_palette
    ]

    new_im = Image.new("RGB", (max_width, 100))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return new_im


# PAGE CONTENT ----------------------------------------------------------------


# header
icon("🌈")
st.title("Color Contrast Checker")


# content
st.markdown(
    """
    This is to help you create a color palette that follows the AA & AAA guidelines for website accessibility.
    """
)


# inspiration palette

inspo_expander = st.expander(
    "**Inspiration Palettes**", expanded=False, icon=":material/auto_awesome:"
)
inspo_expander.markdown(hide_expander_border, unsafe_allow_html=True)

with inspo_expander:
    images = [gen_palette_img(color_palette["p"]) for color_palette in default_palettes]
    caps = [
        # color_palette["cap"] + f" [🔗]({color_palette['url']})"
        color_palette["cap"]
        for color_palette in default_palettes
    ]

    col1, col2 = st.columns([0.2, 0.8])

    with col1:
        st.markdown(
            """
        <style>
        [role=radiogroup]{
            gap: 1.35rem; padding-top: 1rem;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        pick_img = st.radio(
            "Inspo Palette",
            [x for x in range(len(images))],
            captions=caps,
        )

    color_palette_idx = pick_img
    color_palette = default_palettes[color_palette_idx]["p"]

    with col2:
        st.write("---")
        st.image(images)

    # ColorContrastGenerator


color_input = st.text_input("Import List, separate with commas (max 10)")

if color_input:

    # try:
    #     input_color_palette = eval(color_input)
    #     if not isinstance(color_palette, list):
    #         raise ValueError
    # except:

    # only accept letters, numbers and #,
    color_input = re.sub(r"[^a-zA-Z0-9 #,]", "", color_input)

    input_color_palette = [
        "#" + color
        for color in color_input.replace(" ", "#")
        .replace(",", "#")
        .replace("'", "#")
        .split("#")
        if color and color != "#"
    ]

    # only accept valid hex codes
    color_palette = list_unique(
        [
            color
            for color in input_color_palette
            if re.match(r"^#[0-9A-Fa-f]{6}$", color)
        ]
    )[:10]

    not_colors = list_unique(
        [
            color
            for color in input_color_palette
            if not re.match(r"^#[0-9A-Fa-f]{6}$", color)
        ]
    )

    if len(color_palette) < 2:
        color_palette += ["#000000", "#EAEAEA", "#FF0000"][: 2 - len(color_palette)]

    if input_color_palette != color_palette:
        st.write("your unique color palette:")
        st.code(color_palette)

    if not_colors:
        st.write("the following are not proper hex codes:")
        st.code(not_colors)

with st.container(border=True):

    st.markdown("### CUSTOM PALETTE")

    st.number_input(
        "Number of Colors",
        min_value=2,
        max_value=10,
        value=len(color_palette),
        key="color_nums",
        help="max 10",
    )

    color_picks = []
    cols = st.columns(st.session_state["color_nums"])
    for i, x in enumerate(cols):

        x.color_picker(
            key="color_picker" + str(i),
            label=f"Color {i+1}",
            value=color_palette[i % len(color_palette)],
        )

        color_picks.append("color_picker" + str(i))

# if st.button("run"):

# get the colors

color_palette = [st.session_state[x] for x in color_picks]

all_results = ColorContrastGenerator.all_palette_results(color_palette)

results = all_results

st.header("RESULTS")

# color_palette = reorder_as_ombre(color_palette)

# st.image(gen_palette_img(color_palette))
# st.image(gen_palette_img(reorder_as_ombre(color_palette)))


# filters

# filter_expander = st.expander("**Filter**", expanded=True)
# filter_expander.markdown(hide_expander_border, unsafe_allow_html=True)


results_filter = st.segmented_control(
    "",
    ["AAA (7)", "AA / AAA Large (4.5)", "AA Large (3)"],
    selection_mode="single",
)

if results_filter == "AA / AAA Large (4.5)":
    results = [x for x in all_results if x["contrast_ratio"] >= 4.5]

if results_filter == "AAA (7)":
    results = [x for x in all_results if x["contrast_ratio"] >= 7]

if results_filter == "AA Large (3)":
    results = [x for x in all_results if x["contrast_ratio"] >= 3]


# Get unique combinations of results
unique_results = []
seen_combinations = set()

for result in results:
    combo = tuple(sorted([result["color1"], result["color2"]]))
    if combo not in seen_combinations and result["color1"] != result["color2"]:
        seen_combinations.add(combo)
        unique_results.append(result)

results = unique_results


def levels(contrast_ratio):

    ret = [
        {"level": i, "pass": contrast_ratio >= x}
        for i, x in ColorContrastGenerator.AccessibilityLevel.items()
    ]

    return ret


it = 0


# all_results

# ColorContrastGenerator.AccessibilityLevel


line_expander = st.expander("**Line Check**")
line_expander.markdown(hide_expander_border, unsafe_allow_html=True)


box_expander = st.expander("**Box Check**", expanded=False)
box_expander.markdown(hide_expander_border, unsafe_allow_html=True)

if not results:
    line_expander.write("No combinations found")
    box_expander.write("No combinations found")
    color1 = color_palette[0]
    color2 = color_palette[1]

for c in results:

    with st.container():

        color1 = c["color1"]
        color2 = c["color2"]
        contrast_ratio = c["contrast_ratio"]
        color_names = "Color1" + " + " + "Color2"

        c1, c2, c3 = box_expander.columns(3)

        with c1:
            txt = f"background: {color1}, text: {color2} - Lorem ipsum dolor sit amet, consectetur adipiscing"
            line_expander.markdown(
                f"""
                <span style="line-height: 1px;padding: .5rem; background-color: {color1}; color: {color2};">{txt}</span> - {contrast_ratio}
                
                <span style="line-height: 1px;padding: .5rem; background-color: {color2}; color: {color1};">{txt}</span> - {contrast_ratio}
                """,
                unsafe_allow_html=True,
            )

            def color_font(color, txt="■"):
                return f"""<span style="color: {color}; -webkit-text-stroke: 1px black;">{txt}</span>"""

            # c1.markdown(
            #     str(color_font(color1, color1))
            #     + f"""<span style="font-size: 25px; line-height: 3.2rem; text-align: bottom; font-weight: bold; "> & </span>"""
            #     + str(color_font(color2, color2)),
            #     unsafe_allow_html=True,
            # )

            c1.markdown(
                f"""
                <span style="font-size: 19px; line-height: 3.2rem; text-align: center; font-weight: bold; text-transform: uppercase; text-align: center;line-height: 40px;"> {color1} {color_font(color1)} *&* {color2} {color_font(color2)}</span>
                """,
                unsafe_allow_html=True,
            )

            c1.table(
                pd.DataFrame(levels(contrast_ratio))
                .set_index("level")
                .replace({True: "✅", False: "❌"})
            )

        with c2:
            css_styles = f"""{{
                    background-color: {color1};
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    text-align: center;
                    padding-top: 1.5rem;
                    padding-bottom: 2rem;
                    line-height: 16px;
                    color: {color2};
                            .hex {{
                                line-height: 20px;
                                }}
                            .highlight {{
                                
                                }}
            }}"""

            with stylable_container(
                key="container_with_border" + str(it),
                css_styles=css_styles,
            ):
                st.markdown(
                    f"""                                                 
                    <span class="highlight" style="font-size: 25px;">**Contrast Ratio**</span>
                    
                    <span style="font-size: 50px;">{contrast_ratio}</span>
                    
                    <span class="hex" >
                    Background: {color1} 
                     
                    Text: {color2}
                    </span>
                    
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    """,
                    unsafe_allow_html=True,
                )

        with c3:
            css_styles = f"""{{
                    background-color: {color2};
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    text-align: center;
                    padding-top: 1.5rem;
                    padding-bottom: 2rem;
                    line-height: 16px;
                    color: {color1};
                            .hex {{
                                line-height: 20px;
                                }}
                            .highlight {{
                                
                                }}
            }}"""

            with stylable_container(
                key="container_with_border_ALT" + str(it),
                css_styles=css_styles,
            ):
                st.markdown(
                    f"""                                                 
                    <span class="highlight" style="font-size: 25px;">**Contrast Ratio**</span>
                    
                    <span style="font-size: 50px;">{contrast_ratio}</span>
                    
                    <span class="hex" >
                    Background: {color2} 

                    Text: {color1}
                    </span>
                    
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    """,
                    unsafe_allow_html=True,
                )

        it += 1


custom_expander = st.expander("**Custom Check**", expanded=True)
custom_expander.markdown(hide_expander_border, unsafe_allow_html=True)


def invert_bgtx():
    old_background = st.session_state["background_pill"]
    old_text = st.session_state["text_pill"]

    st.session_state["background_pill"] = old_text
    st.session_state["text_pill"] = old_background


with custom_expander:

    c1, c2, c3 = st.columns([0.45, 0.1, 0.45], gap="large")

    if "background_pill" not in st.session_state:
        st.session_state["background_pill"] = 1

    if "text_pill" not in st.session_state:
        st.session_state["text_pill"] = 2

    background_color_idx = color_palette.index(color1) + 1
    text_color_idx = color_palette.index(color2) + 1

    with c2:

        c2.markdown(
            """
            <style>
            div.stButton > button {
            display: block;
            margin: auto;
            position: relative;
            top: 50%;
            transform: translateY(150%);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        invert_button = c2.button(
            "",
            icon=":material/invert_colors:",
            on_click=invert_bgtx,
            use_container_width=True,
            type="tertiary",
            help="Invert colors",
        )

    background_color_idx = c1.pills(
        "Background Color",
        key="background_pill",
        options=range(1, len(color_palette) + 1),
        default=background_color_idx,
    )
    text_color_idx = c3.pills(
        "Text Color",
        key="text_pill",
        options=range(1, len(color_palette) + 1),
        default=text_color_idx,
    )

    # custom_text = st.text_area(
    #     "Custom Text",
    #     value="""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""",
    # )

    custom_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    background_color = (
        color_palette[background_color_idx - 1] if background_color_idx else "#ffffff"
    )
    text_color = color_palette[text_color_idx - 1] if text_color_idx else "#000000"
    contrast_ratio = ColorContrastGenerator.get_contrast_ratio(
        background_color, text_color
    )
    passed_standards = (
        ", ".join(
            i
            for i, x in ColorContrastGenerator.AccessibilityLevel.items()
            if x <= contrast_ratio
        )
        if any(
            x <= contrast_ratio
            for x in ColorContrastGenerator.AccessibilityLevel.values()
        )
        else "meets no standard"
    )
    missed_standards = (
        ", ".join(
            i
            for i, x in ColorContrastGenerator.AccessibilityLevel.items()
            if x >= contrast_ratio
        )
        if any(
            x >= contrast_ratio
            for x in ColorContrastGenerator.AccessibilityLevel.values()
        )
        else "passed all"
    )

    css_styles = f"""{{
                    background-color: {background_color};
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: 3rem;
                    line-height: 30px;
                    color: {text_color};
                    text-align: justify;
                    .hex {{
                        line-height: 10px;
                        }}
                    .highlight {{
                        line-height: 25px;
                        text-align: justify;
                        word-wrap: break-word;
                        # line-height: 20px;
                        padding-right: 8rem;
                        display: inline-block;
                        }}
            }}"""

    with stylable_container(
        key="custom_check",
        css_styles=css_styles,
    ):
        st.markdown(
            f"""                                                 
                <span class="highlight" style="font-size: 25px;">**Contrast Ratio**</span>
                
                <span style="font-size: 50px;">{contrast_ratio}</span>
                
                <span class="hex">
                Background: {background_color} 

                Text: {text_color}
                
                **Passes Standards: {passed_standards}**
                
                **Missed Standards: {missed_standards}**
                </span>
                
                
                <span class="highlight" >
                ________________________________________________________________________
                
                <h1>Example</h1>

                {custom_text}
                </span>
                """,
            unsafe_allow_html=True,
        )


# <span style="text-align: left;"></span>

st.write("# COPY PALETTE")


# color_palette = reorder_as_ombre(color_palette)

st.image(gen_palette_img(color_palette))

# st.image(gen_palette_img(reorder_as_ombre(color_palette)))


# st.code(convert_rgb_palette(reorder_as_ombre(color_palette)), wrap_lines=True)

st.code(reorder_as_ombre(color_palette))

# color_palette
