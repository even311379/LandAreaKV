from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy_garden.mapview import MapView, MapSource, MapMarker
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Line, Color



Window.size = (540, 960)

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    

class AppContent(MDFloatLayout):
    
    map = ObjectProperty()
    edit_btn = ObjectProperty()
    editmode = False
    marker_points = []
    marker_latlon = []

    def toggle_editmode(self):
        if self.editmode:
            self.editmode = False
            self.edit_btn.icon = "pen-plus"
            
        else:
            self.editmode = True
            self.edit_btn.icon = "pen-off"
    

    def on_touch_down(self, touch):
        if self.editmode:
            print(touch.x, touch.y)
            print(self.map.get_bbox())
            # if touch(x, y is located inside finish edit btn)
            if touch.x > self.edit_btn.x and touch.x < self.edit_btn.right and touch.y > self.edit_btn.y and touch.y < self.edit_btn.top:
                self.edit_btn.on_touch_down(touch)
                                                   
        else:
            super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.editmode:
            print(touch.x, touch.y)
            print(self.map.get_bbox())
            if self.marker_points:
                self.canvas.after.clear()
                with self.canvas.after:
                    Color(0.9,0.1,0.05,1)
                    Line(points=self.marker_points+[touch.x, touch.y],width=3)

            # self.ll.points = [0,0, touch.x, touch.y]                        
        else:
            super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.editmode:
            if not self.IsInsideBtns(touch.x, touch.y):
                m_lat, m_lon = self.map.get_latlon_at(touch.x, touch.y)
                self.marker_points += touch.x, touch.y
                self.marker_latlon.append((m_lat, m_lon))
                marker = MapMarker()
                marker.lat = m_lat
                marker.lon = m_lon
                marker.source = 'marker.png'
                # marker.bind(on_press=self.test)
                self.map.add_marker(marker)
                print('is label added???')
        else:
            super().on_touch_up(touch)
    
    def IsInsideBtns(self, x, y):
        bs = []
        # edit_btn
        bs.append(x > self.edit_btn.x and x < self.edit_btn.right and y > self.edit_btn.y and y < self.edit_btn.top)

        return sum(bs)>0

    def test(self):
        print('test')
    #btn functions:
    # def btn_toggle_editmode(self):
        #print(instance)
        # self.toggle_editmode()

class AppScreen(Screen):

    content = ObjectProperty()
    nav_drawer = ObjectProperty()



class MainApp(MDApp):    

    def on_start(self):
        self.theme_cls.primary_palette = 'BlueGray'
  
    def build(self):
        # content = AppContent()
        # source = MapSource(url="http://mt0.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}", maxZoom=20)
        # content.map.map_source = source
        # Clock.schedule_interval(content.map.tick,1/30)
        # return  content
        app = AppScreen()
        source = MapSource(url="http://mt0.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}", maxZoom=20)
        app.content.map.map_source = source        
        return app

        

    def open_drawer(self):
        pass
        

if __name__ == "__main__":
    MainApp().run()