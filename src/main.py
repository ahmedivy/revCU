import typer
import asyncio
import logging

from revCU import Spider, Course

logging.basicConfig(level=logging.ERROR)


async def main():
    async with Spider() as spider:
        # Print the courses
        spider.scrape_dashboard()
        Course.print_courses(spider.courses)

        # Print the marks
        for course in spider.generate_marks():
            course.print_marks()
            typer.secho("\n", fg=typer.colors.GREEN)


def _main():
    asyncio.run(main())


if __name__ == "__main__":
    typer.run(_main)
