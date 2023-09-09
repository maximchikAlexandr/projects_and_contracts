from cleo.application import Application

from src.commands.project import (
    AddContractCommand,
    CompleteActiveContractCommand,
    CreateProjectCommand,
    ListProjectCommand,
)

application = Application()
application.add(CreateProjectCommand())
application.add(ListProjectCommand())
application.add(AddContractCommand())
application.add(CompleteActiveContractCommand())


if __name__ == "__main__":
    application.run()
