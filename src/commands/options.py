from cleo.helpers import option

project_id_opt = option(
    "project_id",
    "pid",
    description="id (идентификатор) проекта",
    flag=False,
)

contract_id_opt = option(
    "contract_id",
    "cid",
    description="id (идентификатор) договора",
    flag=False,
)

project_title = option(
    "title",
    "t",
    description="Название создаваемого проекта",
    flag=False,
)

contract_title = option(
    "title",
    "t",
    description="Название создаваемого договора",
    flag=False,
)
