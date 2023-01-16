import asyncio
from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class AsyncAlchemyInstruments():

    def __init__(self, table, engine):
        self.table = table
        self.engine = engine
        self.async_session = sessionmaker(self.engine, expire_on_commit=False,
                                          class_=AsyncSession
                                          )

    async def database_init(self):
        Base = declarative_base()
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await self.engine.dispose()

    async def add_entry(self, **attrs):
        async with self.async_session() as session:
            async with session.begin():
                new_entry = self.table()
                for attr, val in attrs.items():
                    setattr(new_entry, attr, val)
                session.add(new_entry)
                await session.commit()
        await self.engine.dispose()
        result = new_entry.to_dict()
        return result

    async def find_entry(self, **attrs):
        async with self.async_session() as session:
            atr = attrs.popitem()
            db_req = select(self.table)\
                .where(self.table.__dict__[atr[0]] == atr[1])
            for key, val in attrs.items():
                db_req = db_req.where(self.table.__dict__[key] == val)

            query = await session.execute(db_req)
            tb = query.scalars().first()
            if tb:
                result = tb
            else:
                result = None
        await self.engine.dispose()
        return result

    async def get_entry(self, id=None):
        async with self.async_session() as session:
            if id:
                query = await session\
                    .execute(select(self.table).where(self.table.id == id))
            else:
                query = await session.execute(select(self.table))
            tb = query.scalars().all()
            if tb:
                result = tb
            else:
                result = None
        await self.engine.dispose()

        return result

    async def update_entry(self, id, **attrs):
        async with self.async_session() as session:
            query = await\
                 session.execute(select(self.table).where(self.table.id == id))
            tb = query.scalars().first()
            if tb:
                for attr, val in attrs.items():
                    setattr(tb, attr, val)
                await session.commit()
                result = tb.to_dict()
            else:
                result = None
        await self.engine.dispose()

        return result

    async def delete_entry(self, id):
        async with self.async_session() as session:
            query = await session\
                    .execute(select(self.table).where(self.table.id == id))
            tb = query.scalars().first()
            if tb:
                query = await session\
                    .execute(delete(self.table).where(self.table.id == id))
                await session.commit()
                result = tb.to_dict()
            else:
                result = None

        await self.engine.dispose()
        return result
