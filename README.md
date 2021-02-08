Vad är detta?
Detta är en custom components för att hämta temperaturer från http://temperatur.nu/ via det officiella APIet. Läs mer om APIet och villkoren här: http://wiki.temperatur.nu/index.php/API

Vad gör den?
Komponenten använder sig av configuration.yaml för att avgöra vilka temperaturer som ska hämtas. Konfigurationen görs som en sensor med namn på respektive sensor som argument. Namnet hämtas från http://temperatur.nu genom att välja en mästation och använda namnet från URL.
```  - platform: temperatur_nu
       name:
         - bjuv
         - toltorpsdalen
         - vikingstad```
