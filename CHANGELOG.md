## ConfigMaster Changelog  
[*2.0.2*:](https://bitbucket.org/SunDwarf/configmaster/commits/tag/2.0.2-stable):  
 - Fixed bug where ConfigFiles would fail on initial_populate due to an empty method.  

*2.0.1*:  
 - Converted INI config files to the new Hook format.  
 
*2.0.0*:  
 - Rewrite most of the core code.  
 - Config files now work on a hooks system.  
    - A load hook is called whenever the file is loaded. This handles loading in whatever file format the file supports.  
    - A dump hook is called whenever the file is dumped. This does the same as the loading hook, but dumps instead of loading.  
    - For networked files, a networked load hook is used for loading from the network.  
    - Additionally, networked files have normal load hooks, for save_to_file().  
  
[*1.5.0*:](https://bitbucket.org/SunDwarf/configmaster/commits/tag/1.5.0-stable)  
 - Add the ability to save networked files to disk, after downloading.  
 - Fixed .load() not being automatically called on object creation.  
 
[*1.4.0*:](https://bitbucket.org/SunDwarf/configmaster/commits/tag/1.4.0-stable)  
 - Add INI Config files.  
 - Add safer loading for ConfigKeys.  
 - Add global ConfigFile safe_load switch.  
 - Fix JSONConfigFile objects not being created properly if the file doesn't exist.  
 - Change tests to use JSONConfigFiles.  
 - Add skip conditions for tests.  


