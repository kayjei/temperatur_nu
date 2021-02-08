<h1>Vad är detta?</h1>
Detta är en custom components för att hämta temperaturer från http://temperatur.nu/ via det officiella APIet. Läs mer om APIet och villkoren här: http://wiki.temperatur.nu/index.php/API

<h1>Vad gör den?</h1>

```temperatur_nu``` skapar en sensor i Home Assistant för varje sensor som konfigurerats att hämtas. Temperaturen uppdateras därefter var 10:e minut. Alla sensorer visas på kartan i komponenten ```map```.<br><br>

<h1>Installation och konfiguration</h1>
Komponenten installeras som en custom_component eller via HACS.<br>
Komponenten använder sig av configuration.yaml för att avgöra vilka temperaturer som ska hämtas. Konfigurationen görs som en sensor med namn på respektive sensor som argument. Namnet hämtas från http://temperatur.nu genom att välja en mätstation och använda namnet från URL. Om inget namn anges som argument kommer komponenten inte att starta.<br><br>

![alt text](https://github.com/kayjei/temperatur_nu/blob/main/temp_nu_1.JPG?raw=true)
<br><br>
![alt text](https://github.com/kayjei/temperatur_nu/blob/main/temp_nu.JPG?raw=true)

```
sensor:
  - platform: temperatur_nu
    name:
      - bjuv
      - toltorpsdalen
      - vikingstad
```
<br><br>
![alt text](http://wiki.temperatur.nu/images/2/27/Www.temperatur.nu.gif?raw=true)
