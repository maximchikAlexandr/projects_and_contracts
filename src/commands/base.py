from cleo.commands.command import Command as BaseCommand

from src.db.settings import EngineDB
from src.facades import ContractFacade, ProjectFacade

engine_db = EngineDB()
contract_facade = ContractFacade(engine_db=engine_db)
project_facade = ProjectFacade(engine_db=engine_db)


class CreateEntityCommand(BaseCommand):
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


class Command(BaseCommand):

    def render_custom_table(self, data: list[dict[str, str]]) -> None:
        headers = list(data[0].keys())
        rows = [list(dct.values()) for dct in data]
        self.render_table(headers, rows, style='box-double')

    def is_valid_model_id(self, facade, model_id):

        try:
            int(model_id)
        except ValueError:
            self.line(
                "<error>Некорректный id (идентификатором). Только целочисленный формат</error>"
            )
            return False

        if not facade.is_existing(model_id):
            self.line(
                "<error>Объект с таким id (идентификатором) не существует</error>"
            )
            return False

        return True
