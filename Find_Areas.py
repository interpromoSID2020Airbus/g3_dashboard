########################################################
#File containing the functions of the Aircraft Plan tab#
########################################################


'''
input : json file containing all the data
        name of the selected aircraft type
output : all the coordinates of all the seats of the aircraft
'''
def find_coordinates(file, name_aircraft):
    dico_seat = {}
    for type_seat in file[name_aircraft]:
        for seat in file[name_aircraft][type_seat]:
            seat = seat.replace("(","")
            seat = seat.replace(")","")
            seat = seat.replace(",","")
            coor = seat.split(" ")
            dico_seat[seat] = [int(coor[0])-int(coor[2])/2,
                               int(coor[1])-int(coor[3])/2,
                               int(coor[0])+int(coor[2])/2,
                               int(coor[1])+int(coor[3])/2]
    return dico_seat

'''
input : json file containing all the data
        name of the selected aircraft type
output : all the seats and their class for the dropdown
'''
def find_seats(file, name_aircraft):
    list_seat = []
    n_seat = 0
    for type_seat in file[name_aircraft]:
        type_seat_clean = type_seat.replace("_"," ")
        type_seat_clean = type_seat_clean.title()
        for seat in file[name_aircraft][type_seat]:
            list_seat.append("Seat N°" + str(n_seat) + " - " + str(type_seat_clean))
            n_seat += 1
    return list_seat

'''
input : json file containing all the data
        name of the selected aircraft type
        name of the selected seat
output : all the elements found in the aircraft with the coordinates and the
         distance with the seat
'''
def find_elements(file, name_aircraft, name_seat):
    split_seat = str(name_seat).split(" - ")
    n_seat = split_seat[0].replace("Seat N°", "")
    try:
        type_seat = split_seat[1].replace(" ", "_").upper()
        all_seat = file[name_aircraft][type_seat]
        key_seat = list(all_seat.keys())[int(n_seat)]
        elements = all_seat[key_seat]
        return elements
    except:
        return {}