# Prüft ob der eingegebene Wert in eine Ganzzahl umgewandelt werden kann
def isInt(value):
  try:
    int(value)
    return True
  except ValueError:
    return False


# Quantity beschreibt den Exponent der Basis 2 abzgl. 1
# 2^0-1 = 0, 2^1-1 = 1, 2^2-1 = 3, 2^3-1 = 7 usw.
def palette():
    print("Die Farbpalette bestimmt, die Anzahl der Farbabstufungen, die ausgegeben wird.")
    print("0=256, 1=128, 2=64 ... 7=2 Farbabstufungen.")
    print("0 ≤ Eingabe ≤ 7")
    
    while True:
        quantity = input( "Geben Sie die Farbpalette ein [0]: ")
        if quantity == "":
            quantity = 0
        if isInt(quantity):
            if int(quantity) in range(8):
                return int(quantity)
        print("Eingabe ungültig.")


# Angabe des Farbkanals (0=Rot in RGB, 1=Grün in RGB, 2=Blau in RGB)
def farbkanal():
    print("\r\nGeben Sie einen Farbkanal an. ")
    print("Bei RGB geben Sie bitte 0 bis 2 für Rot, Grün oder Blau an.")
    print("Bei YCbCr geben Sie bitte 3 für Rot, 4 für Grün und 5 für Blau an")

    while True:
        channel = input( "Geben Sie den Kanal ein [0]: ")
        if channel == "":
            channel = 0
        if isInt(channel):
            if int(channel) in range(6):
                return int(channel)
        print("Eingabe ungültig.")
    


# Soll Dithering verwendet werden, muss der wahrgenommene Farbraum höher sein, als
# der tatsächliche Farbraum, den ich zuvor via "quantisierung" abgefragt habe
def vFarbraum():
    print("\r\nWollen Sie mit Dithering die wahrgenommene Bildqualität durch Dithering optimieren?")
    print("Geben Sie 0 ein, um den wahrgenommenen Farbraum gemäß dem tatsächlichen Farbraum")
    print("abzubilden.")
    print("Geben Sie 1..3 ein, um den wahrgenommenen Farbraum zu verdoppeln, zu vervierfachen ")
    print("oder zu verachtfachen. (1=2x, 2=4x und 3=8x)")
    print("0 ≤ Eingabe ≤ 3")

    dither = None
    while True:
        dither = input( "Erweiterung des virtuellen Farbraums [0]: " )
        if dither == "":
            dither = 0
        if isInt(dither):
            if int(dither) in range(4):
                return int(dither)
        print("Eingabe ungültig.")