package com.huy.Config;
import com.huy.App;
import com.huy.Config.config;
import com.huy.Shared.helper;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.yaml.snakeyaml.LoaderOptions;
import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.constructor.Constructor;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;


public class configHandler {
    private static final InputStream config = helper.getResources("Config/yaml/config.yaml");
    public static config CONFIG;
    public static void loadConfig(){
        Constructor constructor = new Constructor(config.class, new LoaderOptions());
        Yaml yaml = new Yaml(constructor);
        CONFIG = yaml.load(config);
    }
}
