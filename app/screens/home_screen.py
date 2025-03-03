import flet as ft
import threading
from app.components.bottom_nav import create_bottom_nav
from app.utils.supabase_config import supabase
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))


def home_screen(page: ft.Page):
    page.clean()
    page.bgcolor = ft.Colors.LIGHT_BLUE_50

    # Enhanced header with modern typography
    header = ft.Container(
        content=ft.Column([
            ft.Text(
                "Student Clearance",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
                font_family="Poppins",
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Select a department below",
                size=14,
                color=ft.Colors.WHITE,
                font_family="Open Sans",
                opacity=0.9,
                text_align=ft.TextAlign.CENTER
            )
        ],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=20),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#4FC3F7", "#2196F3"]  # Sky Blue gradient
        ),
        border_radius=ft.border_radius.only(bottom_left=25, bottom_right=25, top_left=25, top_right=25),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.colors.with_opacity(0.2, "#4FC3F7")
        ),
        margin=20,
        alignment=ft.alignment.center  # Center the header container
    )

    # Enhanced department cards
    departments = [
        {"name": "Academic", "icon": ft.Icons.SCHOOL, "color": "#4FC3F7", "description": "Submit academic clearance"},
        {"name": "Finance", "icon": ft.Icons.ACCOUNT_BALANCE_WALLET, "color": "#4FC3F7", "description": "Clear financial records"},
        {"name": "Library", "icon": ft.Icons.LIBRARY_BOOKS, "color": "#4FC3F7", "description": "Clear library dues"},
        {"name": "ICT", "icon": ft.Icons.COMPUTER, "color": "#4FC3F7", "description": "IT services clearance"},
    ]

    def handle_department_click(e, dept_name):
        page.go(f"/department/{dept_name}")

    department_cards = [
        ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(dept["icon"], color=dept["color"], size=28),
                            ft.Text(
                                dept["name"],
                                font_family="Poppins",
                                size=20,
                                weight=ft.FontWeight.W_600,
                                color="#333333"  # Charcoal Gray
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Text(
                            dept["description"],
                            font_family="Open Sans",
                            size=14,
                            color="#666666",  # Soft Gray
                            opacity=0.9
                        )
                    ]),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                ),
                elevation=0,
                surface_tint_color=ft.colors.with_opacity(0.1, "#4FC3F7"),
                margin=10,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=5,
                color=ft.colors.with_opacity(0.1, ft.colors.BLUE_GREY)
            ),
            margin=10,
            on_click=lambda e, dept=dept["name"]: handle_department_click(e, dept)  # Attach click handler
        ) for dept in departments
    ]

    # Responsive grid layout
    department_grid = ft.ResponsiveRow(
        controls=[
            ft.Container(
                content=card,
                col={"sm": 6, "md": 6},
                padding=8,
            ) for card in department_cards
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Main content with proper spacing
    main_content = ft.Column(
        controls=[
            ft.Container(
                content=department_grid,
                padding=ft.padding.symmetric(horizontal=16, vertical=20),
            )
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    page.add(
        header,
        ft.Container(
            content=main_content,
            expand=True,
        )
    )
    page.update()