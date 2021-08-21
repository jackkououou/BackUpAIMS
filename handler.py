from __future__ import annotations
from abc import ABC, abstractmethod
from PyQt5 import QtCore, QtGui, QtWidgets
from requests.models import encode_multipart_formdata
from Album import Album
from gsheets import Gsheet
import urllib.request
from AlbumPopUp import Ui_Dialog
from WareHousePopUp import Ui_Warehous_Dialog

class Mediator(ABC):
    def notify(self, sender: object, event : str):
        #model function, filled in by children, damn lazy parents
        pass
    
class BaseComponent:
    def __init__(self, mediator: Mediator = None):
        self._mediator = mediator
        
    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator

class SearchUtil(BaseComponent):
    def __init__(self, artist : QtWidgets.QLineEdit, title : QtWidgets.QLineEdit):
        super().__init__(mediator = None)
        self._artist = artist.text()
        self._album = title.text()
        self._sheet = Gsheet()
        self._alb_obj = None
        
    def search_album(self):
        if(self._sheet.album_exist(artist=self._artist, album=self._album)):
            self.mediator.notify(self, 'IN_SHEET')
        else:
            self.mediator.notify(self, 'NOTIN_SHEET')
            
    def gsheets_fetch_album(self, alb_obj : Album):
        self._sheet.get_album_data(title=self._album, artist=self._artist, obj= alb_obj)
        print (alb_obj)
        
    def lfm_fetch_album(self) -> Album:
        alb_obj = Album(self._artist, self._album)
        print(alb_obj)
        self._alb_obj = alb_obj
        return alb_obj

class CastAlbumUtil(BaseComponent):
    def __init__(self, dialog_object : Ui_Dialog):
        super().__init__(mediator= None)
        self._dialog = dialog_object
    
    def cast_album(self):
        self.mediator.notify(self, 'CASTING_ALBUM')
        
    def cast_to_screen(self, alb_obj : Album):
        url = alb_obj.get_art()
        data = urllib.request.urlopen(url).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        self._dialog.AlbumImage.setPixmap(QtGui.QPixmap(image))
        self._dialog.AlbumName.setText(alb_obj.get_album_title())
        self._dialog.ArtistName.setText(alb_obj.get_album_artist())
        self._dialog.alb_artist = f'{alb_obj.get_album_artist()}'
        self._dialog.alb_title = f'{alb_obj.get_album_title()}'
        genres = alb_obj.get_genres()
        for genre in genres:
            self._dialog.listWidget.addItem(genre)
        
        tracks = alb_obj.get_tracks()
        for index, track in enumerate(tracks):
            self._dialog.listWidget_2.addItem(f"{index + 1}. {track}")
        
        is_in = int(alb_obj.get_total())
        Dialog = QtWidgets.QDialog()
        if (is_in > -1) :
            self._dialog.Genre.setText('Album is in inventory')
            self._dialog.AddButton.setText('Album exists')
            self._dialog.AddButton.setEnabled(False)
            
            
            
        
        
        
        self._dialog.setupUi(Dialog)
        Dialog.show()


class UtilMediator(Mediator):
    _alb_obj = Album()
    _table = []        
    def __init__(self, search : SearchUtil, caster : CastAlbumUtil):
        
        self._search_component = search
        self._search_component.mediator = self
        self._caster_component = caster
        self._caster_component.mediator = self
        
    def notify(self, sender: object, event: str):
        
        if event == 'IN_SHEET':
            print('In gsheet... extracting')
            self._search_component.gsheets_fetch_album(self._alb_obj)
        
        if event == 'NOTIN_SHEET':
            print('Not in gsheet... fetching from Lfm')
            self._alb_obj = self._search_component.lfm_fetch_album()
        
        if event == 'CASTING_ALBUM':
            if self._alb_obj == None:
                print('No Album Obj')
            else:
                print('Showing album')
                self._caster_component.cast_to_screen(self._alb_obj)
        
class WareMediator(Mediator):
    
    def __init__(self, handler : WarehouseLoader, caster : CastWarehouse):
        self._handler = handler
        self._handler.mediator = self
        self._caster = caster
        self._caster.mediator = self
        self._table = []
    
    def notify(self, sender : object, event : str):
        if event == 'SET_TABLE':
            self._handler.set_table(self._table)
        if event == 'CAST_TABLE':
            self._caster.cast_table_to_screen(self._table)
        
class WarehouseLoader(BaseComponent):
    def __init__(self):
        super().__init__(mediator= None)
        self._sheet = Gsheet()
        self._sheet.refresh()
        self._block = []
        
    def download_sheet(self):
        self.mediator.notify(self, 'SET_TABLE')
        
    def set_table(self, table : list):

        self._sheet.refresh()
        self._block = self._sheet.inv_extract
        
        
        for row_index, row in enumerate (self._block) :
           table.append([])
           table[row_index].append(row[1])
           table[row_index].append(row[0])
           table[row_index].append(row[5])
           table[row_index].append(row[6])
           table[row_index].append(row[7])
        
        
class CastWarehouse(BaseComponent):
    def __init__(self, dialog_obj : Ui_Warehous_Dialog):
        super().__init__(mediator= None)
        self._dialog = dialog_obj
        
    def cast_table(self):
        self.mediator.notify(self, 'CAST_TABLE')
        
    def cast_table_to_screen(self, table : list):
        self._dialog.tableWidget.setRowCount(len(table))
        for row_index, row in enumerate(table):
            self._dialog.tableWidget.setItem(row_index , 0 , QtWidgets.QTableWidgetItem(row[0]))
            self._dialog.tableWidget.setItem(row_index , 1 , QtWidgets.QTableWidgetItem(row[1]))
            self._dialog.tableWidget.setItem(row_index , 2 , QtWidgets.QTableWidgetItem(row[2]))
            self._dialog.tableWidget.setItem(row_index , 3 , QtWidgets.QTableWidgetItem(row[3]))
            self._dialog.tableWidget.setItem(row_index , 4 , QtWidgets.QTableWidgetItem(row[4]))
        
        
