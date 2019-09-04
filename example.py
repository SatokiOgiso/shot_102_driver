from shot_102 import shot_102

def main():
    stage = shot_102("COM4", # コントローラのつながっているCOMポートしてい
                     pulse_per_unit=(1000, 1000)) # ステージの種類で異なる． 1000パルス/mmでとりあえず指定．

    # 機械原点復帰
    stage.go_mechanical_origin(1, "+")
    stage.go_mechanical_origin(2, "+")

    # 現在位置からの相対移動量をパルス数で指定して移動
    stage.set_cmd_relative_move_pulse(1, -1000)
    stage.start_move() #移動量を指定した後，動作開始命令

    # 現在位置からの相対移動量を単位(mmやrad)で指定して移動
    stage.set_cmd_relative_move_unit(2, -1)
    stage.start_move()

    # 移動先の絶対位置をパルス数で指定して移動
    stage.set_cmd_absolute_move_pulse(1, -2000)
    stage.start_move()

    # 移動先の絶対位置を単位(mmやrad)で指定して移動
    stage.set_cmd_absolute_move_unit(2, -2)
    stage.start_move()

    # 現在位置を原点に設定
    stage.set_current_position_as_origin(1)

    #通信終了
    stage.close_com()

if __name__ == "__main__":
    main()