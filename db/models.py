import enum

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class StatusEnum(enum.StrEnum):
    draft = "черновик"
    active = "активен"
    completed = "завершен"


class ProjectModel(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    created = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    contract = relationship("ContractModel", back_populates="project", passive_deletes=True)


class ContractModel(Base):
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    created = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    signed = Column(TIMESTAMP, nullable=True)
    status = Column(String, Enum(StatusEnum), default=StatusEnum.draft)
    project_id = Column(Integer, ForeignKey("project.id", ondelete='SET NULL'))
    project = relationship("ProjectModel", back_populates="contract")
