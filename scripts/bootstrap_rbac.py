import asyncio

from app.db import AsyncSessionFactory
from app.services.bootstrap import RBACBootstrapper


async def main() -> None:
    async with AsyncSessionFactory() as session:
        await RBACBootstrapper(session).bootstrap()


if __name__ == '__main__':
    asyncio.run(main())
