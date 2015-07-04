try:
    import yaml
    import yaml.scanner
except ImportError:
    raise exc.FiletypeNotSupportedException(
        "You have not installed the PyYAML library. Install it via `pip install PyYAML`.")

from .ConfigFile import ConfigFile, NetworkedConfigObject

from . import exc

from .ConfigGenerator import GenerateConfigFile, GenerateNetworkedConfigFile


def cload_safe(fd):
    """
    Wrapper for the YAML Cloader.
    :param fd: The file descriptor to open.
    :return: The YAML dict.
    """
    return yaml.load(fd, Loader=yaml.CSafeLoader)


def cload_load(fd):
    """
    Wrapper for the YAML Cloader.
    :param fd: The file descriptor to open.
    :return: The YAML dict.
    """
    return yaml.load(fd, Loader=yaml.CLoader)


def yaml_load_hook(load_net: False):
    def actual_load_hook(cfg: ConfigFile):
        # Should we safe load the file using YAML's Safe loader?
        # This is always on by default, for security reasons.
        if cfg.safe_load:
            # Assign 'loader' to the safe YAML CSafeLoader.
            if yaml.__with_libyaml__:
                loader = cload_safe
            else:
                loader = yaml.safe_load
        # Otherwise, use the YAML CLoader.
        else:
            if yaml.__with_libyaml__:
                loader = cload_load
            else:
                loader = yaml.load
        # Setup dumper.
        if yaml.__with_libyaml__:
            cfg.dumper = yaml.CDumper
        else:
            cfg.dumper = yaml.Dumper
        # Load the YAML file.
        try:
            if not load_net:
                data = loader(cfg.fd)
            elif load_net and isinstance(cfg, NetworkedConfigObject):
                data = loader(cfg.request.text)
            else:
                raise exc.LoaderException("No data source to load from.")
        except UnicodeDecodeError:
            raise exc.LoaderException("Selected file was not in a valid encoding format.")
        except yaml.scanner.ScannerError:
            raise exc.LoaderException("Selected file had invalid YAML tokens.")
        # Serialize the data into new sets of ConfigKey classes.
        cfg.config.load_from_dict(data)
    return actual_load_hook

def yaml_dump_hook(cfg):
    """
    Dumps all the data into a YAML file.
    """
    name = cfg.fd.name
    cfg.fd.close()
    cfg.fd = open(name, 'w')

    data = cfg.config.dump()
    yaml.dump(data, cfg.fd, Dumper=cfg.dumper, default_flow_style=False)
    cfg.reload()


YAMLConfigFile = GenerateConfigFile(load_hook=yaml_load_hook(False), dump_hook=yaml_dump_hook)
NetworkedYAMLConfigFile = GenerateNetworkedConfigFile(load_hook=yaml_load_hook(True),
                        normal_class_load_hook=yaml_load_hook(True), normal_class_dump_hook=yaml_dump_hook)