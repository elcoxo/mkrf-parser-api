import os
from dotenv import load_dotenv

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASS')

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,

)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base: DeclarativeMeta = declarative_base()


def connection(method):
    """
    Decorator for database that enables automatic session creation and closure.

    connection: takes the original function to be wrapped
    wrapper: accepts all arguments of the original function
    async_session_maker(): automatically creates and closes a session in async mode
    """

    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper
