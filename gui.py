from typing import Dict
import cv2
import PySimpleGUI as sg
from PIL import Image, ImageTk
from baza_date import incarca_bd_mock
import numpy as np

def selectare_nume(bd):
    layout = [[sg.Button(f'Adauga: {nume}', size=(25, 2)), sg.Button(
        f'Sterge: {nume}', button_color='Red', size=(25, 2))] for nume in bd.keys()]
    layout += [[sg.InputText()], [sg.Button('Adaugare nou')]]
    window = sg.Window('Selectare Nume', layout)

    nume = ''

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

        if event == 'Adaugare nou':
            if values[0] == '':
                sg.Popup('Campul este gol. Introduceti un nume',
                         keep_on_top=True)
            elif values[0] in bd.keys():
                sg.Popup('Numele se afla deja in baza de date',
                         keep_on_top=True)
            else:
                bd[values[0]] = []
                nume = values[0]
                break
        elif event.split()[1] in bd.keys():
            del bd[event.split()[1]]
            break

    window.close()

    return nume, bd


def achizitie_date(bd):
    nume, bd = selectare_nume(bd)

    if nume == '':
        return

    sg.Popup(['Apasati tasta SPACE pentru a captura un cadru',
             'Pentru a iesi apasati ESC'], keep_on_top=True)

    key = 0
    cap = cv2.VideoCapture(0)

    while key not in (ord('q'), ord('Q')):
        status, frame = cap.read()

        if not status:
            break

        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1)
        if key == 32:
            bd[nume].append(frame)
            print(f'Cadru salvat. Cadre salvate: {len(bd[nume])}')
        elif key == 27:
            cv2.destroyAllWindows()
            break


def imagini_de_afisat(bd, nume, pagina):
    blank = np.zeros((300, 300, 3), dtype=np.uint8)

    l_imagini = len(bd[nume])
    imagini = [Image.fromarray(bd[nume][i][:, :, ::-1]) for i in range(pagina*4, min((pagina+1)*4, l_imagini))]
    imagini = [img.resize((300, 300), resample=Image.BICUBIC) for img in imagini]
    imagini = [ImageTk.PhotoImage(img) for img in imagini]
    if len(imagini) < 4:
        imagini += [ImageTk.PhotoImage(Image.fromarray(blank))] * (4-len(imagini))
        
    return imagini


def afisare_baza_date(bd: Dict):
    nume = list(bd.keys())
    idx, pagina = 0, 0
    l_nume = len(nume)

    layout = [
        [sg.Image(size=(300, 300), key='i_0'), sg.Image(size=(300, 300), key='i_1')],
        [sg.Image(size=(300, 300), key='i_2'), sg.Image(size=(300, 300), key='i_3')],
        [sg.Button('Pagina Precedenta', size=(25, 2)), sg.Button('Pagina Urmatoare', size=(25, 2))],
        [sg.Button('Utilizatorul Precedent', size=(25, 2)), sg.Button('Utilizatorul Urmator', size=(25, 2))],
    ]

    window = sg.Window('Baza de date', layout, finalize=True)

    nume_curent = nume[idx]
    imagini = imagini_de_afisat(bd, nume_curent, pagina)

    for i in range(4):
        window[f'i_{i}'].update(data=imagini[i])

    while True:
        event, values = window.read()
    
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == 'Pagina Precedenta':
            pagina = (pagina-1) % int(len(bd[nume_curent])/4 + 1) 
            imagini = imagini_de_afisat(bd, nume_curent, pagina)
            for i in range(4):
                window[f'i_{i}'].update(data=imagini[i])
        elif event == 'Pagina Urmatoare':
            pagina = (pagina+1) % int(len(bd[nume_curent])/4 + 1)
            imagini = imagini_de_afisat(bd, nume_curent, pagina)
            for i in range(4):
                window[f'i_{i}'].update(data=imagini[i])
        elif event == 'Utilizatorul Precedent':
            pagina = 0
            idx = (idx-1) % len(nume)
            nume_curent = nume[idx]
            imagini = imagini_de_afisat(bd, nume_curent, pagina)
            for i in range(4):
                window[f'i_{i}'].update(data=imagini[i])
        elif event == 'Utilizatorul Urmator':
            pagina = 0
            idx = (idx+1) % len(nume)
            nume_curent = nume[idx]
            imagini = imagini_de_afisat(bd, nume_curent, pagina)
            for i in range(4):
                window[f'i_{i}'].update(data=imagini[i])  

    window.close()


def gui():
    sg.theme('DarkBlue')
    # All the stuff inside your window. This is the PSG magic code compactor...
    layout = [[sg.Button('Vizualizare Baza de Date', size=(25, 2))],
              [sg.Button('Editare Baza de Date', size=(25, 2))]]

    bd = incarca_bd_mock()

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events"
    while True:
        event, values = window.read()

        if event == 'Vizualizare Baza de Date':
            afisare_baza_date(bd)
        elif event == 'Editare Baza de Date':
            bd = achizitie_date(bd)

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

    window.close()


if __name__ == '__main__':
    gui()