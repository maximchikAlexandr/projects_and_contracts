from cleo.commands.command import Command

from src.db.settings import EngineDB
from src.facades import ContractFacade, ProjectFacade

engine_db = EngineDB()
contract_facade = ContractFacade(engine_db=engine_db)
project_facade = ProjectFacade(engine_db=engine_db)


class CreateEntityCommand(Command):
    ENTITY_NAME = ''
    facade = None
    name = "create"

    def handle(self) -> None:
        if self.option("title"):
            title = self.option("title")
        else:
            title = f"Тестовый {self.ENTITY_NAME}"
            question = self.create_question(
                f"Название {self.ENTITY_NAME}а [<comment>{title}</comment>]: ", default=title
            )
            title = self.ask(question)
        inserted_pk = self.facade.create(title)
        self.line(
            f"<info>Был создан {self.ENTITY_NAME} с id: {inserted_pk}</info>"
        )


class RenderTableMixin:

    def render_custom_table(self, data: list[dict[str, str]]) -> None:
        headers = list(data[0].keys())
        rows = [list(dct.values()) for dct in data]
        self.render_table(headers, rows, style='box-double')
