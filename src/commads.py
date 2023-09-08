import click

from src.db.settings import EngineDB
from src.facades import ContractFacade, ProjectFacade
from src.renders import to_render_table

engine_db = EngineDB()
contract_facade = ContractFacade(engine_db=engine_db)
project_facade = ProjectFacade(engine_db=engine_db)


@click.group()
def cli():
    pass


@cli.group("contract")
def contract():
    pass


@cli.group("project")
def project():
    pass


@project.command("create")
@click.option("--title", "-t", prompt="Введите название проекта")
def create(title):
    project_facade.create(title)


@project.command("ls")
def ls():
    data = project_facade.get_all_projects()
    table = to_render_table(data)
    click.echo(table)


def get_unlinked_active_contracts_prompt():
    data = contract_facade.get_unlinked_active_contracts()
    table = to_render_table(data)
    return str(table) + "\nВведите id (идентификатор) договора"


def get_all_projects_prompt():
    data = project_facade.get_all_projects()
    table = to_render_table(data)
    return str(table) + "\nВведите id (идентификатор) проекта"


@project.command("addcontract")
@click.option("--project_id", "-pid", prompt=get_all_projects_prompt())
@click.option("--contract_id", "-cid", prompt=get_unlinked_active_contracts_prompt())
def addcontract(project_id, contract_id):
    check = (
        contract_facade.is_existing(contract_id),
        contract_facade.is_active(contract_id),
        project_facade.is_existing(project_id),
        not project_facade.has_active_contracts(project_id),
    )
    if all(check):
        project_facade.add_contract(project_id, contract_id)
    else:
        click.echo("Неверные данные")


@contract.command("create")
@click.option("--title", "-t", prompt="Введите название договора")
def create(title):
    contract_facade.create(title)


@contract.command("act")
@click.option("--contract_id", "-cid", prompt="Введите id (идентификатор) договора")
def act(contract_id):
    contract_facade.approve(contract_id)


def get_fin_prompt():
    data = contract_facade.get_linked_active_contracts()
    table = to_render_table(data)
    return str(table) + "\nВведите id (идентификатор) договора"


@contract.command("fin")
@click.option("--contract_id", "-cid", prompt=get_fin_prompt())
def fin(contract_id):
    contract_facade.complete(contract_id)


@contract.command("ls")
def ls():
    data = contract_facade.get_all_contracts()
    table = to_render_table(data)
    click.echo(table)
