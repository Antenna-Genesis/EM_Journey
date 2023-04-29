import win32gui,win32con
import time
def get_hwnd_dic(hwnd, hwnd_title):
    if (win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd)
            and win32gui.GetWindowText(hwnd)):
        hwnd_title[f"{hwnd}"] = win32gui.GetWindowText(hwnd)

def get_hwnd():
    """
    :return: {hwnd:title}
    """
    hwnd_title = {}
    win32gui.EnumWindows(get_hwnd_dic, hwnd_title)
    return hwnd_title
#获取所有窗口句柄

def close_cst_window(projectname='DRAtest'):
    #关掉cst窗口
    fname=projectname+' - CST Studio Suite'
    hwnd = win32gui.FindWindow(None, fname)
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

def is_CST_open(projectname='DRAtest'):
    #判断CST窗口是否成功打开
    fname = projectname + ' - CST Studio Suite'
    hwndJson = get_hwnd()
    bb=0
    for ww in hwndJson.values():
        if fname==ww:
            bb=1
            break
    if bb==1:
        return True
    else:
        return False

if __name__ == "__main__":
    hwndJson = get_hwnd()
    print(hwndJson)
    time.sleep(1)
    print(is_CST_open())
    # hwnd= win32gui.FindWindow(None, 'DRAtest - CST Studio Suite')
    # win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)
