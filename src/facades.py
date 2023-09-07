from sqlalchemy import (
    String,
    case,
    func,
    insert,
    literal_column,
    outerjoin,
    select,
    update,
)
from sqlalchemy.sql import text

from src.db.models import ContractModel, ProjectModel, StatusEnum


class BaseFacade:
    MODEL_CLASS = None
    DATETIME_FORMAT = "DD-MM-YYYY"

    def __init__(self, engine_db):
        conn = engine_db.connect()
        self.connection = conn.execution_options(echo=True)
        self.model = self.MODEL_CLASS

    def create(self, title):
        query = insert(self.model).values(title=title)
        self.connection.execute(query)
        self.connection.commit()

    def is_existing(self, model_id):
        query = select(
            case(
                (func.count() > 0, literal_column("true")),
                else_=literal_column("false"),
            ).label("is_existing")
        ).where(self.model.id == model_id)
        result = self.connection.execute(query).fetchone()
        return result[0]


class ProjectFacade(BaseFacade):
    MODEL_CLASS = ProjectModel

    def get_all_projects(self):
        query = select(
            ProjectModel.id.label("id"),
            ProjectModel.title.label("Название проекта"),
            func.to_char(ProjectModel.created, self.DATETIME_FORMAT).label(
                "Дата создания проекта"
            ),
        ).order_by("id")
        cursor = self.connection.execute(query)
        return cursor.mappings().all()

    def has_active_contracts(self, project_id):
        query = (
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
        result = self.connection.execute(query).fetchone()
        return result[0]

    def add_contract(self, project_id, contract_id):
        query = (
            update(ContractModel)
            .where(ContractModel.id == contract_id)
            .values(project_id=project_id)
        )
        self.connection.execute(query)
        self.connection.commit()


class ContractFacade(BaseFacade):
    MODEL_CLASS = ContractModel

    def get_unlinked_active_contracts(self):
        query = (
            select(
                ContractModel.id,
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
        cursor = self.connection.execute(query)
        return cursor.mappings().all()

    def get_linked_active_contracts(self):
        query = (
            select(
                ContractModel.id.label("id договора"),
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
        cursor = self.connection.execute(query)
        return cursor.mappings().all()

    def get_all_contracts(self):
        query = (
            select(
                ContractModel.id.label("id договора"),
                ContractModel.title.label("Название договора"),
                func.to_char(ContractModel.signed, self.DATETIME_FORMAT).label(
                    "Дата подписания договора"
                ),
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
        cursor = self.connection.execute(query)
        return cursor.mappings().all()

    def is_active(self, contract_id):
        query = select(
            case(
                (ContractModel.status == StatusEnum.active, literal_column("true")),
                else_=literal_column("false"),
            ).label("is_active")
        ).where(ContractModel.id == contract_id)
        result = self.connection.execute(query).fetchone()
        return result[0]

    def approve(self, contract_id):
        query = (
            update(ContractModel)
            .where(ContractModel.id == contract_id)
            .values(status=StatusEnum.active, signed=text("CURRENT_TIMESTAMP"))
        )
        self.connection.execute(query)
        self.connection.commit()

    def complete(self, contract_id):
        query = (
            update(self.model)
            .where(self.model.id == contract_id)
            .values(status=StatusEnum.completed)
        )
        self.connection.execute(query)
        self.connection.commit()
