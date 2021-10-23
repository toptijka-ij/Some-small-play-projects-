from tkinter import *
from tkinter import filedialog

import speech_recognition as sp_recog

from functional import file_audio_recognize, life_audio_recognize


def get_results(event, place, language_code, file_path=None):
    try:
        if file_path is None:
            res = life_audio_recognize(language_code)
        else:
            res = file_audio_recognize(file_path, language_code)
    except sp_recog.RequestError:
        Label(place, text='ERROR!').grid(column=0, row=2, columnspan=2, rowspan=2, padx=2, pady=2)
        Label(place, text='Check your connection with the Internet!').grid(column=0, row=2, columnspan=2, rowspan=2,
                                                                           padx=2, pady=2)
    except sp_recog.UnknownValueError:
        Label(place, text='ERROR!').grid(column=0, row=2, columnspan=2, rowspan=2, padx=2, pady=2)
        Label(place, text="The system can't recognize your data!").grid(column=0, row=2, columnspan=2, rowspan=2,
                                                                        padx=2, pady=2)
    else:
        Label(place, text='Result:').grid(column=0, row=2, columnspan=2, rowspan=2, padx=2, pady=2)
        text = Text(place, wrap=WORD, height=11, width=34)
        text.grid(column=0, row=4, columnspan=2, padx=2, pady=2)
        text.insert('1.0', res)
        scroll = Scrollbar(place, orient='vertical', command=text.yview)
        scroll.grid(row=0, column=2)
        text.config(yscrollcommand=scroll.set)


def work_window(event):
    new_window = Toplevel()
    new_window.resizable(False, False)
    new_window.geometry('300x300')
    new_window.title("Speech recognition")
    language_code = ''
    if language.get() == 'russian':
        language_code = 'ru-RU'
    elif language.get() == 'english':
        language_code = 'en-US'
    if audio_type.get() == 'file':

        def open_masker():
            return filedialog.askopenfilename(filetypes=(("Audio Files", ".mp3"), ("All Files", "*.*")))

        choose_file = Button(new_window, text='Choose file', width=16)
        choose_file.bind('<ButtonRelease-1>',
                         lambda event: get_results(event, language_code=language_code, place=new_window,
                                                   file_path=open_masker()))
        choose_file.grid(column=0, row=0, columnspan=2, rowspan=2, padx=2, pady=2)
    elif audio_type.get() == 'live speech':
        get_speech = Button(new_window, text='Click to start!')
        get_speech.bind('<ButtonRelease-1>',
                        lambda event: get_results(event, language_code=language_code, place=new_window))
        get_speech.grid(column=0, row=0, columnspan=2, rowspan=2, padx=2, pady=2)


if __name__ == '__main__':
    prep_window = Tk()
    prep_window.title("Speech recognition")
    prep_window.geometry('200x220')
    prep_window.resizable(False, False)
    prep_window.option_add('*Font', 'Tahoma 11')
    prep_window.option_add('*Label.Font', 'Tahoma 11 bold')
    prep_window.option_add('*Background', '#FFF8E9')
    prep_window['background'] = '#FFF8E9'
    Label(prep_window, text="Choose the language:", pady=5, padx=5).grid(column=0, row=0, columnspan=2, rowspan=2,
                                                                         padx=2, pady=2)
    language = StringVar()
    language.set('russian')
    rad1 = Radiobutton(prep_window, text='russian', variable=language, value='russian')
    rad2 = Radiobutton(prep_window, text='english', variable=language, value='english')
    rad1.grid(column=0, row=2, pady=5, padx=5)
    rad2.grid(column=1, row=2, pady=5, padx=5)
    Label(prep_window, text="Choose type of audio:", pady=5, padx=5).grid(column=0, row=3, columnspan=2, rowspan=2,
                                                                          padx=2, pady=2)
    audio_type = StringVar()
    audio_type.set('live speech')
    rad3 = Radiobutton(prep_window, text='file', variable=audio_type, value='file')
    rad4 = Radiobutton(prep_window, text='live speech', variable=audio_type, value='live speech')
    rad3.grid(column=0, row=5, pady=5, padx=5)
    rad4.grid(column=1, row=5, pady=5, padx=5)
    submit = Button(prep_window, text="Submit", width=10, height=1, pady=10, padx=10)
    submit.bind('<ButtonRelease-1>', work_window)
    submit.grid(column=0, row=6, columnspan=2, rowspan=2, padx=2, pady=2)
    prep_window.mainloop()
