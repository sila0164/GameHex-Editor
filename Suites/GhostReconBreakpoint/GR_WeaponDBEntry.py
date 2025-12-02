


def read():
    from core.file import current as file
    offset = 0

    #Initial values
    file.save('int16', 'Rate of Fire', 14)
    file.save('float', 'Projectile Breaking Angle', 56)

    #Range
    offset = file.intsearch(1684107084, 'int32', 56)
    if offset != 0: # If it does not find the range start it wont add range
        offset += 25
        if file.id in (1838530271017, 1838530266984):
            offset += 120
        file.save('float', 'Zero', offset)
        offset += 24
        if file.id in (1838530271017, 1838530266984):
            offset += 120
        file.save('float', 'Range', offset)

        #damage and penetration
    if file.id in (1698309626211, 1923391143335, 1698309626316):
        offset -= 8
    if "Maxim9" in file.name:
        offset = file.intsearch(1573516640874, 'int64', offset)
    elif "MK23" in file.name:
        offset = file.intsearch(1700302930594, 'int64', offset)
    else:
        offset = file.intsearch(1921650116144, 'int64', offset)
    if offset != 0:
        offset += 32
        file.save('int16', 'Damage', offset)
        offset += 24
        file.save('float', 'Penetration', offset)
        offset += 4
        file.save('float', 'Penetration Ratio', offset)



