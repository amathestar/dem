"""Development Environment Catalog."""
# dem/core/dev_env_catalog.py

from dem.core.dev_env import DevEnv
from dem.core.data_management import ConfigFile
import requests

class DevEnvCatalog():
    """ Development Environment Catalog. """
    def __init__(self, url: str) -> None:
        """ Init the class with the DevEnvs available in the catalog. 

            Args:
                url -- the url of the catalog
        """
        self.url: str = url
        self.dev_envs: list[DevEnv] = []
        for dev_env_descriptor in requests.get(url).json()["development_environments"]:
            self.dev_envs.append(DevEnv(descriptor=dev_env_descriptor))

    def get_dev_env_by_name(self, dev_env_name: str) -> DevEnv | None:
        """ Get the Development Environment by name.
        
            Args:
                dev_env_name -- name of the Development Environment to get
            Return with the instance representing the Development Environment. If the Development 
            Environment doesn't exist in the catalog, return with None.
        """
        for dev_env in self.dev_envs:
            if dev_env.name == dev_env_name:
                return dev_env

class DevEnvCatalogs():
    """ List of the available Development Environment Catalogs. """
    def __init__(self, config_file: ConfigFile) -> None:
        """ Init the class with the catalogs from the config file.

            Args:
                config_file -- contains the catalog descriptions
            """
        self._config_file: ConfigFile = config_file
        self.catalogs: list[DevEnvCatalog] = []
        for catalog_config in config_file.catalogs:
            self.catalogs.append(DevEnvCatalog(catalog_config["url"]))

    def add_catalog(self, catalog_config: dict) -> None:
        """ Add a new catalog.
        
            Args:
                catalog_config -- the new catalog to add
        """
        self.catalogs.append(DevEnvCatalog(catalog_config["url"]))

        self._config_file.catalogs.append(catalog_config)
        self._config_file.flush()

    def list_catalog_configs(self) -> list[dict]:
        """ List the catalog configs. (As stored in the config file.)
        
            Return with the list of the available catalog configurations.
        """
        return self._config_file.catalogs