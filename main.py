import pygame
import requests
import tkinter as tk

SCREENW = 880
SCREENH = 880
SERVERIP = 'http://127.0.0.1:12345'
MAXLAG = 5000  # in ms, more -> more stable

globaloffset = [0, 0]
crossmove = True

poss = []  # [x, y, iscross]


def drawgrid(display):
    global globaloffset
    for i in range(41):
        pygame.draw.line(display, (0, 0, 0), (i*40+globaloffset[0] % 40, -80+globaloffset[1] % 40),
                         (i*40+globaloffset[0] % 40, 880+globaloffset[1] % 40))
    for i in range(41):
        pygame.draw.line(display, (0, 0, 0), (-80+globaloffset[0] % 40, i*40+globaloffset[1] % 40),
                         (880+globaloffset[0] % 40, i*40+globaloffset[1] % 40))


def find_five_pieces(pieces):
    rows = {}
    cols = {}
    diags = {}
    for x, y, color in pieces:
        rows.setdefault(x, []).append((x, y, color))
        cols.setdefault(y, []).append((x, y, color))
        diags.setdefault(x + y, []).append((x, y, color))
        diags.setdefault(x - y, []).append((x, y, color))
    for d in rows, cols, diags:
        for k in d:
            if len(d[k]) >= 5:
                for i in range(len(d[k]) - 4):
                    if all(c == d[k][i][2] for _, _, c in d[k][i:i+5]):
                        return d[k][i:i+5]
    return None


def game(online=False, roomcode=None, color='r'):  # r, b; red moves first
    pygame.init()
    global crossmove, poss

    display = pygame.display.set_mode((SCREENW, SCREENH))  # w, h
    clock = pygame.time.Clock()
    FPS = 50
    cnt = 1
    while True:
        display.fill((255, 255, 255))
        drawgrid(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not ([(pos[0]-globaloffset[0])//40, (pos[1]-globaloffset[1])//40, crossmove] in poss
                        or [(pos[0]-globaloffset[0])//40, (pos[1]-globaloffset[1])//40, not crossmove] in poss):
                    poss.append([(pos[0]-globaloffset[0])//40, (pos[1]-globaloffset[1])//40, crossmove])
                    crossmove = not crossmove
                    print(find_five_pieces(poss))

        keyspressed = pygame.key.get_pressed()
        if keyspressed[pygame.K_UP]:
            globaloffset[1] += 5
        if keyspressed[pygame.K_DOWN]:
            globaloffset[1] += -5
        if keyspressed[pygame.K_LEFT]:
            globaloffset[0] += 5
        if keyspressed[pygame.K_RIGHT]:
            globaloffset[0] += -5

        # renderer
        if cnt == MAXLAG // 200 + 1 and online:
            cnt = 1
            poss = requests.post(SERVERIP+'/receive', params={"roomid": roomcode}, timeout=1)

        for s in poss:
            pygame.draw.circle(display, (255*s[2], 0, 0), [s[0]*40+20+globaloffset[0], s[1]*40+20+globaloffset[1]], 10)
        pygame.display.update()

        cnt += 1
        clock.tick(FPS)


def menu():
    w = tk.Tk()
    w.geometry('400x400')
    bg = tk.PhotoImage(file="exb.png")
    tk.Label(w, image=bg).place(x=0, y=0)
    tk.Label(w, text='ETTT', font=('Impact', 50), fg='black', bg='white', relief='solid').place(
        x=200, y=50, anchor='center')

    obb = tk.Button(w, text='Over the board', font=('Helvetica', 30), command=lambda: w.destroy(), width=16)
    obb.place(x=200, y=150, anchor='center')
    crc = tk.Button(w, text='Create room', font=('Helvetica', 30), width=16, command=lambda: createroom())
    crc.place(x=200, y=250, anchor='center')
    erc = tk.Button(w, text='Enter room code', font=('Helvetica', 30), width=16, command=lambda: joinroom())
    erc.place(x=200, y=350, anchor='center')

    def createroom():
        try:
            code = requests.get(SERVERIP+'/creategame')
            print(code.text)
            w.destroy()
            game(online=True, roomcode=code.text, color='r')
        except Exception:
            pass

    def joinroom():
        obb.place_forget()
        crc.place_forget()
        erc.place_forget()

        ercl = tk.Label(w, text='Enter room code:', font=('Helvetica', 30), width=16, relief='solid')
        ercl.place(x=200, y=150, anchor='center')

        rcentry = tk.Entry(w, width=30)
        rcentry.place(x=200, y=222, anchor='center')

        okb = tk.Button(w, text='ok', font=('Helvetica', 20))
        okb.place(x=200, y=275, anchor='center')

        backb = tk.Button(w, text='<back', font=('Helvetica', 20), command=lambda: backfromjoinroom())
        backb.place(x=60, y=30, anchor='center')

        def backfromjoinroom():
            ercl.place_forget()
            rcentry.place_forget()
            okb.place_forget()
            backb.place_forget()
            obb.place(x=200, y=150, anchor='center')
            crc.place(x=200, y=250, anchor='center')
            erc.place(x=200, y=350, anchor='center')

    w.mainloop()


if __name__ == "__main__":
    menu()
    game()
    pygame.quit()
