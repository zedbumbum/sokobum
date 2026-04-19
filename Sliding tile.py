import tkinter as tk

def load_map(map1):
    with open(map1, 'r') as f:
        lines = f.readlines()
    lines = [ line.strip() for line in lines]
    return lines


MAP = load_map("sliding_tile/maps/map1.txt")
if len(MAP) == 0:
    raise ValueError("Map is empty")

width = len(MAP[0])
for line in MAP:
    if len(line) != width:
        raise ValueError("All lines must have the same width")
if len(line) != width:
    raise ValueError("Map is not rectangular")
allowed = set("#.P")
for r in range(len(MAP)):
    for c in range(len(MAP[0])):
        ch = MAP[r][c]
        if ch not in allowed:
            raise ValueError(f"Bad char{ch} at ({r}, {c})")
        
p_count = 0
for r in range(len(MAP)):
    for c in range(len(MAP[0])):
        if MAP[r][c] == "P":
            p_count += 1
if p_count != 1:
    raise ValueError("There must be exactly one P in the map")

TILE = 120
ROWS = len(MAP)
COLS = len(MAP[0])


def draw_image_tile(r, c, key):
    x = c * TILE
    y = r * TILE
    canvas.create_image(x, y,image=images[key]
                        , anchor="nw")
tile_lookup = {
    '#': 'wall',
    '.': 'floor',
    'P': 'player'
}


W = COLS * TILE
H = ROWS * TILE

print (W, H)

root = tk.Tk()
root.title("Me tryna get out of prison")

canvas = tk.Canvas(root, width=W, height=H)
canvas.pack()

player_r = 0
player_c = 0

images = {
    'floor': tk.PhotoImage(file='sliding_tile/tiles/extra_dirt_detail.png'),
    'wall': tk.PhotoImage(file='sliding_tile/tiles/extra_stone.png'),
    'player': tk.PhotoImage(file='sliding_tile/tiles/extra_character.png')
}


for r in range(ROWS):
    for c in range(COLS):
        if MAP[r][c] == 'P':
            player_r = r
            player_c = c


def draw_tile(r, c, ch):
    
    x1 = c * TILE
    y1 = r * TILE
    x2 = x1 + TILE
    y2 = y1 + TILE

    if ch == "#":
        color = "grey"
    else:
        color = "white"
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

def draw_player(r, c):
    x1 = c * TILE
    y1 = r * TILE
    x2 = x1 + TILE
    y2 = y1 + TILE
    canvas.create_oval(x1+8, y1+8, x2-8, y2-8,
                       fill="orange", outline="")

def draw_world():
    canvas.delete("all")
    for r in range(ROWS):
        for c in range (COLS):
            ch = MAP[r][c]
            base = tile_lookup[ch]
            draw_image_tile(r, c, base)
            
    draw_image_tile(player_r, player_c, "player")    

draw_world()

def try_move(dr, dc):
    global player_r, player_c
    nr = player_r + dr
    nc = player_c + dc

    if not ( 0 <= nr < ROWS and 0 <= nc < COLS):
        return

    if MAP[nr][nc] == "#":
        return
    player_r = nr
    player_c = nc
    draw_world()


def on_key(event):
    if event.keysym == "Up":
        try_move(-1, 0)
    elif event.keysym == "Down":
        try_move(1, 0)
    elif event.keysym == "Left":
        try_move(0, -1)
    elif event.keysym == "Right":
        try_move(0, 1)


root.bind("<Key>", on_key)

draw_world()

root.mainloop()