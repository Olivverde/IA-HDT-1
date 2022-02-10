import struct
import mmap
import numpy

class writebmp(object):

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

class readbmp(object):
    def __init__(self, path):
        self.path = path
        self.read()
    
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
        print(len(self.pixels))
        
        for i in range(len(self.pixels)):
          self.aux.append(self.pixels[i])
          if (len(self.aux) == 3):
            color = self.color(self.aux[0], self.aux[1], self.aux[2])
            self.processed.append(color)
            self.aux = []
            if (len(self.processed) == self.width):
              self.buffer.append(self.processed)
              self.processed = []
        
        print(len(self.buffer))
        return self.buffer
          

reader = readbmp("Test2.bmp")
writer = writebmp()
width, height = reader.width, reader.height
print(width, height)
writer.writebmp("bmp-out.bmp", width, height, reader.buffer)
