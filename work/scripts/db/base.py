"""SQLAlchemy declarative base definition.

This module defines the base class for all ORM models used in the
application. All database models must inherit from this class to ensure
proper metadata registration and ORM functionality.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models.

    This class provides the foundation for SQLAlchemy declarative models,
    including metadata storage and table mapping functionality.

    Notes
    -----
    All ORM models must inherit from this class.
    """

    pass
