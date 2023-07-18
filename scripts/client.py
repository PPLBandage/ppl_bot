
from minepi import Player
from PIL import Image, ImageEnhance, ImageFont, ImageDraw, ImageOps
from os import listdir
from os.path import isfile, join
import json


def transparent_negative(img):
    rgb_im = img.convert('RGBA')
    for y in range(64):
        for x in range(64):
            r, g, b, t = rgb_im.getpixel((x, y))
            try: 
                if t != 0: rgb_im.putpixel((x, y), (255 - r, 255 - g, 255 - b, t))
            except: pass
    return rgb_im


def bw_mode(img):
    rgb_im = img.convert('RGBA')
    for y in range(64):
        for x in range(64):
            r, g, b, t = rgb_im.getpixel((x, y))
            try: 
                if t != 0: 
                    a = round((r + b + g) / 3)
                    rgb_im.putpixel((x, y), (a, a, a, t))
            except: pass
    return rgb_im
def average_colour(im):
    rgb_im = im.convert('RGBA')
    w, h = rgb_im.size
    r_a = 0
    g_a = 0
    b_a = 0
    num = 0
    for y in range(h):
        for x in range(w):
            r, g, b, t = rgb_im.getpixel((x, y))
            if t != 0:
                r_a += r
                g_a += g
                b_a += b
                num += 1

    return (255 - round(r_a / num), 255 - round(g_a / num), 255 - round(b_a / num))

def fill(img, colour):
    rgb_im = img.convert('RGBA')
    w, h = img.size
    r_c, g_c, b_c = colour
    for y in range(h):
        for x in range(w):
            r, g, b, t = rgb_im.getpixel((x, y))
            try: 
                if t != 0 and r == g == b: 
                    rgb_im.putpixel((x, y), (round((r / 255) * r_c), round((g / 255) * g_c), round((b / 255) * b_c), t))
            except: pass
    return rgb_im


def clear(img, pos):
    rgb_im = img.convert('RGBA')
    w, h = 16, 4
    pos_x, pos_y = pos
    for y in range(h):
        for x in range(w):
            try: rgb_im.putpixel((x + pos_x, y + pos_y), (0, 0, 0, 0))
            except: pass
    return rgb_im

def crop(img, abs, slim):

    image = Image.open(img).convert("RGBA")
    if slim and abs == 0: image_o = image.crop((0, 0, 15, 5))
    else: image_o = image.copy()

    if abs > 1:
        img_left = image_o.crop((0, 0, 8, 4))
        img_right = image_o.crop((8, 0, 16, 4))
        image_o = Image.new('RGBA', (16, 4), (0, 0, 0, 0))
        image_o.paste(img_right, (0, 0), img_right)
        image_o.paste(img_left, (8 if not (slim and (abs == 0 or img == "res/pepes/pepe1.png")) else 6, 0), img_left)

    return image_o
    
def to64(skin):
    new_img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    img = skin.copy()
    leg = img.crop((0, 16, 16, 32))
    arm = img.crop((40, 16, 64, 32))

    new_img.paste(leg, (16, 48), leg)
    new_img.paste(arm, (32, 48), arm)
    new_img.paste(img, (0, 0), img)

    leg_1 = img.crop((0, 20, 4, 32))
    leg_1 = ImageOps.mirror(leg_1)
    new_img.paste(leg_1, (24, 52), leg_1)

    leg_2 = img.crop((8, 20, 12, 32))
    leg_2 = ImageOps.mirror(leg_2)
    new_img.paste(leg_2, (16, 52), leg_2)

    leg_2 = img.crop((4, 20, 8, 32))
    leg_2_m = ImageOps.mirror(leg_2)
    new_img.paste(leg_2_m, (20, 52), leg_2_m)

    leg_2 = img.crop((12, 20, 16, 32))
    leg_2_m = ImageOps.mirror(leg_2)
    new_img.paste(leg_2_m, (28, 52), leg_2_m)

    leg_2 = img.crop((4, 16, 8, 20))
    leg_2_m = ImageOps.mirror(leg_2)
    new_img.paste(leg_2_m, (20, 48), leg_2_m)

    leg_2 = img.crop((8, 16, 12, 20))
    leg_2_m = ImageOps.mirror(leg_2)
    new_img.paste(leg_2_m, (24, 48), leg_2_m)

    arm_1 = img.crop((40, 20, 44, 32))
    arm_1 = ImageOps.mirror(arm_1)
    new_img.paste(arm_1, (40, 52), arm_1)

    arm_1 = img.crop((48, 20, 52, 32))
    arm_1 = ImageOps.mirror(arm_1)
    new_img.paste(arm_1, (32, 52), arm_1)

    arm_1 = img.crop((44, 20, 48, 32))
    arm_1_m = ImageOps.mirror(arm_1)
    new_img.paste(arm_1_m, (36, 52), arm_1_m)

    arm_1 = img.crop((52, 20, 56, 32))
    arm_1_m = ImageOps.mirror(arm_1)
    new_img.paste(arm_1_m, (44, 52), arm_1_m)

    arm_1 = img.crop((44, 16, 48, 20))
    arm_1_m = ImageOps.mirror(arm_1)
    new_img.paste(arm_1_m, (36, 48), arm_1_m)

    arm_1 = img.crop((48, 16, 52, 20))
    arm_1_m = ImageOps.mirror(arm_1)
    new_img.paste(arm_1_m, (40, 48), arm_1_m)

    return new_img

