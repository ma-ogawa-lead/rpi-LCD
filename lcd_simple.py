# import
import smbus
import time

# LCD(I2C)の設定
# 事前確認でアドレスが27ではない場合はここを修正
LCD_ADDR = 0x27
LCD_WIDTH = 16
LCD_BACKLIGHT = 0x08

# HD44780コマンド準備
LCD_CLEAR_DISPLAY = 0x01
LCD_RETURN_HOME = 0x02
LCD_ENTRY_MODE = 0x06
LCD_DISPLAY_ON = 0x0C
LCD_DISPLAY_OFF = 0x08
LCD_CURSOR_ON = 0x0E
LCD_BLINK_ON = 0x0F
LCD_SET_DDRAM = 0x80

# PCF8574に接続されたLCDピン準備
RS = 0x01
RW = 0x02
EN = 0x04

# LCD初期化処理
def lcd_init(bus):
    # 初期化シーケンス設定
    # 4ビットモードに設定
    lcd_send(bus, 0x33, 0)
    time.sleep(0.005)
    # 4ビットモードに設定
    lcd_send(bus, 0x32, 0)
    time.sleep(0.005)

    # コマンド設定
    # 2行表示 5x8ドット
    lcd_send(bus, 0x28, 0)
    time.sleep(0.00015)
    # ディスプレイオフ
    lcd_send(bus, LCD_DISPLAY_OFF, 0)
    time.sleep(0.00015)
    # ディスプレイクリア
    lcd_send(bus, LCD_CLEAR_DISPLAY, 0)
    time.sleep(0.002)
    # エントリモード設定
    lcd_send(bus, LCD_ENTRY_MODE, 0)
    time.sleep(0.00015)
    # ディスプレイオン
    lcd_send(bus, LCD_DISPLAY_ON, 0)
    time.sleep(0.00015)

# LCDデータ送信処理
def lcd_send(bus, data, mode):
    # 上位4ビット
    high = mode | (data & 0xF0) | LCD_BACKLIGHT
    # 下位4ビット
    low = mode | ((data << 4) & 0xF0) | LCD_BACKLIGHT

    # データ送信
    bus.write_byte(LCD_ADDR, high)
    lcd_toggle_enable(bus, high)
    bus.write_byte(LCD_ADDR, low)
    lcd_toggle_enable(bus, low)

# トグル処理
def lcd_toggle_enable(bus, value):
    # Enable ON
    bus.write_byte(LCD_ADDR, value | EN)
    time.sleep(0.0005)
    # Enable OFF
    bus.write_byte(LCD_ADDR, value & ~EN)
    time.sleep(0.0005)

# カーソル位置設定処理
def lcd_set_cursor(bus, col, row):
    addr = LCD_SET_DDRAM | (col + 0x40 * row)
    lcd_send(bus, addr, 0)

# 文字列出力処理
def lcd_print(bus, text):
    for char in text:
        lcd_send(bus, ord(char), 1)

# メイン処理
def main():
    bus = smbus.SMBus(1)
    lcd_init(bus)

    # 文字列を表示
    text_line1 = "Hello, world!"
    text_line2 = "Raspberry Pi"

    lcd_set_cursor(bus, 0, 0)
    lcd_print(bus, text_line1)

    lcd_set_cursor(bus, 0, 1)
    lcd_print(bus, text_line2)

    # 待機
    time.sleep(10)
    # 表示をクリア
    lcd_send(bus, LCD_CLEAR_DISPLAY, 1)

if __name__ == "__main__":
    main()
