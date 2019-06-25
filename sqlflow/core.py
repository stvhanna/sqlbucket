from sqlflow.project import Project
from sqlflow.exceptions import ProjectNotFound, ConnectionNotFound
from sqlflow.cli import load_cli
from pathlib import Path
import os


class SQLFlow:

    def __init__(
        self,
        projects_folder: str = 'projects',
        macro_folder: str = None,
        connections: dict = None,
        env_name: str = None,
        env_variables: dict = None
    ):

        self.projects_path = Path(projects_folder)
        self.macro_path = Path(macro_folder) if macro_folder is not None else None
        self.connections = connections
        self.env_name = env_name
        self.env_variables = env_variables

    def load_project(self, project_name: str, connection_name: str,
                     variables: dict = None) -> Project:
        """
        Load a project for a given project name and a given connection name.
        :param project_name
        :param connection_name
        :param variables: Typically variables submitted via CLI
        :return: Project instance
        """

        project_path = (self.projects_path / project_name).resolve()
        if not self.connection_exists(connection_name):
            raise ConnectionNotFound(f'Connection "{connection_name}" not found.')
        if not project_path.exists() or not project_path.is_dir():
            raise ProjectNotFound(f'Project "{project_name}" does not exist.')

        return Project(
            project_path=str(project_path),
            connection_url=self.connections[connection_name],
            connection_name=connection_name,
            variables=variables,
            env_name=self.env_name,
            env_variables=self.env_variables,
            macros_path=self.macro_path
        )

    def connection_exists(self, connection_name):
        if connection_name in self.connections:
            return True
        if os.environ.get(connection_name) is not None:
            return True
        return False

    def cli(self):
        command_line = load_cli(self)
        return command_line()