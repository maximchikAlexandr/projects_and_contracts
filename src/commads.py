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


@cli.command()
@click.option('--title', prompt='Введите название проекта')
def createproject(title):
    project_facade.create(title)


@cli.command()
@click.option('--title', prompt='Введите название договора')
def createcontract(title):
    contract_facade.create(title)


@cli.command()
@click.option('--contract_id', prompt='Введите id (идентификатор) договора')
def approvecontract(contract_id):
    contract_facade.approve(contract_id)


@cli.command()
@click.argument('objects', default='contracts')
def ls(objects):
    if objects == 'contracts':
        data = contract_facade.get_all_contracts()
        table = to_render_table(data)
        click.echo(table)
    elif objects == "projects":
        data = project_facade.get_all_projects()
        table = to_render_table(data)
        click.echo(table)
    else:
        click.echo("Неверный ввод")
