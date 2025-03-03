import flet as ft
from app.utils.supabase_config import supabase
from datetime import datetime
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

def account_settings_page(page: ft.Page):
    page.clean()
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.LIGHT_BLUE_50

    # Back button
    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda _: page.go("/profile"),
        icon_color=ft.Colors.BLUE_600,
        tooltip="Go Back"
    )

    # Form fields
    full_name_field = ft.TextField(
        label="Full Name",
        prefix_icon=ft.Icons.PERSON,
        border_radius=8,
        filled=True,
        fill_color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_200,
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        width=300
    )

    gender_field = ft.Dropdown(
        label="Gender",
        options=[
            ft.DropdownOption("Male"),
            ft.DropdownOption("Female"),
            ft.DropdownOption("Other")
        ],
        border_radius=8,
        filled=True,
        fill_color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_200,
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        width=300
    )
    phone_number_field = ft.TextField(
        label="Phone Number",
        prefix_icon=ft.Icons.PHONE,
        border_radius=8,
        filled=True,
        fill_color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_200,
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        width=300
    )

    address_field = ft.TextField(
        label="Address",
        prefix_icon=ft.Icons.HOME,
        border_radius=8,
        filled=True,
        fill_color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_200,
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        width=300
    )

    course_field = ft.TextField(
        label="Course",
        prefix_icon=ft.Icons.SCHOOL,
        border_radius=8,
        filled=True,
        fill_color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_200,
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        width=300
    )

    registration_number_field = ft.TextField(
        label="Registration Number",
        prefix_icon=ft.Icons.NUMBERS,
        border_radius=8,
        filled=True,
        fill_color=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_200,
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        width=300
    )

    def save_info(e):
        user_id = page.session.get("user_id")
        if not user_id:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("User not logged in"),
                bgcolor=ft.Colors.RED_600
            )
            page.snack_bar.open = True
            return

        user_info = {
            "user_id": user_id,
            "full_name": full_name_field.value,
            "gender": gender_field.value,
            "phone_number": phone_number_field.value,
            "address": address_field.value,
            "course": course_field.value,
            "registration_number": registration_number_field.value,
            "updated_at": datetime.now().isoformat()
        }

        response = supabase.table("student_info").upsert(user_info).execute()
        if response.data:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Information saved successfully!"),
                bgcolor=ft.Colors.GREEN_600
            )
            page.snack_bar.open = True
            page.go("/profile")
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Failed to save information"),
                bgcolor=ft.Colors.RED_600
            )
            page.snack_bar.open = True

    save_button = ft.ElevatedButton(
        "Save Information",
        icon=ft.Icons.SAVE,
        on_click=save_info,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        width=300
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    back_button,
                    ft.Text("Account Settings", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                    full_name_field,
                    gender_field,           
                    phone_number_field,
                    address_field,
                    course_field,
                    registration_number_field,
                    save_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            width=400
        )
    ) 