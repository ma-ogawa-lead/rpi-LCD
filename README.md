# rpi-LCD

Use LCD Display for Raspberry Pi

# 概要

I2C接続のLCDモジュール関連サンプルプログラム

# 利用ライブラリ

python3-smbus

# 利用方法

- I2Cを有効にする

`raspi-config`コマンドを実行し、I2Cを有効にする
<br>
「3 Interface Options」 -> 「I5 I2C」 -> 「Yes」

- ライブラリのインストール

```
sudo apt-get install python3-smbus
```

- 接続したLCDモジュールのI2Cアドレスの確認

`sudo i2cdetect -y 1`コマンドを実行し、表示されたI2Cアドレスを確認する
<br>
※「27」のはず
<br>
※27でない場合はサンプルコード内のI2Cアドレスの変数の値を表示されたアドレスに変更する
