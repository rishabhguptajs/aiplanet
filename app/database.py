from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
project_root = os.path.dirname(current_dir)  # Get the project root directory
env_path = os.path.join(project_root, '.env')  # Construct the path to the .env file

load_dotenv(env_path)  # Load the environment variables

# Retrieve the database URL from the environment variables
DATABASE_URL = os.getenv("POSTGRES_URL")
print(f"Current working directory: {os.getcwd()}")  # Print the current working directory
print(f".env file path: {env_path}")  # Print the path to the .env file
print(f"Environment variable POSTGRES_URL: {'Found' if DATABASE_URL else 'Not Found'}")  # Check if the POSTGRES_URL is found

# Modify the DATABASE_URL to use asyncpg driver
DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create an asynchronous database engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Enable logging of SQL statements
    pool_pre_ping=True,  # Check connections before using them
    pool_size=10,  # Set the size of the connection pool
    max_overflow=20  # Allow up to 20 additional connections beyond pool_size
)

# Create a session factory for asynchronous sessions
async_session = sessionmaker(
    engine, 
    class_=AsyncSession,  # Use AsyncSession for asynchronous operations
    expire_on_commit=False  # Do not expire instances after commit
)

# Asynchronous generator to provide a session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:  # Create a new session
        try:
            yield session  # Yield the session for use
        finally:
            await session.close()  # Ensure the session is closed after use