import click
import pyperclip

from kvnoteafly.db.models import create_session, Note, NoteCategory, NoteType

PARAMS = {
    "category":  None,
    "note_type": None,
    }


@click.command()
def create():
    """Simple script to quickly create notes"""
    click.echo("This is a simple program to create notes via clipboard")
    session = create_session()
    while True:
        try:
            make_new = input("Create a new note? [y/n]")
            if make_new == "y":
                create_note(session)
            else:
                click.echo("Goodbye")
                return
        except Exception as e:
            print(e)
            click.echo("Goodbye")
            return


def get_params():
    global PARAMS
    if all(PARAMS.values()):
        print(f"Last used\nCategory: {PARAMS['category']}\nNote_Type: {PARAMS['note_type']}")
        use_same = input("Use the same params? [y/n]")
        if use_same == "y":
            return PARAMS
    # category
    categories = {i: NoteCategory(i) for i in range(len(NoteCategory))}
    for k, v in categories.items():
        print(f"{k} : {v.name}")

    user_cat = int(input(f"Select category [{min(categories)}-{max(categories)}]: "))

    # note type
    note_types = {i: NoteType(i) for i in range(len(NoteType))}
    for k, v in note_types.items():
        print(f"{k} : {v.name}")

    user_type = int(input(f"Select note type [{min(note_types)}-{max(note_types)}]: "))

    PARAMS['category'] = user_cat
    PARAMS['note_type'] = user_type
    return PARAMS


def create_note(session):
    params = get_params()

    note_type = params['note_type']
    note_category = params['category']

    def handle_key_note():
        keys = []
        while True:
            try:
                if keys:
                    print(",".join(keys))
                key = input("Enter a key, type 'done' when finished")
                if key == 'done':
                    note = Note()
                    note.keys = keys
                    note.category = NoteCategory(note_category)
                    note.note_type = NoteType(note_type)
                    return note
                else:
                    keys.append(key)
            except:
                return None

    def handle_other_note():
        ok = input("Ready to get clipboard contents? [y/n]")
        if ok == "n":
            return

        note = Note()
        note.text = pyperclip.paste()
        note.category = NoteCategory(params['category'])
        note.note_type = NoteType(params['note_type'])
        return note

    if note_type == NoteType.KEYBOARD_NOTE.value:
        note = handle_key_note()
    else:
        note = handle_other_note()
    if note:
        note.title = input("Note Title ?")
        session.add(note)
        session.commit()


if __name__ == '__main__':
    create()
