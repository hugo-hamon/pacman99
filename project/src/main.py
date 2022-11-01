from .game import app


def run(graphics_enable: bool) -> None:
    """Run the app"""
    application = app.App(
        graphics_enable=graphics_enable
    )
    # application.run() quelque chose du genre
