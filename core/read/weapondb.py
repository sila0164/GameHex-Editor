import main
from core.search import typesearch, dictsearch

def weapondbread():
    stats = main.file.stats
    id = main.file.id
    filename = main.file.name
    print("weapondbread")
    with open(main.file.path, "rb+") as f:
        #Initial values
        stats["rateoffire"] = Int16(14)
        stats["projectilebreakingangle"] = Float(56)

        #Range
        offset = typesearch(1684107084, 4, 56)
        offset += 25
        if id in (1838530271017, 1838530266984):
            offset += 120
        stats["zero"] = Float(offset)
        offset += 24
        if id in (1838530271017, 1838530266984):
            offset += 120
        stats["range"] = Float(offset)

        #damage and penetration
        if id in (1698309626211, 1923391143335, 1698309626316):
            offset -= 8
        elif "Maxim9" in filename:
            offset = typesearch(1573516640874, 8, offset)
        elif "MK23" in filename:
            offset = typesearch(1700302930594, 8, offset)
        else:
            offset = typesearch(1921650116144, 8, offset)
        offset += 32
        stats["damage"] = Int16(offset)
        offset += 24
        stats["penetration1"] = Float(offset)
        offset += 4
        stats["penetration2"] = Float(offset)

        #for testing
        print(main.file)
        #print(main.file.stats)

