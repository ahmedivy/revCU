import asyncio

from spider import Spider


async def main():
    async with Spider() as spider:
        spider.scrape_dashboard()
        for course in spider.generate_marks():
            print(course)
            for mark in course.marks:
                print(mark)


if __name__ == "__main__":
    asyncio.run(main())
