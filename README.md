# LandAreaKV
a andriod app developed by kv framework

---
Notes for building android by buildozer:

Buildozer should be installed on system, than in vitural environments.

Don't use kivy.garden for mapview, instead just install mapview:

```
pip install mapview
```
then, import kivy_garden.mapview instead of kivy.garden.mapview...


how to fix **ReferenceError: weakly-referenced object no longer exists**
1. Must manualy load kv file
2. Size of layout can not bigger than device size

---
Bugs:

add geojson layer to mapview is actually working...
but you have to move map for any bit...otherwise, the new added layer will not display.

---
Issues:

(1) get understand with the unit of size in kivy, for better offset toolbar width on andriod device
(2) fix duplicate layers when use builder to load kv file...