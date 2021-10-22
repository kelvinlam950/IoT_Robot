import framebuf
from micropython import const

OLED_Address = 0x3C
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_PAGE_SADDR = const(0xB0)
SET_PAGE_LOW_COL_ADDR = const(0x00)
SET_PAGE_HIGH_COL_ADDR = const(0x10)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)

class SSD1307(framebuf.FrameBuffer):
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = int(self.height / 8)
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP,  # Set Display Off
            SET_MEM_ADDR, # Set Memory Addressing Mode
            0x10,
            SET_DISP_CLK_DIV, # Display divide ratio/osc. freq. mode 
            0xA1, #Fosc:1010b Divider:2
            SET_MUX_RATIO, #Set Mux ratio
            self.height - 1, #31 MUX
            SET_DISP_OFFSET, #Set Display Offset
            0x23, #Vertical shift 35
            SET_DISP_START_LINE, #Set Display Start Line
            SET_SEG_REMAP|0x01, #Segment Remap 127 to SEG0
            SET_COM_OUT_DIR, #Set COM Output Scan Direction
            SET_COM_PIN_CFG, #Set SEG Pins Hardware Configuration
            0x12, #Alternative SEG pin config and disable SEG Left/Right remap
            SET_CONTRAST, #Contrast control 
            0x80, #Half contrast
            SET_PRECHARGE, #Set pre-charge period 
            0x51, #Phase 1: 1 period Phase 2: 5 period
            SET_VCOM_DESEL, #Set VCOMH 
            0x20, #0.77xVcc
            SET_ENTIRE_ON, #Set Entire Display ON and Output follows RAM content
            SET_NORM_INV, #Set Normal Display 
        ):  # on           
            self.write_cmd(cmd)

        self.clear()
        self.poweron()  # Set Display ON
 
    def poweroff(self):
        self.write_cmd(SET_DISP)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def rotate(self, rotate):
        self.write_cmd(SET_COM_OUT_DIR | ((rotate & 1) << 3))
        self.write_cmd(SET_SEG_REMAP | (1 - rotate))
    
    def clear(self):
        self.fill(0)
        self.show()
        
    def show(self):
        for i in range(self.pages):
            self.write_cmd(SET_PAGE_SADDR| i) #Set Page start address
            self.write_cmd(SET_PAGE_LOW_COL_ADDR) #Set Lower Column Start address
            self.write_cmd(SET_PAGE_HIGH_COL_ADDR) #Set Higher Column Start address
            self.write_data(self.buffer[(i)*self.width:(self.width * (i+1)-1)])
    
    def drawRect(self, x, y, w, h, mode):
        if(mode == 0):
            self.rect(x,y,w,h,1)
        else:
            self.fill_rect(x,y,w,h,1)
            
    def drawLine(self, x, y, l, mode):
        if(mode == 0):
            self.hline(x,y,l,1)
        else:
            self.vline(x,y,l,1)
            
class SSD1307_I2C(SSD1307):
    def __init__(self, width, height, i2c, addr=OLED_Address, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2) #used for command transmission
        super().__init__(width, height, external_vcc)
    
    def write_cmd(self, cmd):
        self.temp[0] = 0x00  #Command
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.temp[0]=self.addr<<1
        self.temp[1]=0x40
        self.i2c.start()
        self.i2c.write(self.temp)
        self.i2c.write(buf)
        self.i2c.stop()
