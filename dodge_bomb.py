import os
import random
import sys
import time

import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, 5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (5, 0),
    }
# キーに応じた移動量の辞書
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectの位置が画面の中か外かを判定する
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or  HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    引数：screen
    画面に「Game Over」の文字を表示し、
    文字の両隣に泣いているこうかとんを表示する。
    """
    screen.fill((0, 0, 0)) # ブラックアウト
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255)) # Game Overのフォント
    txt_rect = txt.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(txt, txt_rect)
    kk_cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.0) # 泣いているこうかとんの画像を読み込む
    kk_cry_rct1 = kk_cry_img.get_rect()
    kk_cry_rct1.center = WIDTH/3, HEIGHT/2
    kk_cry_rct2 = kk_cry_img.get_rect()
    kk_cry_rct2.center = WIDTH*2/3, HEIGHT/2
    screen.blit(kk_cry_img, kk_cry_rct1)
    screen.blit(kk_cry_img, kk_cry_rct2)
    pg.display.update() # 画面の更新
    time.sleep(5) # 5秒停止

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect() # 爆弾Rectの抽出
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) # 爆弾の出現位置の乱数
    vx, vy = +5, +5 # 爆弾の速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct): # こうかとんと爆弾の衝突判定
            gameover(screen) # ゲームオーバーの処理
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): # こうかとんの画面内外の判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
            kk_rct.move_ip(0, -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko: # 爆弾のx軸の画面内外の判定
            vx *= -1
        if not tate: # 爆弾のy軸の画面内外の判定
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
