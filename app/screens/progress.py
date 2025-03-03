import flet as ft
import supabase

# Mock session storage
session_storage = {}

async def progress_page(page: ft.Page):
    page.clean()
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.LIGHT_BLUE_50

    user_id = page.session.get("user_id")
    status = await fetch_clearance_status(user_id)

    if not status:
        page.add(
            ft.Text("Error loading clearance status", color=ft.Colors.RED_600)
        )
        return

    # Update progress indicator
    progress_indicator = ft.Container(
        content=ft.Column([
            ft.Text(
                f"Overall Progress: {status['completion_percentage']:.0f}%",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_800
            ),
            ft.ProgressBar(
                value=status['completion_percentage'] / 100,
                bgcolor=ft.Colors.BLUE_50,
                color=ft.Colors.BLUE_800,
                height=8
            )
        ]),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        margin=ft.margin.only(bottom=20)
    )

    # Header
    header = ft.Container(
        content=ft.Column([
            ft.Text(
                "Clearance Progress",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
                font_family="Poppins",
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Track your clearance status below",
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
            colors=["#4FC3F7", "#2196F3"]
        ),
        border_radius=ft.border_radius.only(bottom_left=25, bottom_right=25, top_left=25, top_right=25),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.colors.with_opacity(0.2, "#4FC3F7")
        ),
        margin=20,
        alignment=ft.alignment.center
    )

    # Check if status is already cached in session
    if user_id not in session_storage:
        # Fetch from backend and cache it
        status = await fetch_clearance_status(user_id)
        session_storage[user_id] = status
    else:
        # Use cached status
        status = session_storage[user_id]

    # Check if all departments are cleared
    all_cleared = all(status["submissions"].values())

    # UI components
    if all_cleared:
        # Display a message indicating clearance is complete
        clearance_complete_message = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Congratulations! You have cleared all departments.",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREEN_700,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Please wait for final approval from the departments.",
                    size=16,
                    color=ft.Colors.BLUE_GREY_700,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Once approved, you can download your clearance certificate.",
                    size=16,
                    color=ft.Colors.BLUE_GREY_700,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.ElevatedButton(
                    "Download Certificate",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=lambda e: download_certificate(),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    disabled=True  # Initially disabled until approval
                )
            ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )
        page.add(header, clearance_complete_message)
    else:
        # Department status list
        department_grid = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                leading=ft.Icon(
                                    ft.icons.CHECK_CIRCLE if submitted else ft.icons.PENDING,
                                    color=ft.Colors.GREEN_600 if submitted else ft.Colors.ORANGE_400
                                ),
                                title=ft.Text(
                                    dept,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_800,
                                    font_family="Poppins"
                                ),
                                subtitle=ft.Text(
                                    "Submitted" if submitted else "Pending Submission",
                                    color=ft.Colors.BLUE_GREY,
                                    font_family="Open Sans"
                                )
                            ),
                            padding=ft.padding.all(10),
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10
                        ),
                        elevation=2
                    ),
                    on_click=lambda e, d=dept: page.go(f"/department/{d}"),
                    bgcolor=ft.Colors.WHITE,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=5,
                        color=ft.colors.with_opacity(0.1, ft.colors.BLUE_GREY)
                    ),
                    margin=ft.margin.only(bottom=10),
                    col={"sm": 6, "md": 6},
                )
                for dept, submitted in status["submissions"].items()
            ]
        )

        # Add department grid to page
        page.add(
            header,
            ft.Container(
                content=ft.Column(
                    controls=[
                        department_grid
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    expand=True,
                ),
                padding=ft.padding.all(20),
                expand=True,
            )
        )

    page.update()

async def fetch_clearance_status(user_id: str):
    try:
        # Get all submissions for this user
        submissions = supabase.table("submissions").select("*").eq("user_id", user_id).execute()
        
        # Get all departments
        departments = supabase.table("departments").select("*").execute()
        
        # Create a dictionary of department submissions
        submission_status = {}
        for dept in departments.data:
            # Check if there's a submission for this department
            is_submitted = any(
                sub["department_id"] == dept["id"] 
                for sub in submissions.data
            ) if submissions.data else False
            
            submission_status[dept["name"]] = is_submitted
        
        # Calculate completion percentage
        total_depts = len(departments.data)
        completed_depts = sum(1 for status in submission_status.values() if status)
        completion_percentage = (completed_depts / total_depts) * 100 if total_depts > 0 else 0

        return {
            "success": True,
            "status": "cleared" if completed_depts == total_depts else "pending",
            "completion_percentage": completion_percentage,
            "submissions": submission_status
        }
    except Exception as e:
        print(f"Error fetching clearance status: {e}")
        return None

def download_certificate():
    # Logic to download the certificate
    print("Downloading certificate...")