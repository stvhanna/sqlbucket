from sqlflow import SQLFlow, Project
from sqlflow.exceptions import ProjectNotFound, ConnectionNotFound
from pathlib import Path
import pytest
import yaml
import os


fixtures_path = Path('fixtures')


class TestSQLFlow:

    sqlflow = SQLFlow(projects_folder='projects', macro_folder='macros')

    def test_project_folder_exist(self):
        assert self.sqlflow.projects_path is not None
        assert isinstance(self.sqlflow.projects_path, Path)

    def test_macro_folder_exist(self):
        assert self.sqlflow.macro_path is not None
        assert isinstance(self.sqlflow.macro_path, Path)


class TestProjectLoading:

    sqlflow = SQLFlow(
        projects_folder='fixtures/projects',
        connections={'db_name': 'db_url'},
        env_name='dev'
    )

    def test_load_wrong_project_name(self):
        with pytest.raises(ProjectNotFound):
            self.sqlflow.load_project(
                project_name='fixture_project',
                connection_name='db_name'
            )

    def test_connection_not_found(self):
        with pytest.raises(ConnectionNotFound):
            self.sqlflow.load_project(
                project_name='project1',
                connection_name='wrong_db_name'
            )

    def test_connection_in_shell_environment(self):
        os.environ['db_in_env'] = 'db_url'
        assert self.sqlflow.connection_exists('db_in_env')

    def test_successful_project_loading(self):
        project = self.sqlflow.load_project(
            project_name='project1',
            connection_name='db_name'
        )
        assert isinstance(project, Project)


class TestConnections:
    connections_path = (fixtures_path / 'connections.yaml').resolve()
    connections = yaml.load(open(connections_path))
    sqlflow = SQLFlow(
        projects_folder='projects',
        macro_folder='macros',
        connections=connections
    )

    def test_connections_attr(self):
        assert self.sqlflow.connections is not None

    def test_get_connection(self):
        assert self.sqlflow.connections['database_1'] == 'psycopg2://database'

