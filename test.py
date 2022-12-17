# import psycopg2 as db
# from psycopg2 import OperationalError
#
#
# class Connection:
#     __conn = None
#     __cur = None
#
#     def __init__(self):
#         # load all the database connection details from the environment variable file
#         self.__dbuser = "username"
#         self.__dbname = "database_name"
#         self.__password = "password"
#         self.__host = "localhost"
#         self.__port = "5432"
#         # connect to database
#         self.__connect()
#         self.__dbcur = Connection.__cur
#         self.__dbconn = Connection.__conn
#
#     def __connect(self):
#         try:
#             if Connection.__conn is None:
#                 Connection.__conn = db.connect(database=self.__dbname, user=self.__dbuser,
#                                                             password=self.__password,
#                                                             host=self.__host, port=self.__port)
#                 Connection.__conn.autocommit = True
#                 Connection.__cur = Connection.__conn.cursor()
#         except OperationalError as e:
#             raise e
#
#     @property
#     def cursor(self):
#         return self.__dbcur
#
#     def close(self):
#         self.__dbconn.close()
#

# import tkinter as tk
# from tkinter import ttk
# from tkinter.messagebox import showinfo
#
# root = tk.Tk()
# root.title('Treeview demo')
# root.geometry('620x200')
#
# # define columns
# columns = (1, 2, 3, 4, 5, 6, 7)
#
# tree = ttk.Treeview(root, columns=columns, show="headings")
#
# # define headings
# tree.heading(1, text='First Name')
# tree.heading(2, text='Last Name')
# tree.heading(3, text='Email')
# tree.heading(4, text='Email2')
# tree.heading(5, text='Email3')
# tree.heading(6, text='Email4')
# tree.heading(7, text='Email5')
#
# # generate sample data
# contacts = []
# for n in range(1, 100):
#     contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))
#
# # add data to the treeview
# for contact in contacts:
#     tree.insert('', tk.END, values=contact)
#
#
# def item_selected(event):
#     for selected_item in tree.selection():
#         item = tree.item(selected_item)
#         record = item['values']
#         # show a message
#         showinfo(title='Information', message=','.join(record))
#
#
# tree.bind('<<TreeviewSelect>>', item_selected)
#
# tree.grid(row=0, column=0, sticky='nsew')
#
# # add a scrollbar
# scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
# tree.configure(yscroll=scrollbar.set)
# scrollbar.grid(row=0, column=1, sticky='ns')
#
# # run the app
# root.mainloop()

import re

string = "abgc4687"
m = re.fullmatch(
    r"([a-zA-Z]{4,}(\d+)?)$",
    string)
print(m)
