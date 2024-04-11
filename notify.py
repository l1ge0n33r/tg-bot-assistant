from windows_toasts import Toast, WindowsToaster
from datetime import datetime
toaster = WindowsToaster("Zalupa")
newToast = Toast()
c = datetime.today().strftime('%Y-%m-%d')
print(c)
newToast.text_fields= [f'{c}']
newToast.on_activated = lambda _: print("AAAAAAAAAAA")
toaster.show_toast(newToast)
toaster.schedule_toast