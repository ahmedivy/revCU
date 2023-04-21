import typer
import logging

from revCU import Spider, Course

logging.basicConfig(level=logging.ERROR)

app = typer.Typer()


@app.command()
def config(
    username: str = typer.Option(..., prompt=True, help="CU Username"),
    password: str = typer.Option(..., prompt=True, hide_input=True, help="CU Password"),
):
    """
    Configure the credentials for the CU Portal.
    """
    with Spider() as spider:
        spider.config["username"] = username
        spider.config["password"] = password
        spider.write_config()
        typer.secho("Credentials saved", fg=typer.colors.GREEN)


@app.command()
def all():
    with Spider() as spider:
        # Print the courses
        spider.get_cookies()
        spider.scrape_dashboard()
        Course.print_courses(spider.courses)

        # Print the marks
        for course in spider.generate_marks():
            course.print_marks()
            typer.secho("\n", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
