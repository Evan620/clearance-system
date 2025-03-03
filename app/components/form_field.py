import flet as ft

def show_tooltip(e, hint):
    e.control.tooltip = hint


def create_form_field(page: ft.Page, label: str, hint: str, required: bool = True, field_type: str = "text"):
    error_text = ft.Text("", color=ft.Colors.RED_600, size=12, visible=False)
    
    field = ft.TextField(
        label=label + (" *" if required else ""),
        hint_text=hint,
        width=None,
        height=55,
        text_size=16,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_800,

        focused_bgcolor=ft.Colors.BLUE_50,
        helper_text="Required" if required else "Optional",
        helper_style=ft.TextStyle(
            size=12,
            color=ft.Colors.BLUE_GREY_400,
            italic=True,
        ),
        label_style=ft.TextStyle(
            size=14,
            color=ft.Colors.BLUE_800,
            weight=ft.FontWeight.W_500,
        ),
        text_style=ft.TextStyle(
            size=16,
            color=ft.Colors.BLUE_GREY_900,
        ),
        expand=True,
        suffix_icon=ft.icons.INFO_OUTLINE,
        suffix_style=ft.TextStyle(color=ft.Colors.BLUE_400),
        on_focus=lambda e: show_tooltip(e, hint),
    )
    
    def validate(e):
        if required and not field.value:
            error_text.value = f"{label} is required"
            error_text.visible = True
        else:
            error_text.visible = False
        page.update()
    
    field.on_blur = validate
    
    return ft.Container(
        content=ft.Column([
            field,
            error_text
        ]),
        margin=ft.margin.only(bottom=15),
        expand=True,
    ) 