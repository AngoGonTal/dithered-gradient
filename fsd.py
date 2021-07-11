# Floyd–Steinberg dithering with serpentine scanning
# Quelle: https://en.wikipedia.org/wiki/Floyd–Steinberg_dithering
#
# Argument pixels erwartet ein zwei-dimensionales Array aus Tupel
# Die Tupel enthalten Elemente für genau drei Farbkanäle


# Alte Version erwartet Tupel, mit drei Werte von je 0-255 
# (und war buggy)
#def find_closest_palette_color( oldpixel, palette ):
#    ch = [0,0,0]
#    ch[0] = round( oldpixel[0] / 255 * 2**palette  )
#    ch[1] = round( oldpixel[1] / 255 * 2**palette )
#    ch[2] = round( oldpixel[2] / 255 * 2**palette )
#    return( ( int( ch[0]*255/2**palette ), int( ch[1]*255/2**palette ), int( ch[2]*255/2**palette ) ) )
#
#
# Erwartet einen einzelnen Farbwert als Quotient zwischen Wert
# und Farbraum 80 in TrueColor(8bit pro Kanal) = 85 = 85/255 = 1/3 = 0.333
# Es gilt: 0 ≤ ColorRation ≤ 1
# Die Palette beschreibt, wie viele Farbabstufungen 
# zwischen 0% und 100% möglich sind, wobei das Argument den 
# Exponenten zur Basis 2 darstellt. (3= 2**3 = 8)
def find_closest_palette_color( ColorRatio: float, palette: int ) -> float:
    raum = 2**palette - 1
    ret = round( ColorRatio * raum ) / raum

    # Stelle sicher, dass der Wert stets zwischen 0 und 1 liegt
    ret = InBetween( ret, 0.0, 1.0 )

    return( ret )
    # Notiz: Python rundet bis inkl. 0.5 RUNTER
    # da der Divisor (raum) aber immer ungerade sein muss, kann ColorRation nie 0.5 sein


def InBetween( value: float, minimum: float=0.0 , maximum: float=1.0  ) -> float:
    ret = value
    ret = max( ret, minimum )
    ret = min( ret, maximum )
    return( ret )


def fsd( PrePic, WIDTH, HEIGHT, palette, DEPTH ):
    with open("R:\\Temp\\debug.txt","w+") as f:
        #
        # DEBUG START
        # print( str(WIDTH), str(HEIGHT), str(palette), str(DEPTH), file=f )
        # DEBUG ENDE
        #

        px = PrePic
        for y in range( HEIGHT ):
            oldpixel = None
            newpixel = None
            for x in range( WIDTH ):
                oldpixel = px[y*WIDTH+x] / (2**DEPTH-1)
                newpixel = find_closest_palette_color( oldpixel, palette )
                px[y*WIDTH+x] = int( round( newpixel * (2**DEPTH-1) ) )

                # Wenn die virtuelle Farbtiefe größer ist als die 
                # tatsächliche Farbtiefe, also der Farbraum der 
                # Palette, dann nutze Dithering
                if DEPTH > palette:
                    quant_error = (oldpixel - newpixel) * (2**DEPTH-1) 

                    if x < WIDTH-1:
                        # DEBUG
                        # print("#1 Rechne: ", px[y*WIDTH+x+1], "+", quant_error * 7/16, "=", int( round( InBetween( (px[y*WIDTH+x+1] + quant_error * 7/16) / (2**DEPTH-1) ) * (2**DEPTH-1) ) ), file=f)
                        px[y*WIDTH+x+1] = InBetween( (px[y*WIDTH+x+1] + quant_error * 7/16) / (2**DEPTH-1) ) * (2**DEPTH-1)
                    
                    if x > 0 and y < HEIGHT -1:
                        # DEBUG
                        # print("#2 Rechne: ", px[(y+1)*WIDTH+x-1], "+", quant_error * 3/16, "=", int( round( InBetween( (px[(y+1)*WIDTH+x-1] + quant_error * 3/16) / (2**DEPTH-1) ) * (2**DEPTH-1) ) ), file=f)
                        px[(y+1)*WIDTH+x-1] = InBetween( (px[(y+1)*WIDTH+x-1] + quant_error * 3/16) / (2**DEPTH-1) ) * (2**DEPTH-1)
                    
                    if y < HEIGHT -1:
                        # DEBUG
                        # print("#3 Rechne: ", px[(y+1)*WIDTH+x], "+", quant_error * 5/16, "=", int( round( InBetween( (px[(y+1)*WIDTH+x] + quant_error * 5/16) / (2**DEPTH-1) ) * (2**DEPTH-1) ) ), file=f)
                        px[(y+1)*WIDTH+x] = InBetween( (px[(y+1)*WIDTH+x] + quant_error * 5/16) / (2**DEPTH-1) ) * (2**DEPTH-1)
                    
                    if x < WIDTH -1 and y < HEIGHT -1:
                        # DEBUG
                        # print("#4 Rechne: ", px[(y+1)*WIDTH+x+1], "+", quant_error * 1/16, "=", int( round( InBetween( (px[(y+1)*WIDTH+x+1] + quant_error * 1/16) / (2**DEPTH-1) ) * (2**DEPTH-1) ) ), file=f)
                        px[(y+1)*WIDTH+x+1] = InBetween( (px[(y+1)*WIDTH+x+1] + quant_error * 1/16) / (2**DEPTH-1) ) * (2**DEPTH-1)
            # DEBUG
            # print("Zeile: ", y, "Alt: ", str(oldpixel), "Neu: ", str(newpixel), px[y*WIDTH+x], file=f )
    return px


