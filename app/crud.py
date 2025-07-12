from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_create: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        email=user_create.email,
        password_hash=hashed_password,
        name=user_create.name,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
