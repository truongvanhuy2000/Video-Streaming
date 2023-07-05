package com.huy.Config;
import org.yaml.snakeyaml.LoaderOptions;
import org.yaml.snakeyaml.Yaml;
import com.huy.Shared.helper;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class config {
    private Map<String, String> rabbitmq = new HashMap<>();
    public config(){}
    public Map<String, String> getRabbitmq() {
        return rabbitmq;
    }
    public void setRabbitmq(Map<String, String> rabbitmq) {
        this.rabbitmq = rabbitmq;
    }
}
