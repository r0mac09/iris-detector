import cv2
import PySimpleGUI as sg

baza_date = {}


def selectare_nume():
    layout = [[sg.Button(f'Adauga: {nume}', size=(25, 2)), sg.Button(
        f'Sterge: {nume}', button_color='Red', size=(25, 2))] for nume in baza_date.keys()]
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
            elif values[0] in baza_date.keys():
                sg.Popup('Numele se afla deja in baza de date',
                         keep_on_top=True)
            else:
                baza_date[values[0]] = []
                nume = values[0]
                break
        elif event.split()[1] in baza_date.keys():
            nume = event
            break

    window.close()

    return nume


def achizitie_date():
    nume = selectare_nume()

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

            baza_date[nume].append(frame)
            print(f'Cadru salvat. Cadre salvate: {len(baza_date[nume])}')
        elif key == 27:
            cv2.destroyAllWindows()
            break


def gui():
    sg.theme('DarkBlue')
    # All the stuff inside your window. This is the PSG magic code compactor...
    layout = [[sg.Button('Vizualizare Baza de Date', size=(25, 2))],
              [sg.Button('Editare Baza de Date', size=(25, 2))]]

    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events"
    while True:
        event, values = window.read()

        if event == 'Vizualizare Baza de Date':
            pass
        elif event == 'Editare Baza de Date':
            achizitie_date()

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break

    window.close()
