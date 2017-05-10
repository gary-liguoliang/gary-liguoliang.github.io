---
layout: post
title:  "IntelliJ: How to support customized Cucumber feature file extension"
---

## Requirement
as a heavy user of Cucumber, I created customized feature file (e.g. .feature2) for my enhancment. I want to add support to customized feature file with IntelliJ and Cucumber plugin.

## Solution

the [IntelliJ Cucumber plugin](https://github.com/JetBrains/intellij-plugins/tree/master/cucumber) is created by JetBrains with '[Apache License 2.0](https://github.com/JetBrains/intellij-plugins/blob/master/cucumber/LICENSE.txt)'

so we can download, modify, redistribute it. 

before you proceed to downloading, you may want to select the brache with your IntellJ version.


**Step 1. Override the `CucumberFileTypeFactory`**
    instead of modifying the original code `CucumberFileTypeFactory`, I prefer to extend it:

```java
package aqua;

import com.intellij.openapi.fileTypes.ExtensionFileNameMatcher;
import com.intellij.openapi.fileTypes.FileTypeConsumer;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.plugins.cucumber.psi.CucumberFileTypeFactory;
import org.jetbrains.plugins.cucumber.psi.GherkinFileType;

public class AquaFileTypeFactory extends CucumberFileTypeFactory{
    @Override
    public void createFileTypes(@NotNull FileTypeConsumer consumer) {
        consumer.consume(GherkinFileType.INSTANCE, new ExtensionFileNameMatcher("feature"), new ExtensionFileNameMatcher("feature2"));
    }
}
```

**Step 2. Register the `FileTypeFactory` created in Step 1 in `src/META-INF/plugin.xml**

```xml
<idea-plugin version="2">
    <id>gherkin</id> <!-- I prefer to keep this id so that other plugins can continue to depend on it -->
    <name>Gherkin-AQUA</name>
    <fileTypeFactory implementation="aqua.AquaFileTypeFactory"/>
</idea-plugin>
``` 

then you may [build your plugin redistribute it](https://www.jetbrains.com/help/idea/2017.1/preparing-plugins-for-publishing.html)!
