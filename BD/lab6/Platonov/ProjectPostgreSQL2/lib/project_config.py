# Загрузка настроек проекта (в данном случае только настроек соединения с БД)
# из файла config.yaml.
import yaml

class ProjectConfig:
    """Класс считывает базовые настройки из файла config.yaml"""

    def __init__(self):
        with open('config/config.yaml') as f:
            config = yaml.safe_load(f)
            self.dbname = config['dbname']
            self.user = config['user']
            self.password = config['password']
            self.host = config['host']
            self.dbtableprefix = config['dbtableprefix']
            self.port = config['port']
            # Добавил распознавание порта из конфига, т к у меня запущены 2 постгресса, можно потом убрать

# Этот метод запускается только, если запускать
# данный файл, а не подключать его.
if __name__ == "__main__":
    x = ProjectConfig()
    #print(x.dbfilepath)
