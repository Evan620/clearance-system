import flet as ft
from app.components.bottom_nav import create_bottom_nav
from app.utils.supabase_config import supabase
from datetime import datetime
import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

def department_form_page(page: ft.Page, dept_name: str):
    # Get department ID
    dept_response = supabase.table("departments").select("id").eq("name", dept_name).execute()
    if not dept_response.data:
        raise Exception("Department not found")
    department_id = dept_response.data[0]['id']

    page.clean()
    # Enable scrolling for the page
    page.scroll = ft.ScrollMode.AUTO

    # Back button handler
    def go_back(e):
        page.go("/home")

    # Department icons
    department_icons = {
        "Academic": ft.Icons.SCHOOL,
        "Finance": ft.Icons.ACCOUNT_BALANCE_WALLET,
        "Library": ft.Icons.LIBRARY_BOOKS,
        "ICT": ft.Icons.COMPUTER
    }

    # Form header with back button and department icon
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=go_back,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Go Back"
                ),
                ft.Icon(
                    department_icons.get(dept_name, ft.Icons.QUESTION_MARK),
                    color=ft.Colors.WHITE,
                    size=30
                ),
                ft.Text(
                    f"{dept_name} Department",
                    color=ft.Colors.WHITE,
                    size=20,
                    weight=ft.FontWeight.BOLD
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor=ft.Colors.BLUE_800,
        padding=ft.padding.symmetric(vertical=15, horizontal=20),
        border_radius=ft.border_radius.only(top_left=10, top_right=10)
    )

    # Common form styling
    def create_question(icon: str, label: str, hint: str, multiline=False):
        return ft.TextField(
            label=label,
            hint_text=hint,
            prefix_icon=icon,
            border_radius=8,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_600,
            text_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            multiline=multiline,
            min_lines=3 if multiline else 1,
            max_lines=5 if multiline else 1,
            width=400
        )

    def create_dropdown(icon: str, label: str, options: list):
        return ft.Dropdown(
            label=label,
            options=[ft.dropdown.Option(option) for option in options],
            prefix_icon=icon,
            border_radius=8,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_600,
            text_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_700, weight=ft.FontWeight.W_500),
            width=400
        )

    # Department-specific questions
    form_sections = []
    if dept_name == "Academic":
        form_sections = [
            create_question(ft.Icons.PERSON, "Full Name", "Enter your full name as it appears in academic records"),
            create_dropdown(ft.Icons.CHECK, "Completed Required Courses?", ["Yes", "No"]),
            create_question(ft.Icons.BOOK, "Remaining Courses", "List any remaining courses (if any)", multiline=True),
            create_dropdown(ft.Icons.ASSIGNMENT, "Thesis/Dissertation Status", 
                          ["Submitted and Approved", "In Progress", "Not Submitted"]),
            create_question(ft.Icons.EDIT, "Current Status", "Explain your current academic status", multiline=True)
        ]
    elif dept_name == "Finance":
        form_sections = [
            create_question(ft.Icons.ATTACH_MONEY, "Total Fee Balance", "Enter your current fee balance"),
            create_dropdown(ft.Icons.PAYMENT, "Tuition Payment Status", ["Fully Paid", "Partially Paid", "Not Paid"]),
            create_question(ft.Icons.DESCRIPTION, "Payment Plan", "Describe your payment plan if not fully paid", multiline=True),
            create_dropdown(ft.Icons.MONEY, "Additional Costs", ["Yes", "No"]),
            create_question(ft.Icons.LIST, "Additional Costs Details", "Specify any additional costs or fines", multiline=True)
        ]
    elif dept_name == "Library":
        form_sections = [
            create_question(ft.Icons.BADGE, "Student ID", "Enter your student ID number"),
            create_dropdown(ft.Icons.BOOK, "Library Books Status", ["All Returned", "Some Pending", "None Returned"]),
            create_question(ft.Icons.WARNING, "Pending Returns", "List any books or materials not yet returned", multiline=True),
            create_dropdown(ft.Icons.MONEY_OFF, "Library Fines", ["No Fines", "Pending Fines"]),
            create_question(ft.Icons.DESCRIPTION, "Fine Details", "Provide details of any pending library fines", multiline=True)
        ]
    elif dept_name == "ICT":
        form_sections = [
            create_question(ft.Icons.EMAIL, "University Email", "Enter your university email address"),
            create_dropdown(ft.Icons.COMPUTER, "IT Services Status", ["All Cleared", "Pending Services"]),
            create_question(ft.Icons.LIST, "Pending Services", "List any unpaid IT services or equipment", multiline=True),
            create_dropdown(ft.Icons.POLICY, "IT Policy Compliance", ["Fully Compliant", "Non-Compliant"]),
            create_question(ft.Icons.EDIT, "Non-Compliance Details", "Explain any IT policy violations or issues", multiline=True)
        ]

    async def handle_submit(e):
        try:
            # Show loading state
            submit_button.disabled = True
            submit_button.text = "Submitting..."
            page.update()

            # Get user ID from session
            user_id = page.session.get("user_id")
            if not user_id:
                raise Exception("User not logged in")

            # Check if user has already submitted for this department
            existing_request = supabase.table("clearancerequests")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("department_id", department_id)\
                .execute()

            if existing_request.data:
                raise Exception(f"You have already submitted clearance for {dept_name} department")

            # Collect form data
            form_data = {}
            for field in form_sections:
                if not field.value:
                    raise Exception(f"{field.label} is required")
                form_data[field.label] = field.value

            # Submit to Supabase using lowercase table names
            response = supabase.table("clearancerequests").insert({
                "user_id": user_id,
                "department_id": department_id,
                "status": "Pending",
                "form_data": form_data,
                "submitted_at": datetime.now().isoformat()
            }).execute()

            if response.data:
                # Create notification (removed await)
                supabase.table("notifications").insert({
                    "user_id": user_id,
                    "message": f"Clearance request submitted for {dept_name} department",
                    "created_at": datetime.now().isoformat()
                }).execute()

                # Show success dialog
                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Success!", size=20, weight=ft.FontWeight.BOLD),
                    content=ft.Text(
                        f"Your clearance request for {dept_name} department has been submitted successfully.",
                        size=16
                    ),
                    actions=[
                        ft.TextButton("View Progress", on_click=lambda _: page.go("/progress")),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )

                page.dialog = dialog
                dialog.open = True
                page.update()

                # Disable the form
                for field in form_sections:
                    field.disabled = True
                submit_button.disabled = True
                submit_button.text = "Already Submitted"
                page.update()

            else:
                raise Exception("Failed to submit form")

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(e)}"),
                bgcolor=ft.Colors.RED_600
            )
            page.snack_bar.open = True
            submit_button.disabled = False
            submit_button.text = "Submit Form"
            page.update()

    submit_button = ft.ElevatedButton(
        "Submit Form",
        icon=ft.Icons.CHECK_CIRCLE,
        on_click=handle_submit,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    # Main content layout
    main_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        header,
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    *form_sections,
                                    ft.Container(height=20),
                                    submit_button
                                ],
                                spacing=15,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            padding=ft.padding.all(20),
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            width=450
                        )
                    ],
                    spacing=0,
                ),
                expand=True,
            )
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(main_content)
    page.update()

    # When loading the form, check if already submitted
    try:
        existing_request = supabase.table("clearancerequests")\
            .select("*")\
            .eq("user_id", page.session.get("user_id"))\
            .eq("department_id", department_id)\
            .execute()

        if existing_request.data:
            # Disable the form if already submitted
            for field in form_sections:
                field.disabled = True
            submit_button.disabled = True
            submit_button.text = "Already Submitted"
            page.update()
    except Exception as e:
        print(f"Error checking submission status: {e}")

def get_selected_index(route: str) -> int:
        return {
            "/home": 0,
            "/progress": 1,
            "/profile": 2,
            "/account_settings": 3
        }.get(route, 0)