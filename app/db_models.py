from sqlalchemy import Column, Integer, String

from app.database import Base


class ProjectDB(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default="planned")
