ConfigMaster
------------

## What is ConfigMaster?  
ConfigMaster is a simple library for accessing config files programmatically. No longer will you have to mess with list lookups and dict lookups when you wish to load a config file.  
Instead, objects in the file are accessed as simple class attributes.  

### What is supported

ConfigMaster natively supports JSON and YAML formats.  
The recommended format is YAML.  

### TODO
 - Add in support for python ConfigParser formats
 - <del>Add in networked JSON support</del> *Added in version 1.3.0*
 - Add more docstrings
 - Make proper documentation
 - Add tests

### How to install
For the latest stable version uploaded to PyPI, use:  
`pip install configmaster`
  
For the latest stable version uploaded to bitbucket, use:  
`pip install hg+https://bitbucket.org/SunDwarf/configmaster`  

For the latest dev version, use:  
`pip install hg+https://bitbucket.org/SunDwarf/configmaster@dev`


### How to use
ConfigMaster handles everything for you. Simply specify the location of your file, and the values will be automatically loaded for you.

```  
>>> from configmaster import YAMLConfigFile  
>>> cfg = YAMLConfigFile.YAMLConfigFile("test.yml") # Created automatically if it doesn't exist  
```  

To access config values, simply get the attribute you want from the config object stored.

```  
# YAML data is {"a": 1, "b": [1, 2], "c": {"d": 3}}  
>>> cfg.config.a  
1  
>>> cfg.config.b[1]  
2  
>>> cfg.config.c.d  
3    
```  

To populate your config data, just pass a dict to initial_populate. If the file is empty, this gives it default values, and returns True. If it isn't, nothing happens.

```
>>> pop = cfg.initial_populate({"a": 1, "b": [1, 2], "c": {"d": 3})
>>> if pop: cfg.dump() and cfg.reload() # Dump data and reload from disk.
```

To save your data, simply run .dump().

```
>>> cfg.dump()
```

Need to get the raw dict form of a ConfigKey? Use .dump() on that!

```
>>> cfg.config.dump()
{"a": 1, "b": [1, 2], "c": {"d": 3}
>>> cfg.config.c.dump()
{"d": 3}
```
