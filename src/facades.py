from sqlalchemy import (
    String,
    case,
    cast,
    func,
    insert,
    literal_column,
    outerjoin,
    select,
    update,
)
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.row import Row
from sqlalchemy.sql import text
from sqlalchemy.sql.dml import Insert, Update
from sqlalchemy.sql.selectable import Select

from src.db.models import ContractModel, ProjectModel, StatusEnum
from src.db.settings import EngineDB


class BaseFacade:
    MODEL_CLASS = None
    DATETIME_FORMAT = "DD-MM-YYYY"

    def __init__(self, engine_db: EngineDB) -> None:
        conn = engine_db.connect()
        self.connection = conn.execution_options(echo=True)
        self.model = self.MODEL_CLASS

    def create(self, title: str) -> int:
        query: Insert = insert(self.model).values(title=title)
        cursor: CursorResult = self.connection.execute(query)
        self.connection.commit()
        return cursor.inserted_primary_key[0]

    def is_existing(self, model_id: int) -> bool:
        query: Select = select(
            case(
                (func.count() > 0, literal_column("true")),
                else_=literal_column("false"),
            ).label("is_existing")
        ).where(self.model.id == model_id)
        result: Row = self.connection.execute(query).fetchone()
        return result[0]


class ProjectFacade(BaseFacade):
    MODEL_CLASS = ProjectModel

    def get_all_projects(self) -> list[dict[str, str]]:
        query: Select = select(
            cast(ProjectModel.id, String).label("pid"),
            ProjectModel.title.label("Название проекта"),
            func.to_char(ProjectModel.created, self.DATETIME_FORMAT).label(
                "Дата создания проекта"
            ),
        ).order_by("id")
        cursor: CursorResult = self.connection.execute(query)
        return cursor.mappings().all()

    def has_active_contracts(self, project_id: int) -> bool:
        query: Select = (
            select(
                case(
                    (func.count() > 0, literal_column("true")),
                    else_=literal_column("false"),
                ).label("has_active_contracts")
            )
            .select_from(
                outerjoin(
                    ContractModel,
                    ProjectModel,
                    ProjectModel.id == ContractModel.project_id,
                )
            )
            .where(
                (ProjectModel.id == project_id)
                & (ContractModel.status == StatusEnum.active)
            )
        )
        result: Row = self.connection.execute(query).fetchone()
        return result[0]

    def add_contract(self, project_id: int, contract_id: int) -> None:
        query: Update = (
            update(ContractModel)
            .where(ContractModel.id == contract_id)
            .values(project_id=project_id)
        )
        self.connection.execute(query)
        self.connection.commit()

    def complete_active_contract(self, project_id: int) -> None:
        query: Update = (
            update(ContractModel)
            .where(
                (ContractModel.project_id == project_id)
                & (ContractModel.status == StatusEnum.active)
            )
            .values(status=StatusEnum.completed)
        )
        self.connection.execute(query)
        self.connection.commit()


class ContractFacade(BaseFacade):
    MODEL_CLASS = ContractModel

    def get_unlinked_active_contracts(self) -> list[dict[str, str]]:
        query: Select = (
            select(
                cast(ContractModel.id, String),
                ContractModel.title.label("Название договора"),
                func.to_char(ContractModel.created, self.DATETIME_FORMAT).label(
                    "Дата создания"
                ),
                func.to_char(ContractModel.signed, self.DATETIME_FORMAT).label(
                    "Дата подписания"
                ),
                ContractModel.status.label("Статус"),
            )
            .where(
                (ContractModel.project_id.is_(None))
                & (ContractModel.status == StatusEnum.active)
            )
            .order_by("id")
        )
        cursor: CursorResult = self.connection.execute(query)
        return cursor.mappings().all()

    def get_linked_active_contracts(self) -> list[dict[str, str]]:
        query: Select = (
            select(
                cast(ContractModel.id, String).label("id договора"),
                ContractModel.title.label("Название договора"),
                func.to_char(ContractModel.signed, self.DATETIME_FORMAT).label(
                    "Дата подписания договора"
                ),
                ProjectModel.id.label("id проекта"),
                ProjectModel.title.label("Название проекта"),
            )
            .join(ProjectModel, ProjectModel.id == ContractModel.project_id)
            .filter(ContractModel.status == StatusEnum.active)
            .order_by("id")
        )
        cursor: CursorResult = self.connection.execute(query)
        return cursor.mappings().all()

    def get_all_contracts(self) -> list[dict[str, str]]:
        query: Select = (
            select(
                cast(ContractModel.id, String).label("id договора"),
                ContractModel.title.label("Название договора"),
                case(
                    (ContractModel.signed.is_(None), "-"),
                    else_=func.to_char(ContractModel.signed, self.DATETIME_FORMAT),
                ).label("Дата подписания договора"),
                ContractModel.status.label("Статус"),
                case(
                    (ProjectModel.id.is_(None), "-"), else_=ProjectModel.id.cast(String)
                ).label("id проекта"),
                case(
                    (ProjectModel.title.is_(None), "-"), else_=ProjectModel.title
                ).label("Название проекта"),
            )
            .outerjoin(ProjectModel, ProjectModel.id == ContractModel.project_id)
            .order_by("id договора")
        )
        cursor: CursorResult = self.connection.execute(query)
        return cursor.mappings().all()

    def is_active(self, contract_id: int) -> bool:
        query: Select = select(
            case(
                (ContractModel.status == StatusEnum.active, literal_column("true")),
                else_=literal_column("false"),
            ).label("is_active")
        ).where(ContractModel.id == contract_id)
        result: Row = self.connection.execute(query).fetchone()
        return result[0]

    def approve(self, contract_id: int) -> None:
        query: Update = (
            update(ContractModel)
            .where(ContractModel.id == contract_id)
            .values(status=StatusEnum.active, signed=text("CURRENT_TIMESTAMP"))
        )
        self.connection.execute(query)
        self.connection.commit()

    def complete(self, contract_id: int) -> None:
        query: Update = (
            update(self.model)
            .where(self.model.id == contract_id)
            .values(status=StatusEnum.completed)
        )
        self.connection.execute(query)
        self.connection.commit()
