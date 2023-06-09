from __future__ import annotations

from asyncio import get_event_loop, create_task
from typing import Optional

from prisma import Client, register  # type: ignore
from prisma.engine.errors import AlreadyConnectedError
from prisma.errors import ClientAlreadyRegisteredError


class Database:
    """This is a singleton database connector, thus, overwrite the `__new__`
    life cycle hook method if you desire remove this behavior."""

    __instance: Optional[Database] = None

    # ? ------------------------------------------------------------------------
    # ? LIFE CYCLE HOOKS
    # ? ------------------------------------------------------------------------

    def __new__(cls) -> Database:
        """A hook for new database object creation.
        Returns:
            Database: A self instance.
        """

        if cls.__instance is None:
            cls.conn = Client()

            try:
                register(cls.conn)
            except ClientAlreadyRegisteredError:
                pass
            except Exception as exc:
                raise exc

            cls.__instance = super(Database, cls).__new__(cls)

        return cls.__instance

    # ? ------------------------------------------------------------------------
    # ? PUBLIC METHODS
    # ? ------------------------------------------------------------------------

    async def connect(self) -> None:
        """Create the database connection.
        Raises:
            exc: A generalized Exception dispatched only if a unexpected error
                occurred.
        """

        try:
            await self.conn.connect()
        except AlreadyConnectedError:
            pass
        except Exception as exc:
            raise exc

    def disconnect(self) -> None:
        """Breaks database connection.
        Raises:
            exc: A generalized Exception dispatched only if a unexpected error
                occurred.
        """

        loop = get_event_loop()

        try:
            if loop.is_running():
                create_task(self.conn.disconnect())
            else:
                loop.run_until_complete(self.conn.disconnect())

        except RuntimeError:
            pass
        except Exception as exc:
            raise exc


# ------------------------------------------------------------------------------
# SETUP DEFAULT EXPORTS
# ------------------------------------------------------------------------------


__all__ = ["Database"]
