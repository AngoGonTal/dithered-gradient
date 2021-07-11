# Lade externe Bibliotheken
from PIL import Image


# Lade eigene Bibliotheken
from ycbcr2rgb import rgb2ycbcr
from fsd import fsd
import eingabe


# Abfrage der Quantisierung, des Farbkanals und der wahrnehmbaren Farbtiefe
quantity = eingabe.palette() 
channel = eingabe.farbkanal()
vDepth = eingabe.vFarbraum()


# Bestimme Konstanten für weitere Berechnung
BLOCK = 1                                  # Kantenkänge der kleinstmöglichen Füllfläche
WIDTH, HEIGHT = 0, 1
DEPTH = 8 - quantity + vDepth              # rechnerischen Farbraum
DIMENSIONS = ( 50*BLOCK, 2**DEPTH*BLOCK )  # Kantenlänge des Bildes
if channel <= 2: MODE = "RGB"              # Farbmodell des Bildes
if channel  > 2: MODE = "YCbCr"


# Errechne den Farbwert pro Block für einen vertikalen Farbverlauf
# von 0 bis Vollfarbe. Die zwei anderen Farbkanäle sind immer 0 und 
# werden daher später konstant ergänzt
# Bleibe hierbei noch im virtuellen Farbraum
PrePic = [0] * DIMENSIONS[HEIGHT]*DIMENSIONS[WIDTH]
for y in range(DIMENSIONS[HEIGHT]):
    for x in range( DIMENSIONS[WIDTH] ):
        PrePic[y*DIMENSIONS[WIDTH]+x] = (y // BLOCK) 


# Reduziere die verwendeten Farben auf jene, die als Farbpalette
# erlaubt sind.
# Sollte der Farbraum virtuell erweitert worden sein, heißt das,
# dass via Dithering Zwischenstufen dargestellt werden sollen.
# Diese Zwischenstufen werden jedoch auf Basis der reduzierten
# Farbpalette errechnet
PrePic = fsd( PrePic, DIMENSIONS[WIDTH], DIMENSIONS[HEIGHT], 8-quantity, DEPTH )



# img = Image.new( MODE, size = DIMENSIONS )
# data = img.load()
# for y in range( DIMENSIONS[HEIGHT] ):
#     for x in range( DIMENSIONS[WIDTH] ):
#         ch = [ 0, 0, 0 ]
#         ch[channel%3] = y//BLOCK
#         data[x,y] = (ch[0],ch[1],ch[2])


# Wandle das RGB Farbmodell in YCbCr um
# if channel >= 3:
#     for y in range( DIMENSIONS[HEIGHT] ):
#         if y%BLOCK == 0:
#             print("Konvertiere " + str(( data[0,y][0], data[0,y][1], data[0,y][2] )) + " nach: " )
#         for x in range( DIMENSIONS[WIDTH] ):    
#             data[x,y] = rgb2ycbcr( ( data[x,y][0], data[x,y][1], data[x,y][2] ) )
#         if y%BLOCK == 0:
#             print( str( data[0,y] ) )
            

# Führe Quantisierung durch
# if dither == "n":
#     if quantity > 0: 
#         for y in range( DIMENSIONS[HEIGHT] ):
#             for x in range( DIMENSIONS[WIDTH] ):
#                 ch = [0, 0, 0]
#                 ch[channel%3] = data[x,y][channel%3] & ~(2**quantity-1)
#                 data[x,y] = ( ch[0], ch[1], ch[2] )
# Führe Dithering durch
# if dither == "y":
#     data = fsd( data, DIMENSIONS[WIDTH], DIMENSIONS[HEIGHT], 8-quantity )


# Überführe das Ergebnis in ein Bild
img = Image.new( MODE, size = DIMENSIONS )
data = img.load()
for y in range( DIMENSIONS[HEIGHT] ):
    for x in range( DIMENSIONS[WIDTH] ):
        ch = [ 0, 0, 0 ]
        ch[channel%3] = PrePic[y*DIMENSIONS[WIDTH]+x] * 255 // ((2**DEPTH)-1)    # Normalisiere zu TrueColor Farbraum

        # DEBUG start
        #if x == 0:
        #    print("Alter Wert lautet: " + str( PrePic[y*DIMENSIONS[WIDTH]+x] ) )
        #    print("Neuer Wert lautet: " + str( ch[channel%3] ) )
        #    print("Quotient lautet: " + str( ((2**DEPTH)-1) ) )
        # DEBUG Ende
        

        # Füge die Farbwerte als Tupel im Bild ein
        if channel < 3: data[x,y] = ( ch[0], ch[1], ch[2] )                # Bleibe im RGB Farbraum
        else: data[x,y] = rgb2ycbcr( ch[0], ch[1], ch[2] )                 # Wandle in den YCbCr Farbraum um           


# Gebe das Ergebnis aus
if channel < 3:
    img.save( "R:\\Temp\\" + str(channel) + "-color-gradient-" + str(quantity) + "-" + str(vDepth) + ".png")
if channel >= 3:
    img.save( "R:\\Temp\\" + str(channel) + "-color-gradient-" + str(quantity) + "-" + str(vDepth) + ".jpeg", quality=100, subsampling=0 )

img.show()