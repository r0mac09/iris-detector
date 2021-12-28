from pathlib import Path
import pickle

path_dir_baza_date = Path('./db')
path_backup = path_dir_baza_date / 'baza_date.backup'
path_baza_date = path_dir_baza_date / 'baza_date.pkl'


def intializare_baza_date():
    baza_date = {}

    if not path_dir_baza_date.exists():
        print('Directorul bazei de date nu exista in directorul curent.')
        path_dir_baza_date.mkdir()
        print('Director creat.')
    else:
        print('Incarcare baza de date.')
        if path_baza_date.exists():
            print('Baza de date exista.')
            with open(path_baza_date, 'rb') as f:
                baza_date = pickle.load(f)
                print('Baza date incarcata.')
        else:
            print('Baza de date nu exista.')
            if path_backup.exists():
                print('Incarcare backup.')
                with open(path_backup, 'rb') as f:
                    baza_date = pickle.load(f)
                    print('Baza de date incarcata din backup.')
            else:
                print('Backup al bazei de date nu exista.')

    if baza_date != {}:
        print('Baza de date:')
        for nume in baza_date:
            print(f'\t{nume}: {len(baza_date[nume])}')

    return baza_date


def salvare_baza_date(baza_date):
    if baza_date == {}:
        print('Baza de date este nepopulata')
        return

    if path_baza_date.exists():
        path_baza_date.replace(path_backup)
        print('Backup-ul bazei de date a fost salvat')

    with open(path_baza_date, 'wb') as f:
        pickle.dump(baza_date, f)
        print('Baza de date salvata.')
