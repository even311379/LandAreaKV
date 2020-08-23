from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy_garden.mapview import MapView, MapSource, MapMarker, geojson, MapLayer
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Line, Color
from kivy.lang import Builder

import Utils

import json
import shapely.geometry as sg
import area

# import kivy.resources
# from kivy.core.text import LabelBase
# kivy.resources.resource_add_path('.')
 

# kivy.resources.resource_add_path(".")
# font1 = kivy.resources.resource_find("NotoSansCJKtc-DemiLight.otf")
# #
# # #通过labelBase
# LabelBase.register("NS_labelBase","NotoSansCJKtc-DemiLight.otf")
# kivy.core.text.Label.register("NS_label","NotoSansCJKtc-DemiLight.otf")

Builder.load_file('Layout.kv')


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    

class AppContent(MDFloatLayout):
    
    map = ObjectProperty()
    edit_btn = ObjectProperty()
    area_info = ObjectProperty()

    editmode = False
    marker_point = []
    marker_lonlat = []

    def toggle_editmode(self):
        if self.editmode:
            self.editmode = False
            self.edit_btn.icon = "pen-plus"
            
        else:
            self.editmode = True
            self.edit_btn.icon = "pen-off"
    

    def on_touch_down(self, touch):
        if self.editmode:

            # if touch(x, y is located inside finish edit btn)
            if touch.x > self.edit_btn.x and touch.x < self.edit_btn.right and touch.y > self.edit_btn.y and touch.y < self.edit_btn.top:
                self.edit_btn.on_touch_down(touch)

            
                                                   
        else:
            super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.editmode:
            print(touch.x, touch.y)
            print(self.map.get_bbox())
            if self.marker_point:
                self.canvas.after.clear()
                with self.canvas.after:
                    Color(1, 0.76, 0.98,1)
                    Line(points=self.marker_point+[touch.x, touch.y],width=3)
                      
        else:
            super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.editmode:
            # print(self.map.ids)
            if not self.IsInsideBtns(touch.x, touch.y):
                m_lat, m_lon = self.map.get_latlon_at(touch.x, touch.y)
                self.marker_point = [touch.x, touch.y]     
                self.canvas.after.clear()           
                self.marker_lonlat.append([m_lon, m_lat])
                marker = MapMarker()
                marker.lat = m_lat
                marker.lon = m_lon
                marker.source = 'marker.png'
                # marker.bind(on_press=self.test)
                marker.id = str(m_lat)
                self.map.add_marker(marker)
                # print(len(self.marker_lonlat))
                # print(self.marker_lonlat)
            for child in self.map.children:
                if type(child) == geojson.GeoJsonMapLayer:
                    self.map.remove_widget(child)
                
            if (len(self.marker_lonlat) > 2):
                geoj_layer = geojson.GeoJsonMapLayer(geojson=json.loads(Utils.create_GeoJson(self.marker_lonlat)))
                self.map.add_widget(geoj_layer)
                self.map.center_on(self.map.lat+0.0001, self.map.lon+0.0001)
                obj = {'type': 'Polygon', 'coordinates': [self.marker_lonlat]}
                polygon_area = round(area.area(obj),2)
                self.area_info.text = f'目前面積： {polygon_area} 平方公尺'
                # if 'geoj_layer' in self.map.ids:
                #     print(123)
                #     self.map.remove_widget(self.ids.jlayer)
                # else:
                #     print(456)
        else:
            super().on_touch_up(touch)
    
    def IsInsideBtns(self, x, y):
        bs = []
        # edit_btn
        bs.append(x > self.edit_btn.x and x < self.edit_btn.right and y > self.edit_btn.y and y < self.edit_btn.top)

        return sum(bs)>0

    def test(self):
        print('test')


class AppScreen(Screen):

    content = ObjectProperty()
    nav_drawer = ObjectProperty()



class MainApp(MDApp):    

    device_width = NumericProperty()
    devide_height = NumericProperty()

    def on_start(self):
        self.theme_cls.primary_palette = 'BlueGray'
  
    def build(self):
        self.device_width, self.device_height = Window.size
        app = AppScreen()
        source = MapSource(url="http://mt0.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}", maxZoom=20)
        app.content.map.map_source = source        
        return app

        

    def open_drawer(self):
        pass
        

if __name__ == "__main__":
    MainApp().run()