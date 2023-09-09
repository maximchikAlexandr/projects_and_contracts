from cleo.application import Application

from src.commands.contract import (
    CreateContractCommand,
    ListContractCommand,
    ActivateContractCommand,
    CompleteContractCommand,
)

application = Application()
application.add(CreateContractCommand())
application.add(ListContractCommand())
application.add(ActivateContractCommand())
application.add(CompleteContractCommand())

if __name__ == "__main__":
    application.run()
