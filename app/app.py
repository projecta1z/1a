import reflex as rx
from app.components.directory import directory
from app.states.directory import DirectoryState


def index() -> rx.Component:
    return directory()


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            cross_origin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index,
    route="/",
    title="The Username Index",
    description="An alphabetical collection of usernames. Find a name or browse the A–Z index.",
    on_load=DirectoryState.load,
)
