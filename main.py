from handler import CastAlbumUtil, CastWarehouse, Mediator, SearchUtil, UtilMediator, WarehouseLoader, WareMediator
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from aims2 import Ui_MainWindow
from AlbumPopUp import Ui_Dialog
from WareHousePopUp import Ui_Warehous_Dialog

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.ui.pushButton.clicked.connect(self.search_album_dialog)
        self.ui.load_table_button.clicked.connect(self.show_warehouse)
        
       
        
    def show(self):
        self.main_win.show()
        
    def search_album_dialog(self):
        alb_dialog = QDialog()
        alb_popup = Ui_Dialog()
        alb_popup.setupUi(alb_dialog)
        handler = SearchUtil(self.ui.ArtistName, self.ui.lineEdit)
        caster = CastAlbumUtil(alb_popup)
        mediater = UtilMediator(handler, caster)
        handler.search_album()
        caster.cast_album()
        
        alb_dialog.exec_()
        
    def show_warehouse(self):
        dialog = QDialog()
        popup = Ui_Warehous_Dialog()
        popup.setupUi(dialog)
        
        handler = WarehouseLoader()
        caster = CastWarehouse(popup)
        mediator = WareMediator(handler, caster)
        handler.download_sheet()
        caster.cast_table()
        
        dialog.exec_()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())