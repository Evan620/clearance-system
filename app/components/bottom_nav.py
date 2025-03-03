import flet as ft

def create_bottom_nav(page: ft.Page, selected_index: int = 0):
    """
    Creates a bottom navigation bar for the app.
    """
    def handle_nav_change(e):
        """
        Handles navigation when a bottom navigation item is clicked.
        """
        index = e.control.selected_index
        routes = ["/home", "/progress", "/profile"]  # Define routes for each index
        page.go(routes[index])  # Navigate to the selected route

    return ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.icons.HOME_OUTLINED,
                selected_icon=ft.icons.HOME_ROUNDED,
                label="Home"
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.SHOW_CHART_OUTLINED,
                selected_icon=ft.icons.SHOW_CHART_ROUNDED,
                label="Progress"
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.PERSON_OUTLINE_ROUNDED,
                selected_icon=ft.icons.PERSON_ROUNDED,
                label="Profile"
            ),
        ],
        selected_index=selected_index,  # Use the passed selected_index
        on_change=handle_nav_change,  # Handle navigation changes
        bgcolor=ft.Colors.GREY_500,  # Set a bluish background
        surface_tint_color=ft.Colors.BLUE_100,
        indicator_color=ft.Colors.BLUE_500,
        height=65,
        elevation=2,
        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
    )