class Client:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.slim = None
        self.slim_cust = 0
        self.mc_class = None
        self.skin_raw = None #img
        self.prewiew_id = 0
        self.info_id = 0
        self.delete_mess = False
        self.first_skin1 = None #img
        self.average_col = None
        self.pose = 0
        self.settings_mess = 0
        self.change_e = 0
        self.bandage = None
        self.error_msg = None
        self.wait_to_support = False
        self.wait_to_file = 0
        self.import_msg = -1

        self.pos = 4
        self.colour = (-1, -1, -1)
        self.pepeImage = -1
        self.first_layer = 1
        self.overlay = True
        self.bw = False
        self.negative = False
        self.absolute_pos = 0
        self.delete_pix = True
        self.pepe_type = 0
    
        #leftArm leftLeg rightArm rightLeg
        self.x_f = [32, 16, 40, 0]
        self.y_f = [52, 52, 20, 20]
        self.x_o = [48, 0, 40, 0]
        self.y_o = [52, 52, 36, 36]

        self.pepes = [f for f in listdir("res/pepes") if isfile(join("res/pepes", f))]
        

        self.poses = [
            [0,  20, 10, 0], #vrll
            [0, -20,-10, 0], #vrrl
            [0, -20,-10, 0], #vrla
            [0,  20, 10, 0], #vrra
            [0,   0,  0, 90], #hrla
            [0,   0,  0, -90], #hrra
            [0,   0,  0, 20], #hrll
            [0,   0,  0, -20] #hrrl
        ]
        
        
    def reset(self):
        self.pos = 4
        self.colour = (-1, -1, -1)
        self.first_layer = 1
        self.overlay = True
        self.bw = False
        self.negative = False
        self.absolute_pos = 0
        self.delete_pix = True
        self.pepe_type = 0


    async def init_mc_f(self, usr_img):
        self.mc_class = Player(name="abc", raw_skin=usr_img)  # create a Player object by UUID
        await self.mc_class.initialize()
        self.skin_raw = usr_img
        self.first_skin1 = usr_img.copy()
        w, h = self.skin_raw.size
        if w != 64 or h != 64:
            self.skin_raw = self.first_skin1 = to64(self.skin_raw.copy())
        

    async def init_mc_n(self, name):
        done = 1
        self.mc_class = Player(name=name)  # create a Player object by UUID
        await self.mc_class.initialize()
        if self.mc_class._raw_skin == None: done = 0
        else:
            self.skin_raw = self.mc_class._raw_skin
            self.first_skin1 = self.mc_class._raw_skin.copy()

            w, h = self.skin_raw.size
            if w != 64 or h != 64:
                self.skin_raw = self.first_skin1 = to64(self.skin_raw.copy())

            for y_ch in range(3):
                for x_ch in range(3):
                    r, g, b, t = self.skin_raw.getpixel((x_ch, y_ch))
                    if t != 0:
                        done = 3
                        break
            
            if not bool(self.skin_raw.getpixel((46, 52))[3]) and not bool(self.skin_raw.getpixel((45, 52))[3]): done = 4

                    
            
        return done
        
    def exportJSON(self, chat):
        params = {
            "position": self.pos, 
            "firstLayer": self.first_layer, 
            "overlay": self.overlay, 
            "bw": self.bw, 
            "negative": self.negative, 
            "absolutePos": self.absolute_pos, 
            "layerDelete": self.delete_pix,
            "pepeType": self.pepe_type,
            "pepeImage": self.pepeImage
        }

        json_object = json.dumps(params, indent=9)
 
        # Writing to sample.json
        with open(f"params{chat}.json", "w") as outfile:
            outfile.write(json_object)

    def importJSON(self, chat):
        with open(f'paramImported{chat}.json', 'r') as openfile:
            json_object = json.load(openfile)

        
        self.pos = int(json_object["position"])
        self.first_layer = int(json_object["firstLayer"])
        self.overlay = json_object["overlay"]
        self.bw = json_object["bw"]
        self.negative = json_object["negative"]
        self.absolute_pos = int(json_object["absolutePos"])
        self.delete_pix = json_object["layerDelete"]
        self.pepe_type = int(json_object["pepeType"])
        self.pepeImage = int(json_object["pepeImage"])
        

    async def prerender(self):
        if self.bw: self.skin_raw = bw_mode(self.skin_raw).copy()
        if self.negative: self.skin_raw = transparent_negative(self.skin_raw)
        
        mc_class = Player(name="abc", raw_skin=self.skin_raw)
        self.slim = self.mc_class.skin.is_slim
        await mc_class.initialize()
        
        await mc_class.skin.render_skin(hr=-45, vr=-20, ratio = 20, vrc = 15)
        img = mc_class.skin.skin
        self.average_col = average_colour(img.copy())
        
    async def rerender(self):

        self.skin_raw = self.first_skin1.copy()
        if self.colour != (-1, -1, -1):
            if self.delete_pix: self.skin_raw = clear(self.skin_raw.copy(), (self.x_o[self.absolute_pos], self.y_o[self.absolute_pos] + self.pos))



            if self.pepeImage == -1: img = crop("res/pepes/" + str(self.pepes[self.pepe_type]), self.absolute_pos, self.slim)
            else:img = crop(f"res/pepes/colored/{self.pepeImage}", self.absolute_pos, self.slim)
            
            if self.pepeImage == -1: img = fill(img.copy(), self.colour)
            
            sl = self.slim and (self.absolute_pos == 0)
            if self.first_layer == 2: self.skin_raw.paste(img.crop((1, 0, 16, 4)) if sl else img, (self.x_f[self.absolute_pos], self.y_f[self.absolute_pos] + self.pos), img.crop((1, 0, 16, 4)) if sl else img)
            if self.overlay: self.skin_raw.paste(img.crop((1, 0, 16, 4)) if sl else img, (self.x_o[self.absolute_pos], self.y_o[self.absolute_pos] + self.pos), img.crop((1, 0, 16, 4)) if sl else img)

            
            bond = Image.new('RGBA', (16, 4), (0, 0, 0, 0))
            if self.first_layer == 1: 
                if self.pepeImage == -1: img_lining = Image.open("res/lining/custom.png")
                else: img_lining = crop(f"res/lining/colored/{self.pepeImage}", self.absolute_pos, self.slim)
                img_lining = fill(img_lining.copy(), self.colour)
                self.skin_raw.paste(img_lining.crop((2, 0, 16, 4)) if sl else img_lining, (self.x_f[self.absolute_pos], self.y_f[self.absolute_pos] + self.pos), img_lining.crop((2, 0, 16, 4)) if sl else img_lining)
                bond.paste(img_lining, (0, 0), img_lining)
            bond.paste(img, (0, 0), img)
            self.bandage = bond

            img.close()
        if self.bw: self.skin_raw = bw_mode(self.skin_raw).copy()

        if self.negative: 
            self.skin_raw = transparent_negative(self.skin_raw)
            r, g, b = self.average_col
            average_col = 255 - r, 255 - g, 255 - b
        
        else: average_col = self.average_col

        self.mc_class = Player(name="abc", raw_skin=self.skin_raw)
        await self.mc_class.initialize()


        
        await self.mc_class.skin.render_skin(hr=45 if self.absolute_pos > 1 else -45, 
                                             vr=-20, 
                                             ratio = 20, 
                                             vrc = 15, 
                                             vrll=self.poses[0][self.pose], 
                                             vrrl=self.poses[1][self.pose],
                                             vrla=self.poses[2][self.pose],
                                             vrra=self.poses[3][self.pose],
                                             hrla=self.poses[4][self.pose],
                                             hrra=self.poses[5][self.pose],
                                             hrll=self.poses[6][self.pose],
                                             hrrl=self.poses[7][self.pose],
                                             man_slim=self.slim_cust
                                             )
        img = self.mc_class.skin.skin
        
        new_img = None
        r, g, b = self.average_col
        not_aver = 255 - r, 255 - g, 255 - b
        width, height = img.size
        fnt = ImageFont.truetype("res/font.ttf", 15)
        
        new_img = Image.new('RGB', (height + 20, height + 20), average_col)
        new_img.paste(img, (round((height + 20) / 2) - round
                            (width / 2), 10), img)
        
        d = ImageDraw.Draw(new_img)
        d.text((5, height), "by AndcoolSystems", font=fnt, fill=not_aver)
        return new_img
    
    
    
def find_client(list, chat_id):
    if list == []: id = -1
    else:
        finded = False
        for add in range(len(list)):
            if list[add].chat_id == chat_id:
                finded = True
                id = add
                break
        if not finded: 
            id = -1
    return id
