# 客製化的影像擷取程式
import cv2
import threading
import numpy as np
import platform as plt

class CustomVideoCapture():

    # 初始化 預設的攝影機裝置為 0
    def __init__(self, dev=0):
        self.cap = cv2.VideoCapture(dev)
        self.ret = ''
        self.frame = []     
        self.win_title = 'Modified with set_title()'
        self.info = ''
        self.isStop = False
        self.t = threading.Thread(target=self.video, name='stream')

    # 可以透過這個函式 開啟 Thread 
    def start_stream(self):
        self.t.start()
    
    # 關閉 Thread 與 Camera
    def stop_stream(self):
        self.isStop = True
        self.cap.release()
        cv2.destroyAllWindows()
    
    # 取得最近一次的幀
    def get_current_frame(self):
        return self.ret, self.frame
    
    # 設定顯示視窗的名稱
    def set_title(self, txt):
        self.win_title = txt

    # Thread主要運行的函式
    def video(self):
        # try:
            global close_thread
            close_thread = 0

            frame_rate = int(self.cap.get(cv2.CAP_PROP_FPS))
          

            while not self.isStop:
                self.ret, self.frame = self.cap.read()
                self.frame = cv2.flip(self.frame, 1)

                if self.info != '':
                    cv2.putText(self.frame, self.info, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.namedWindow(self.win_title)
                    cv2.imshow(self.win_title, self.frame)
                    cv2.resizeWindow(self.win_title, 640, 480)

                if cv2.waitKey(1) == 27:
                    break
                if close_thread == 1:
                    break

            self.stop_stream()

# 用於資料前處理的程式
def preprocess(frame, resize=(224, 224), norm=True):
    '''
    設定格式 (1, 224, 224, 3)、縮放大、正規化、放入資料並回傳正確格式的資料
    '''
    height, width, _ = frame.shape
    crop_size = min(width, height)
    x_start = (width - crop_size) // 2
    y_start = (height - crop_size) // 2
    cropped_image = frame[y_start:y_start + crop_size, x_start:x_start + crop_size]
    input_format = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    frame_resize = cv2.resize(cropped_image, resize)
    frame_norm = ((frame_resize.astype(np.float32) / 127.0) - 1) if norm else frame_resize
    input_format[0] = frame_norm
    return input_format

# 解析輸出資訊
def parse_output(preds, label):
    preds = preds[0] if len(preds.shape) == 4 else preds
    trg_id = np.argmax(preds)
    trg_name = label[trg_id]
    trg_prob = preds[trg_id]
    return (trg_id, trg_name, trg_prob)
