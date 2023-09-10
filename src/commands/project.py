from src.commands.base import CreateEntityCommand, Command
from src.db.settings import EngineDB
from src.facades import ContractFacade, ProjectFacade
from src.commands import project_title, contract_id_opt, project_id_opt

engine_db = EngineDB()
contract_facade = ContractFacade(engine_db=engine_db)
project_facade = ProjectFacade(engine_db=engine_db)


class CreateProjectCommand(CreateEntityCommand):
    ENTITY_NAME = 'проект'
    facade = project_facade
    description = "Создает проект"
    options = [project_title]


class ListProjectCommand(Command):
    name = "ls"
    description = "Выводит список проектов"

    def handle(self) -> None:
        try:
            data = project_facade.get_all_projects()
            self.render_custom_table(data)
        except IndexError:
            self.line(
                "<comment>Таблица с проектами пуста</comment>"
            )


class AddContractCommand(Command):
    name = "addcontract"
    description = "Добавляет договор к проекту"
    options = [project_id_opt, contract_id_opt]

    def handle(self) -> None:
        active_contracts = contract_facade.get_unlinked_active_contracts()

        if not active_contracts:
            self.line(
                "<error> Нельзя начать заполнять проект без существования хотя бы одного "
                "активного договора</error>"
            )
            return

        if self.option("project_id"):
            project_id = self.option("project_id")
        else:
            data = project_facade.get_all_projects()
            self.render_custom_table(data)
            question = self.create_question(
                "Введите id (идентификатор) проекта для добавления договора: "
            )
            project_id = self.ask(question)

        if not self.is_valid_model_id(project_facade, project_id):
            return

        if project_facade.has_active_contracts(project_id):
            self.line(
                f"<error>В проекте не может быть более одного активного договора </error>"
            )
            return

        if self.option("contract_id"):
            contract_id = self.option("contract_id")
        else:
            self.render_custom_table(active_contracts)
            question = self.create_question(
                "Введите id (идентификатор) договора для добавления к проекту: "
            )
            contract_id = self.ask(question)

        if not self.is_valid_model_id(contract_facade, contract_id):
            return

        if not contract_facade.is_active(contract_id):
            self.line(
                f"<error>Добавлять в проект можно только активные договоры </error>"
            )
            return

        project_facade.add_contract(project_id, contract_id)


class CompleteActiveContractCommand(Command):
    name = "completecontract"
    description = "Завершает активный договор, связанный с выбранным проектом"
    options = [project_id_opt]

    def handle(self) -> None:
        if self.option("project_id"):
            project_id = self.option("project_id")
        else:
            question = self.create_question(
                "Введите id (идентификатор) проекта для завершения активного договора: "
            )
            project_id = self.ask(question)

        if not self.is_valid_model_id(project_facade, project_id):
            return

        if not project_facade.has_active_contracts(project_id):
            self.line(
                f"<error>В проекте нет ни одного активного договора </error>"
            )
            return

        project_facade.complete_active_contract(project_id)