# def fsd( pixels, width, height, palette=1, serpentine=False ):
# 
#     for y in range( height ):
#         for x in range( width ):
#         
#             # Qualitätsverbesserung:
#             # IM Serpentin-Modus soll das Bild etwas weniger Artefakte produzieren
#             # if serpentine == True:
#             #    x = width -1 - x
# 
#             #
#             oldpixel = pixels[x,y]
#             newpixel = find_closest_palette_color( oldpixel, palette )
#             pixels[x,y] = newpixel
#             quant_error = ( oldpixel[0]-newpixel[0], oldpixel[1]-newpixel[1], oldpixel[2]-newpixel[2] )
#             
#             # push errors to neighbours
#             if x < width-1:
#                 pixels[x+1,y] = (
#                     int( round( pixels[x+1,y][0] + quant_error[0] * 7/16 ) ),
#                     int( round( pixels[x+1,y][1] + quant_error[1] * 7/16 ) ),
#                     int( round( pixels[x+1,y][2] + quant_error[2] * 7/16 ) )
#                 )
#             if x > 0 and y < height -1:
#                 pixels[x-1,y+1] = ( 
#                     int( round( pixels[x-1,y+1][0] + quant_error[0] * 3/16 ) ),
#                     int( round( pixels[x-1,y+1][1] + quant_error[1] * 3/16 ) ),
#                     int( round( pixels[x-1,y+1][2] + quant_error[2] * 3/16 ) )
#                 )
#             if y < height -1:
#                 pixels[x,y+1] = ( 
#                     int( round( pixels[x,y+1][0] + quant_error[0] * 5/16 ) ),
#                     int( round( pixels[x,y+1][1] + quant_error[1] * 5/16 ) ),
#                     int( round( pixels[x,y+1][2] + quant_error[2] * 5/16 ) )
#                 )
#             if x < width -1 and y < height -1:
#                 pixels[x+1,y+1] = ( 
#                     int( round( pixels[x+1,y+1][0] + quant_error[0] * 1/16 ) ),
#                     int( round( pixels[x+1,y+1][1] + quant_error[1] * 1/16 ) ),
#                     int( round( pixels[x+1,y+1][2] + quant_error[2] * 1/16 ) )
#                 )
#             
#             #
#             pixels[x,y] = ( pixels[x,y][0] << 4,pixels[x,y][1] << 4,pixels[x,y][2] << 4 )
