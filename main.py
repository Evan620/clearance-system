import flet as ft
import threading
from app.screens.home_screen import home_screen
from app.screens.profile import profile_page
from app.screens.progress import progress_page
from app.screens.account_settings import account_settings_page
from app.screens.department_form import department_form_page
from app.components.bottom_nav import create_bottom_nav
from app.utils.supabase_config import supabase
import asyncio
from datetime import datetime

def main(page: ft.Page):
    # Set page properties
    page.title = "Online Clearance System"
    page.window_max_width = 375
    page.window_width = 375
    page.window_max_height = 800
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.WHITE
    page.fonts = {
        "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap",
        "Open Sans": "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap"
    }

    # Define theme with proper color contrasts
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_600,
            secondary=ft.Colors.BLACK,
            background=ft.Colors.WHITE,
            error=ft.Colors.RED_600,
            on_error=ft.Colors.WHITE,
            on_primary=ft.Colors.WHITE,
            on_secondary=ft.Colors.BLUE_600,
        ),
        text_theme=ft.TextTheme(
            headline_medium=ft.TextStyle(
                font_family="Arial",
                color=ft.Colors.BLACK,
                size=24,
                weight=ft.FontWeight.BOLD
            ),
            body_medium=ft.TextStyle(
                font_family="Arial",
                color=ft.Colors.BLACK87,
                size=16
            ),
        ),
    )

    # --- Helper Functions ---
    def show_snackbar(page, message, color=ft.Colors.RED_600):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color,
            action="Dismiss",
            duration=5000,
        )
        page.snack_bar.open = True
        page.update()

    def get_selected_index(route: str) -> int:
        return {
            "/home": 0,
            "/progress": 1,
            "/profile": 2,
            "/account_settings": 3
        }.get(route, 0)

    # --- Real-Time Updates ---
    def listen_for_updates():
        def callback(payload):
            if payload.event_type == "INSERT":
                notification = payload.new
                if notification["user_id"] == page.session.get("user_id"):
                    show_snackbar(page, notification["message"], ft.Colors.BLUE_600)
        supabase.realtime.from_("Notifications").on("INSERT", callback).subscribe()

    # --- UI Screens ---
    def login_screen():
        email_field = ft.TextField(
            label="Email",
            prefix_icon=ft.Icons.EMAIL,
            border_radius=8,
            filled=True,
            fill_color=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            text_style=ft.TextStyle(color=ft.Colors.BLACK, size=14),
            width=280
        )
        
        password_field = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            border_radius=8,
            filled=True,
            fill_color=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            text_style=ft.TextStyle(color=ft.Colors.BLACK, size=14),
            width=280
        )

        def sign_in(e):
            email = email_field.value
            password = password_field.value
            
            if not all([email, password]):
                show_snackbar(page, "Please fill in all fields")
                return

            try:
                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                if not user.user.email_confirmed_at:
                    show_snackbar(page, "Please verify your email before logging in.", ft.Colors.ORANGE)
                    return
                page.session.set("user_id", user.user.id)
                page.session.set("user_email", email)
                show_snackbar(page, "Login successful!", ft.Colors.GREEN_600)
                page.update()
                page.go("/home")
            except Exception as e:
                show_snackbar(page, f"Login failed: {str(e)}")
                page.update()

        sign_in_button = ft.ElevatedButton(
            "Sign In",
            icon=ft.Icons.LOGIN,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            width=280,
            on_click=sign_in
        )

        error_display = ft.Text("", color=ft.Colors.RED_600, size=16, visible=False)

        return ft.Container(
            content=ft.Card(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            ft.Icon(ft.Icons.LOCK, size=36, color=ft.Colors.BLUE_600),
                            margin=ft.margin.only(bottom=20)
                        ),
                        ft.Text("Welcome Back!", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                        email_field,
                        password_field,
                        error_display,
                        sign_in_button,
                        ft.TextButton(
                            "Don't have an account? Sign up",
                            on_click=lambda _: page.go("/signup"),
                            style=ft.ButtonStyle(color=ft.Colors.BLUE_600)
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                elevation=6,
                width=350,
                height=450,
                color=ft.Colors.WHITE
            ),
            alignment=ft.alignment.center,
            gradient=ft.LinearGradient(
                colors=[ft.Colors.BLUE_50, ft.Colors.WHITE]
            )
        )

    def signup_screen():
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
        
        email_field = ft.TextField(
            label="Email",
            prefix_icon=ft.Icons.EMAIL,
            border_radius=8,
            filled=True,
            fill_color=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            text_style=ft.TextStyle(color=ft.Colors.BLACK),
            width=300
        )
        
        reg_number_field = ft.TextField(
            label="Registration Number",
            prefix_icon=ft.Icons.NUMBERS,
            border_radius=8,
            filled=True,
            fill_color=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            text_style=ft.TextStyle(color=ft.Colors.BLACK),
            width=300
        )
        
        password_field = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            border_radius=8,
            filled=True,
            fill_color=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            text_style=ft.TextStyle(color=ft.Colors.BLACK),
            width=300
        )

        error_display = ft.Text("", color=ft.Colors.RED_600, size=16, visible=False)

        def sign_up(e):
            full_name = full_name_field.value
            email = email_field.value
            student_id = reg_number_field.value
            password = password_field.value

            if not all([full_name, email, student_id, password]):
                show_snackbar(page, "Please fill in all fields")
                return

            if len(password) < 6:
                show_snackbar(page, "Password must be at least 6 characters")
                return

            try:
                auth_user = supabase.auth.sign_up({"email": email, "password": password})
                if auth_user.user:
                    user_data = {
                        "id": auth_user.user.id,
                        "full_name": full_name,
                        "email": email,
                        "student_id": student_id,
                        "created_at": datetime.now().isoformat()
                    }
                    response = supabase.table("students").insert(user_data).execute()

                    if response.data:
                        show_snackbar(page, "Account created! Check email to verify", ft.Colors.GREEN_600)
                        page.update()
                        page.go("/login")
                    else:
                        raise Exception("Failed to create user profile")
                else:
                    raise Exception("Failed to create account")
            except Exception as e:
                show_snackbar(page, f"Signup failed: {str(e)}")
                page.update()

        sign_up_button = ft.ElevatedButton(
            "Create Account",
            icon=ft.Icons.PERSON_ADD,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            width=300
        )

        sign_up_button.on_click = sign_up

        return ft.Container(
            content=ft.Card(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            ft.Icon(ft.Icons.PERSON_ADD, size=40, color=ft.Colors.BLUE_600),
                            margin=ft.margin.only(bottom=30)
                        ),
                        ft.Text("Create Account", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                        full_name_field,
                        email_field,
                        reg_number_field,
                        password_field,
                        error_display,
                        sign_up_button,
                        ft.TextButton(
                            "Already have an account? Sign in",
                            on_click=lambda _: page.go("/"),
                            style=ft.ButtonStyle(color=ft.Colors.BLUE_600)
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                elevation=8,
                width=400,
                height=650,
                color=ft.Colors.WHITE
            ),
            alignment=ft.alignment.center,  
            gradient=ft.LinearGradient(
                colors=[ft.Colors.BLUE_50, ft.Colors.WHITE]
            )
        )

    # --- Route Handler ---
    async def route_change(e):
        page.clean()
        if e.route in ["/", "/login", "/signup"]:
            if e.route in ["/", "/login"]:
                page.add(login_screen())
            elif e.route == "/signup":
                page.add(signup_screen())
        else:
            if not page.session.get("user_id"):
                page.go("/")
                return

            if e.route == "/home":
                home_screen(page)
            elif e.route == "/profile":
                profile_page(page)
            elif e.route == "/progress":
                await progress_page(page)
            elif e.route.startswith("/department/"):
                dept_name = e.route.split("/")[-1]
                print(f"Route department name: {dept_name}")
                department_form_page(page, dept_name)
            elif e.route == "/account_settings":
                account_settings_page(page)

            page.add(create_bottom_nav(page, get_selected_index(e.route)))
        page.update()

    # Initial setup
    def initialize():
        try:
            session = supabase.auth.get_session()
            if session and session.user.email_confirmed_at:
                page.session.set("user_id", session.user.id)
                page.go("/home")
            else:
                page.go("/")
        except Exception as e:
            print(f"Initialization error: {e}")
            page.go("/")

    # Set up route handler
    page.on_route_change = route_change
    page.on_view_pop = lambda _: page.go(page.route)
    initialize()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)