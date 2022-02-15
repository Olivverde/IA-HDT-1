import struct
import mmap
import numpy

class Writebmp(object):

  def char(self, c):
    """
    Input: requires a size 1 string
    Output: 1 byte of the ascii encoded char
    """
    return struct.pack('=c', c.encode('ascii'))

  def word(self, w):
    """
    Input: requires a number such that (-0x7fff - 1) <= number <= 0x7fff
          ie. (-32768, 32767)
    Output: 2 bytes
    Example:
    >>> struct.pack('=h', 1)
    b'\x01\x00'
    """
    return struct.pack('=h', w)

  def dword(self, d):
    """
    Input: requires a number such that -2147483648 <= number <= 2147483647
    Output: 4 bytes
    Example:
    >>> struct.pack('=l', 1)
    b'\x01\x00\x00\x00'
    """
    return struct.pack('=l', d)

  def toBytes(self):
      self.r = int(max(min(self.r, 255), 0))
      self.g = int(max(min(self.g, 255), 0))
      self.b = int(max(min(self.b, 255), 0))
      return bytes([self.b, self.g, self.r])

  def writebmp(self, filename, width, height, pixels):
    f = open(filename, 'bw')

    f.write(self.char('B'))
    f.write(self.char('M'))
    f.write(self.dword(14 + 40 + width * height * 3))
    f.write(self.dword(0))
    f.write(self.dword(14 + 40))

    f.write(self.dword(40))
    f.write(self.dword(width))
    f.write(self.dword(height))
    f.write(self.word(1))
    f.write(self.word(24))
    f.write(self.dword(0))
    f.write(self.dword(width * height * 3))
    f.write(self.dword(0))
    f.write(self.dword(0))
    f.write(self.dword(0))
    f.write(self.dword(0))

    for x in range(height):
      for y in range(width):
        f.write(pixels[x][y])
    f.close()



class Readbmp(object):
    def __init__(self, path):
        self.path = path
        self.start = self.color(254,0,0)
        self.availablePath = self.color(255,255,255)
        self.wall = self.color(0,0,0)
        self.goal = self.color(5,252,6)
        self.fraction = 20

        self.read()
        self.discretization()
        
    
    def color(self, r, g, b): # generador de colores
      return bytes([r, g, b])

    def read(self):
        self.aux = []
        self.processed = []
        self.buffer = [] 

        img = open(self.path, "rb")
        m = mmap.mmap(img.fileno(), 0, access=mmap.ACCESS_READ)
        ba = bytearray(m)
        header_size = struct.unpack("=l", ba[10:14])[0]
        self.width = struct.unpack("=l", ba[18:22])[0]
        self.height = struct.unpack("=l", ba[18:22])[0]
        all_bytes = ba[header_size::]
        self.pixels = numpy.frombuffer(all_bytes, dtype='uint8')
        img.close()
        
        for i in range(len(self.pixels)):
          self.aux.append(self.pixels[i])
          if (len(self.aux) == 3):
            color = self.color(self.aux[0], self.aux[1], self.aux[2])
            self.processed.append(color)
            self.aux = []
            if (len(self.processed) == self.width):
              self.buffer.append(self.processed)
              self.processed = []
        
        return self.buffer
    
    def stadistics(self, pathFlag, frontier, indexes):
      color = self.color(1, 1, 1)
      totalPixels = self.pixelRange**2
      proportion = pathFlag/totalPixels
      i, j, xRange, yRange = indexes
      print(proportion)
      if proportion >= 0.5 and frontier == 0:
        color = self.availablePath
      elif proportion < 0.5 and frontier == 0:
        color = self.wall
      elif frontier > 0:
        color = self.start
     
      for a in range(i, xRange):
        for b in range(j, yRange):
          self.buffer[a][b] = color
          #print(a,b,i,j)
      #input('[ENTER]')
      self.buffer[0][29]= self.start


    def discretization(self):
      bff = self.buffer
      flagPath, extraFlag = 0, 0
      self.i, self.j, self.x, self.y = 0, 0, 0, 0
      self.pixelRange = round(self.width/self.fraction)
      self.xFraction, self.yFraction = self.fraction, self.fraction
      self.xRange, self.yRange = self.pixelRange, self.pixelRange

      for x in range(self.x, self.xFraction):
        for y in range(self.y, self.yFraction):
          for i in range(self.i, self.xRange):
            for j in range(self.j, self.yRange):
              if bff[i][j] == self.availablePath:
                flagPath += 1
              elif bff[i][j] == self.goal or bff[i][j] == self.start:
                extraFlag += 1
              #print(x,y,i,j)
          #input('[ENTER]')
          self.stadistics(flagPath, extraFlag, [self.i, self.j, self.xRange, self.yRange])
          flagPath, extraFlag = 0,0

          self.j += self.pixelRange
          self.yRange += self.pixelRange
        
        self.j, self.yRange = 0, self.pixelRange
        self.i += self.pixelRange
        self.xRange += self.pixelRange

        
    
    """
    def getFrontierRadio(self):
      self.radio = 0
      indexCounter = []
      frontierColor = self.color(254,0,0)
      offsetColor = self.color(255,255,255)
      flag = 0

      for i in range(len(self.buffer)):
        for pixel in range(len(self.buffer[i])):
          if self.buffer[i][pixel] == frontierColor and flag < 1:
            flag += 1
            self.radio = -pixel
          elif self.buffer[i][pixel] == offsetColor and flag == 1:
            flag += 1
            self.radio += pixel
            indexCounter.append(self.radio)
        self.radio = 0
        flag = 0
      self.radio = max(indexCounter)

      return self.radio
    """

          
"""
TESTING
"""
reader = Readbmp("Test2.bmp")
writer = Writebmp()
width, height = reader.width, reader.height
print(width, height)
writer.writebmp("bmp-out.bmp", width, height, reader.buffer)
"""
print(reader.getFrontierRadio())

"""
