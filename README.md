# Projects and Contracts 
## О проекте

Тестовое задание для стажировки в iCode

## Установка

Склонировать репозиторий с GitHub:

```sh
git clone https://github.com/maximchikAlexandr/projects_and_contracts.git
```

Перейти в директорию с проектом:

```sh
cd projects_and_contracts/
```

**Дальнейшая установка требует запущенного Docker**

### Linux

Сделать исполняемым файл со скриптом и запустить его:

```bash
chmod +x install.sh && ./install.sh
```

### Windows

Запустить файл со скриптом:

```powershell
./install.cmd
```

Данные скрипты создают файл **.env** с переменными окружения.
В переменных окружения сохранены тестовые параметры БД, для реальной
работы переменные окружения необходимо изменить


## Использование

#### Начало работы

Для начала работы нужно войти в докер контейнер приложения:

```bash
docker exec -it pc_app bash
```

#### Работа с проектами

- Для создания проекта введите команду:
```bash
project create
```
После чего приложение попросит ввести название проекта. Альтернатива - сразу передать название 
проекта через опцию консольной команды:

```bash
project create -t "Тестовый проект"
```
```bash
project create --title="Тестовый проект"
```
- Для добавления договора к проекту:
```bash
project addcontract
```
и затем ввести id договора и id проекта. Альтернатива:
```bash
project addcontract -p 1 -c 1
```
```bash
project addcontract --project_id=1 --contract_id=1
```
- Завершить активный договор, связанный с проектом (он всегда один, согласно ТЗ):
```bash
project completecontract
```
и затем ввести id проекта. Альтернатива:
```bash
project completecontract -p 1
```
```bash
project completecontract --project_id=1
```
- Просмотреть список всех проектов:
```bash
project ls
```

#### Работы с договорами

- Для создания договора введите команду:
```bash
contract create
```
После чего приложение попросит ввести название договора. Альтернатива - сразу передать название 
договора через опцию консольной команды:

```bash
contract create -t "Тестовый договор"
```
```bash
contract create --title="Тестовый договор"
```

- Для подтверждения договора:
```bash
contract act
```
и затем ввести id договора. Альтернатива:
```bash
contract act -c 1
```
```bash
contract act --contract_id=1
```

- Для завершения договора:
```bash
contract complete
```
и затем ввести id договора. Альтернатива:
```bash
contract complete -c 1
```
```bash
contract complete --contract_id=1
```
- Просмотреть список всех договоров:
```bash
contract ls
```
#### Завершение работы
Чтобы завершить работу с программой, нужно выйти докер контейнера:

```bash
exit
```

## Уровень логирования SQLAlchemy

Чтобы приложение выводило в консоль SQL запросы, нужно 
изменить переменную окружения в файле **.env**:

```bash
SQLALCHEMY_LOG_LEVEL=INFO
```