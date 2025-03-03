import flet as ft
from app.components.bottom_nav import create_bottom_nav
from app.screens.account_settings import account_settings_page
from app.utils.supabase_config import supabase
import sys
import os
# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

def profile_page(page: ft.Page):
    page.clean()
    # Enable scrolling for the page
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.LIGHT_BLUE_50  # Add a light background color

    # Fetch user data from the database
    user_id = page.session.get("user_id")
    user_data = fetch_user_data(user_id)

    # Profile Header Component
    def create_profile_header(user_data):
        if not user_data:
            return ft.Container(
                content=ft.Column([
                    ft.Text("Profile not found", 
                        size=24, 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.BLUE_900
                    ),
                    ft.Text("Please complete your profile in Account Settings",
                        size=16,
                        color=ft.Colors.BLUE_GREY_600
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                margin=ft.margin.only(bottom=20)
            )

        return ft.Container(
            content=ft.Column([
                ft.Text(user_data.get("name", "No name provided"), 
                    size=24, 
                    weight=ft.FontWeight.BOLD, 
                    color=ft.Colors.BLUE_900
                ),
                ft.Text(user_data.get("email", "No email provided"),
                    size=16,
                    color=ft.Colors.BLUE_GREY_600
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            margin=ft.margin.only(bottom=20)
        )

    # Clearance Status Component
    def create_clearance_status():
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        title=ft.Text("Clearance Status", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                        trailing=ft.Text("25%", size=16, color=ft.Colors.BLUE_800)
                    ),
                    ft.ProgressBar(
                        value=0.25,
                        bgcolor=ft.Colors.BLUE_50,
                        color=ft.Colors.BLUE_800,
                        height=8
                    )
                ]),
                padding=ft.padding.all(15),
                bgcolor=ft.Colors.WHITE,
                width=min(page.window_width * 0.9, 400),  # Responsive width with a max limit
                border_radius=10  # Apply border radius here
            ),
            elevation=2,
            margin=ft.margin.only(bottom=20)
        )

    # Information Section Component
    def create_info_section(title: str, data: dict):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        title=ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                        leading=ft.Icon(ft.icons.INFO_OUTLINE, color=ft.Colors.BLUE_800)
                    ),
                    *[create_info_row(key, value) for key, value in data.items()]
                ]),
                padding=ft.padding.all(15),
                bgcolor=ft.Colors.WHITE,
            ),
            elevation=2,
            margin=ft.margin.only(bottom=20)
        )

    # Individual Info Row
    def create_info_row(label: str, value: str):
        return ft.Row([
            ft.Text(label, style=ft.TextStyle(size=14, color=ft.Colors.BLUE_GREY_700)),
            ft.Text(value, style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD))
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=10)

    # Settings Section Component
    def create_settings_section():
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        title=ft.Text("Settings", 
                            size=16, 
                            weight=ft.FontWeight.BOLD,
                            font_family="Poppins"
                        ),
                        leading=ft.Icon(ft.icons.SETTINGS, color=ft.Colors.BLUE_800)
                    ),
                    ft.Divider(),
                    ft.Container(
                        content=ft.ListTile(
                            title=ft.Text("Account Settings", font_family="Open Sans"),
                            leading=ft.Icon(ft.icons.PERSON_OUTLINE, color=ft.Colors.BLUE_800),
                            trailing=ft.Icon(ft.icons.ARROW_FORWARD_IOS, size=16)
                        ),
                        on_click=lambda _: page.go("/account_settings"),
                    ),
                    ft.Container(
                        content=ft.ListTile(
                            title=ft.Text("Help & Support", font_family="Open Sans"),
                            leading=ft.Icon(ft.icons.HELP_OUTLINE, color=ft.Colors.BLUE_800),
                            trailing=ft.Icon(ft.icons.ARROW_FORWARD_IOS, size=16)
                        ),
                        on_click=lambda _: page.go("/help"),
                    ),
                    ft.Container(
                        content=ft.ListTile(
                            title=ft.Text("Logout", color=ft.Colors.RED_600, font_family="Open Sans"),
                            leading=ft.Icon(ft.icons.LOGOUT, color=ft.Colors.RED_600),
                        ),
                        on_click=lambda _: handle_logout(page),
                    )
                ]),
                padding=ft.padding.all(15)
            ),
            elevation=0
        )

    # Main content
    main_content = ft.Column(
        controls=[
            create_profile_header(user_data),
            create_clearance_status(),
            create_info_section("Personal Information", {
                "Email": user_data.get("email", "N/A"),
                "Student ID": user_data.get("registration", "N/A"),
                "Role": user_data.get("role", "N/A"),
                "Gender": user_data.get("gender", "N/A"),
                "Course": user_data.get("course", "N/A"),
                "Phone Number": user_data.get("phone_number", "N/A"),
                "Address": user_data.get("address", "N/A")
            }),
            create_settings_section()
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(
        ft.Container(
            content=main_content,
            padding=ft.padding.all(20),
            expand=True,
        ),
        create_bottom_nav(page, 2)  # Add bottom navigation bar
    )
    page.update()

def fetch_user_data(user_id):
    try:
        user_response = supabase.table("users").select("*").eq("id", user_id).execute()
        info_response = supabase.table("student_info").select("*").eq("user_id", user_id).execute()

        if user_response.data:
            user = user_response.data[0]
            info = info_response.data[0] if info_response.data else {}
            return {
                "name": user.get("full_name", "Unknown"),
                "email": user.get("email", "N/A"),
                "registration": user.get("registration_number", "N/A"),
                "role": user.get("role", "N/A"),
                "phone_number": info.get("phone_number", "N/A"),
                "address": info.get("address", "N/A"),
                "gender": info.get("gender", "N/A"),
                "course": info.get("course", "N/A"),
            }
        return None
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None

def handle_logout(page: ft.Page):
    try:
        supabase.auth.sign_out()
        page.session.clear()
        page.go("/")
    except Exception as e:
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Logout failed: {str(e)}"),
            bgcolor=ft.Colors.RED_600
        )
        page.snack_bar.open = True
        page.update()