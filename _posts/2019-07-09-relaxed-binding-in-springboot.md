---
layout: post
title:  "Relaxed Binding of Type-safe Configuration Properties in Spring Boot 1.5"
date:  2019-07-09 18:00:00 +0800
categories: dev
tags:
 - java
 - spring
---

## Question: what's the output?

Given this application.yml:
```
freeMarker: # with upper-case M
  templatePath: "/freeMarker/upper-case"
 
freemarker:
  templatePath: "/freemarker/lower-case"
```

and this configuration bean:

```
@Component
@ConfigurationProperties(prefix = "freeMarker")
public class FreeMarkerConfigurationSettings {
 
    String templatePath;
 
    public String getTemplatePath() {
        return templatePath;
    }
 
    public void setTemplatePath(String templatePath) {
        this.templatePath = templatePath;
    }
}
```
**what's the output of this snippet?**

```
@Component
public class PropertiesPrinter implements CommandLineRunner {
 
    @Autowired
    FreeMarkerConfigurationSettings freeMarkerConfigurationSettings;
 
    @Override
    public void run(String... strings) throws Exception {
        System.out.println("templatePath using ConfigurationProperties: " + freeMarkerConfigurationSettings.templatePath);
    }
}
```

looks like the property should be resolved to "/freeMarker/upper-case", but actually it's not.  the output is:

`templatePath using ConfigurationProperties: /freemarker/lower-case`

## What? I found a bug in Spring Boot?

No. actually this is a feature: https://docs.spring.io/spring-boot/docs/current/reference/html/boot-features-external-config.html#boot-features-external-config-relaxed-binding
> Spring Boot uses some relaxed rules for binding Environment properties to @ConfigurationProperties beans, so there does not need to be an exact match between the Environment property name and the bean property name. Common examples where this is useful include dash-separated environment properties (for example, context-path binds to contextPath), and capitalized environment properties (for example, PORT binds to port).

ok, it's a feature, then how does Spring boot choose the one? (from a list of candidates?)

I didn't find documents with concrete details, so I digged into the source code. Spring did the magic during property binding which is part of the 'auto-wired' initialisation:
getPropertyValuesForNamePrefix finds the final property value from a list of candidates with a list of "RelaxedNames", i.e the 2 "propertyValues" we defined in the application.yml:


```
private MutablePropertyValues getPropertyValuesForNamePrefix(
      MutablePropertyValues propertyValues) {
   if (!StringUtils.hasText(this.namePrefix) && !this.ignoreNestedProperties) {
      return propertyValues;
   }
   MutablePropertyValues rtn = new MutablePropertyValues();
   for (PropertyValue value : propertyValues.getPropertyValues()) {
      String name = value.getName();
      for (String prefix : new RelaxedNames(stripLastDot(this.namePrefix))) {
         for (String separator : new String[] { ".", "_" }) {
            String candidate = (StringUtils.hasLength(prefix) ? prefix + separator
                  : prefix);
            if (name.startsWith(candidate)) {
               name = name.substring(candidate.length());
               if (!(this.ignoreNestedProperties && name.contains("."))) {
                  PropertyOrigin propertyOrigin = OriginCapablePropertyValue
                        .getOrigin(value);
                  rtn.addPropertyValue(new OriginCapablePropertyValue(name,
                        value.getValue(), propertyOrigin));
               }
            }
         }
      }
   }
   return rtn;
}
```

what is the "RelaxedNames" for "freeMarker" we defined in our configuration bean? 


```
values = {LinkedHashSet@3080} size = 7
 0 = "freeMarker"
 1 = "free_marker"
 2 = "free-marker"
 3 = "freemarker"
 4 = "FREEMARKER"
 5 = "FREE_MARKER"
 6 = "FREE-MARKER"
```

I would say that "rtn.addPropertyValue()" is not a good name:
```
/**
 * Add a PropertyValue object, replacing any existing one for the
 * corresponding property or getting merged with it (if applicable).
 * @param pv PropertyValue object to add
 * @return this in order to allow for adding multiple property values in a chain
 */
public MutablePropertyValues addPropertyValue(PropertyValue pv) {
   for (int i = 0; i < this.propertyValueList.size(); i++) {
      PropertyValue currentPv = this.propertyValueList.get(i);
      if (currentPv.getName().equals(pv.getName())) {
         pv = mergeIfRequired(pv, currentPv);
         setPropertyValueAt(pv, i);
         return this;
      }
   }
   this.propertyValueList.add(pv);
   return this;
}
```

> "Add a PropertyValue object, replacing any existing one for the corresponding property or getting merged with it (if applicable)."


Spring boot resolves the property's value by comparing each properties with a list of "RelaxedNames" and the return the last one it found. 

## Conclusions
 - Relaxed binding is a nice feature, but it could confuse you with the resolved value: 
spring boot will return the last found property's value based on the list of "RelaxedNames"
 - Choose better "prefix" names. e.g. "freemarker" is too general, "obsFreemarker" is better.

