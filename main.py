from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.garden.mapview import MapView, MapSource, MapMarkerPopup
from kivy.properties import ObjectProperty
from kivy.clock import Clock

class AreaCalcMap(MapView):
    
    def tick(self, *args):
        pass
        # print('a tick function in map')
    

class AppContent(MDFloatLayout):
    
    map = ObjectProperty()
    edit_btn = ObjectProperty()

    editmode = False
    
    def __int__(self):
        super(AppContent, self).__init__(**kwargs)

        
        # source = MapSource(url="http://mt0.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}", maxZoom=20)
        # self.map.map_source = source

    def tick(self, *args):
        print('hey')
    
    # def on_touch_down(self, touch):
    #     print('touched')
    def toggle_editmode(self):
        print('start to edit polygon')
        self.editmode = not self.editmode
        print(self.edit_btn.x, self.edit_btn.y, self.edit_btn.right, self.edit_btn.top)



    def on_touch_down(self, touch):
        if self.editmode:
            print(touch.x, touch.y)
            print(self.map.get_bbox())
            # if touch(x, y is located inside finish edit btn)
            if touch.x > self.edit_btn.x and touch.x < self.edit_btn.right and touch.y > self.edit_btn.y and touch.y < self.edit_btn.top:
                self.toggle_editmode()
                print('something is happen')
                                    
        else:
            super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.editmode:
            print(touch.x, touch.y)
            print(self.map.get_bbox())                        
        else:
            super().on_touch_move(touch)
    
    #btn functions:
    # def btn_toggle_editmode(self):
        #print(instance)
        # self.toggle_editmode()


class MainApp(MDApp):

    def on_start(self):
        self.theme_cls.primary_palette = 'BlueGray'
  
    def build(self):
        content = AppContent()
        source = MapSource(url="http://mt0.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}", maxZoom=20)
        content.map.map_source = source
        Clock.schedule_interval(content.map.tick,1/30)
        return  content
        

if __name__ == "__main__":
    MainApp().run()