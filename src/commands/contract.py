from cleo.commands.command import Command

from src.db.settings import EngineDB
from src.facades import ContractFacade, ProjectFacade
from src.commands.base import CreateEntityCommand, RenderTableMixin
from src.commands.options import contract_title, contract_id_opt, project_id_opt

engine_db = EngineDB()
contract_facade = ContractFacade(engine_db=engine_db)
project_facade = ProjectFacade(engine_db=engine_db)


class CreateContractCommand(CreateEntityCommand):
    ENTITY_NAME = 'договор'
    facade = contract_facade
    description = "Создает договор"
    options = [contract_title]


class ListContractCommand(RenderTableMixin, Command):
    name = "ls"
    description = "Выводит список договоров"

    def handle(self) -> None:
        try:
            data = contract_facade.get_all_contracts()
            self.render_custom_table(data)
        except IndexError:
            self.line(
                "<comment>Таблица с договорами пуста</comment>"
            )


class ActivateContractCommand(Command):
    name = "act"
    description = "Подтверждает договор"
    options = [contract_id_opt]

    def handle(self) -> None:
        if self.option("contract_id"):
            contract_id = self.option("contract_id")
        else:
            question = self.create_question(
                "Введите id (идентификатор) договора для подтверждения: "
            )
            contract_id = self.ask(question)

        if not contract_facade.is_existing(contract_id):
            self.line(
                "<error>Договор с таким id (идентификатором) не существует</error>"
            )
            return

        if contract_facade.is_active(contract_id):
            self.line(
                f"<error>Нельзя подтвердить уже подтвержденный договор</error>"
            )
            return

        contract_facade.approve(contract_id)


class CompleteContractCommand(Command):
    name = "complete"
    description = "Завершает договор"
    options = [contract_id_opt]

    def handle(self) -> None:
        if self.option("contract_id"):
            contract_id = self.option("contract_id")
        else:
            question = self.create_question(
                "Введите id (идентификатор) договора для завершения: "
            )
            contract_id = self.ask(question)

        if not contract_facade.is_existing(contract_id):
            self.line(
                "<error>Договор с таким id (идентификатором) не существует</error>"
            )
            return

        if not contract_facade.is_active(contract_id):
            self.line(
                f"<error>Можно завершить подтвержденный договор</error>"
            )
            return

        contract_facade.complete(contract_id)
