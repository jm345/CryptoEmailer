import smtplib
from tkinter import messagebox,Button,Label,Text,Tk,Entry,Frame,PhotoImage,filedialog,StringVar,Menu,Toplevel,Checkbutton,IntVar,LabelFrame
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import os
import requests
from datetime import datetime

class LoginWindow:

    def __init__(self,master):

        self.master = master

        # Variables
        self.is_checked = IntVar()

        # Widgets
        self.tl_login = Toplevel()
        self.tl_login.title('Simple Email Client v1.0')
        self.credential_frame = Frame(self.tl_login)
        self.label_info = Label(self.credential_frame,text = 'Enter your email address and password.')
        self.label_user = Label(self.credential_frame,text = 'Username: ')
        self.label_password = Label(self.credential_frame, text = 'Password: ')
        self.entry_user = Entry(self.credential_frame,width = 40)
        self.entry_password = Entry(self.credential_frame, width = 40,show = '*')
        self.button_verify = Button(self.tl_login,text = 'Sign In',command = self.verify_user)
        self.check_password = Checkbutton(self.credential_frame, variable = self.is_checked)
        self.label_check_password = Label(self.credential_frame,text = 'Show Password: ')

        # Bindings
        self.check_password.bind('<Button-1>',self.show_password)

        # Layout
        self.credential_frame.grid(row = 0,column = 0,padx = 5,pady = 5)
        self.label_info.grid(columnspan = 2,padx = 10,pady = 10)
        self.label_user.grid(row = 1,column = 0,padx = 5,pady = 5,sticky = 'W')
        self.label_password.grid(row=2, column=0, padx=5, pady=5,sticky = 'W')
        self.entry_user.grid(row=1, column=1, padx=5, pady=5)
        self.entry_password.grid(row=2, column=1, padx=5, pady=5)
        self.button_verify.grid(padx = 10,pady = 10)
        self.label_check_password.grid(padx = 5,pady = 5, sticky = 'W')
        self.check_password.grid(pady = 5,column = 1,row = 3, sticky = 'W')

    def verify_user(self):

        if self.entry_user.get() == '' or self.entry_password.get() == '':
            messagebox.showerror('Empty Fields','You must enter a valid email address and password.')
            return

        try:
            # Open a connection and login using the user credentials. If successful, destroy login window and move to main window.
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(self.entry_user.get(),self.entry_password.get())
            self.master.deiconify()
            MainWindow(self.master,self.entry_user.get(), self.entry_password.get())
            self.tl_login.destroy()

        except smtplib.SMTPAuthenticationError:
            # Raise exception and clear user and password fields.
            messagebox.showerror('Authentication Error','You have entered an incorrect username or password. Please try again.')
            self.entry_password.delete(0, len(self.entry_password.get()))
            self.entry_user.delete(0,len(self.entry_user.get()))

    def show_password(self,event):

        if self.is_checked.get() == 0:
            self.entry_password.config(show='')
        else:
            self.entry_password.config(show='*')

class MainWindow:

    def __init__(self,master,user,password):

        self.master = master
        master.title('Simple Email Client v1.0')

        # Credentials
        self.username = user
        self.password = password
        self.default_receiver = 'justin.butler4564@gmail.com'

        # Variables
        self.xrp_enabled = StringVar()
        self.ada_enabled = StringVar()
        self.xlm_enabled = StringVar()
        self.iota_enabled = StringVar()
        self.eos_enabled = StringVar()
        self.xem_enabled = StringVar()
        self.sc_enabled = StringVar()
        self.var_list = []
        self.var_list.append(self.xrp_enabled)
        self.var_list.append(self.ada_enabled)
        self.var_list.append(self.xlm_enabled)
        self.var_list.append(self.iota_enabled)
        self.var_list.append(self.eos_enabled)
        self.var_list.append(self.xem_enabled)
        self.var_list.append(self.sc_enabled)
        self.user_currencies = ['ADA','XLM','IOTA','XRP','EOS','XEM','SC']
        self.user_currencies_names = {'ADA': 'Cardano', 'XLM': 'Stellar', 'IOTA': 'IOTA', 'MIOTA': 'IOTA', 'XRP': 'Ripple','EOS': 'EOS', 'XEM': 'NEM', 'SC': 'Siacoin'}
        self.currencies = {'NZD':'NZ Dollar','USD':'US Dollar'}
        self.display_currencies = str(self.user_currencies_names.values())[13:-2]

        # Widgets
        # Frame 1
        self.input_frame = Frame(master)
        self.input_sender_l = Label(self.input_frame,text = 'From: ')
        self.input_sender_mail = Entry(self.input_frame,width = 60)
        self.input_sender_mail.insert(0,self.username)
        self.receiver_label = Label(self.input_frame,text = 'To: ')
        self.input_receiver_mail = Entry(self.input_frame,width = 60)
        self.label_subject = Label(self.input_frame,text = 'Subject: ')
        self.input_subject = Entry(self.input_frame,width = 60)
        #self.label_attachement = Label(self.input_frame, text='Attach')
        #self.image_attachment = PhotoImage(file='C:\\Users\\Jordan\\Desktop\\giphy.gif')
        #self.button_attach = Button(self.input_frame, image=self.image_attachment, width=20, height=20,command=self.attach_file)
        self.label_frame_currencies = LabelFrame(self.input_frame)
        self.label_crypto_list = Label(self.label_frame_currencies, text='Current crypto currency list:')
        self.text_user_currencies = Text(self.label_frame_currencies,font = 'Arial',wrap = 'word',height = 3,width = 25,padx = 5,pady = 5)
        self.text_user_currencies.insert(1.0,self.display_currencies.replace('\'',''))
        self.text_user_currencies.config(state = 'disabled')

        # Frame 2
        self.send_frame = Frame(master)
        self.message = Text(self.send_frame, font='Arial', padx=5, pady=5, width=70)
        self.send_button = Button(self.send_frame, text='Send', width=20, command=self.send_mail)
        self.button_retrieve = Button(self.send_frame, text='Retrieve', width=20, command=self.get_crypto)

        # Layout
        # Frame 1
        self.input_frame.grid(sticky = 'W',padx = 5,pady = 5)
        self.input_sender_l.grid(row = 0,column = 0,sticky = 'W')
        self.input_sender_mail.grid(row = 0,column = 1,padx = 5,pady = 5)
        self.receiver_label.grid(row = 1,column = 0, sticky = 'W')
        self.input_receiver_mail.grid(row = 1,column = 1,padx = 5,pady = 5)
        self.label_subject.grid(row = 2,column = 0, sticky = 'W')
        self.input_subject.grid(row = 2,column = 1,padx = 5,pady = 5,sticky = 'N')
        self.label_frame_currencies.grid(sticky='se',padx = 5,pady = 5,row = 0,column = 2,rowspan = 3)
        self.label_crypto_list.grid(column = 0,row = 0)
        #self.label_users_currencies.grid(sticky = 'nswe',column = 0,row = 1)
        self.text_user_currencies.grid(padx = 10,pady = 10,sticky = 'nsew')

        # Frame 2
        self.send_frame.grid(sticky = 'S')
        self.message.grid(padx=20, pady=5)
        self.send_button.grid(row = 1,sticky = 'e',padx=100, pady=5)
        self.button_retrieve.grid(row = 1,sticky = 'w',padx = 100,pady = 5)

        # Menus
        # File Menu
        self.menubar = Menu(master)
        self.file_menu = Menu(self.menubar,tearoff = 0)
        self.file_menu.add_command(label = 'New')
        self.file_menu.add_command(label = 'Open')
        self.file_menu.add_command(label = 'Save')
        self.file_menu.add_command(label = 'Save As')
        self.file_menu.add_separator()
        self.file_menu.add_command(label = 'Exit',command = self.master.quit)
        self.menubar.add_cascade(label = 'File',menu = self.file_menu)

        # Edit Menu
        self.edit_menu = Menu(self.menubar,tearoff = 0)
        self.edit_menu.add_command(label = 'Clear All Fields',command = self.clear_all)
        self.edit_menu.add_command(label = 'Clear Text Box',command = self.clear_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label = 'Use Default Fields',command = self.default_fields)
        self.menubar.add_cascade(label = 'Edit',menu = self.edit_menu)

        # Retrieve Menu
        self.retrieve_menu = Menu(self.menubar,tearoff = 0)
        self.retrieve_menu.add_command(label = 'Update Currency Data',command = self.select_crypto)
        self.menubar.add_cascade(label = 'Retrieve',menu = self.retrieve_menu)
        self.master.config(menu = self.menubar)

    def default_fields(self):
        self.input_sender_mail.delete(0, len(self.input_sender_mail.get()))
        self.input_sender_mail.insert(0,self.username)
        self.input_receiver_mail.delete(0, len(self.input_receiver_mail.get()))
        self.input_receiver_mail.insert(0,self.default_receiver)
        self.input_subject.delete(0, len(self.input_subject.get()))
        self.input_subject.insert(0,'Crypto Daily Price')

    def clear_text(self):
        self.message.delete(1.0, 'end-1c')

    def clear_all(self):
        self.input_sender_mail.delete(0,len(self.input_sender_mail.get()))
        self.input_receiver_mail.delete(0,len(self.input_receiver_mail.get()))
        self.input_subject.delete(0,len(self.input_subject.get()))
        self.message.delete(1.0,'end-1c')

    def send_mail(self):
        # Create the email, connect to a SMTP server then send the email.
        try:
            msg = MIMEMultipart()
            msg['From'] = self.input_sender_mail.get()
            msg['To'] = self.input_receiver_mail.get()
            recipients = msg['To'].split(',')
            msg['Subject'] = self.input_subject.get()
            body = self.message.get(1.0, 'end-1c')
            msg.attach(MIMEText(body, 'plain'))
            '''file, attachment = self.attach_file()
            part = MIMEBase('application', 'octet stream')
            part.set_payload(attachment.read())
            encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename= ' + file)
            msg.attach(part)'''
            email = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(msg['From'], self.password)
            server.sendmail(msg['From'], recipients, email)
            server.quit()
            messagebox.showinfo('Successfully Sent', 'Message has been delivered successfully.')

        except smtplib.SMTPAuthenticationError:
            messagebox.showerror('Incorrect Username or Password','Please enter a valid email address and password.')

    def attach_file(self):
        self.attachment_description = StringVar()
        try:
            file_path = filedialog.askopenfilename()
            attach_file = open(file_path, 'rb')
        except FileNotFoundError:
            return
        self.input_attach = Entry(self.input_frame, width=60)
        self.input_attach.grid(row=3, column=1, padx=5, pady=5)
        self.label_attach = Label(self.input_frame, text='Attached: ')
        self.label_attach.grid(row=3, column=0)
        self.attachment_description = self.file_path
        self.input_attach.insert(0, os.path.basename(self.attachment_description) + ', ')
        self.input_attach['state'] = 'disabled'
        return self.file_path, self.attach_file

    def select_crypto(self):
		# Creates a new window for the user to select which currencies they would like to receive information for.
        coin_list = ['ADA - Cardano', 'XLM - Stellar', 'IOTA - IOTA', 'XRP - Ripple', 'EOS - EOS', 'XEM - NEM','SC - Siacoin']
        self.window_currency_select = Toplevel()
        self.checkbutton_frame = Frame(self.window_currency_select)
        self.label_select = Label(self.checkbutton_frame, text='Please select the currencies you would like to retrieve.')
        self.button_confirm = Button(self.window_currency_select, text='Retrieve',command = self.store_currencies)
        self.button_update = Button(self.window_currency_select,text = 'Update',command = self.update_crypto_list)
        self.checkbutton_frame.grid()
        self.label_select.grid(padx=5, pady=5)
        self.button_ada = Checkbutton(self.checkbutton_frame,offvalue = '',onvalue = 'ADA',text = coin_list[0],variable = self.ada_enabled)
        self.button_xlm = Checkbutton(self.checkbutton_frame,offvalue = '',onvalue = 'XLM', text=coin_list[1],variable = self.xlm_enabled)
        self.button_iota = Checkbutton(self.checkbutton_frame,offvalue = '',onvalue = 'IOTA', text=coin_list[2],variable = self.iota_enabled)
        self.button_xrp = Checkbutton(self.checkbutton_frame,offvalue = '',onvalue = 'XRP', text=coin_list[3],variable = self.xrp_enabled)
        self.button_eos = Checkbutton(self.checkbutton_frame,offvalue = '',onvalue = 'EOS', text=coin_list[4],variable = self.eos_enabled)
        self.button_xem = Checkbutton(self.checkbutton_frame,offvalue = '',onvalue = 'XEM', text=coin_list[5],variable = self.xem_enabled)
        self.button_sc = Checkbutton(self.checkbutton_frame,offvalue = '',onvalue = 'SC', text=coin_list[6],variable = self.sc_enabled)
        self.button_ada.grid(padx = 5,pady = 5,sticky = 'W')
        self.button_xlm.grid(padx = 5,pady = 5,sticky = 'W')
        self.button_iota.grid(padx = 5,pady = 5,sticky = 'W')
        self.button_xrp.grid(padx = 5,pady = 5,sticky = 'W')
        self.button_eos.grid(padx = 5,pady = 5,sticky = 'W')
        self.button_xem.grid(padx = 5,pady = 5,sticky = 'W')
        self.button_sc.grid(padx = 5,pady = 5,sticky = 'W')
        self.button_confirm.grid(sticky = 'w',row = 1,padx = 80,pady = 5)
        self.button_update.grid(sticky = 'e',row = 1,padx = 80,pady = 5)

    def store_currencies(self):
        # Store the users current cryptos in a list. The function within performs the actual GET based on the cryptos that are requested.
        self.user_currencies.clear()
        for currency in self.var_list:
            if currency.get() != '':
                self.user_currencies.append(currency.get())
        self.get_crypto()
        self.window_currency_select.destroy()

    def get_crypto(self):
        # Form a get request using the users current check list. Returns a message which contains recent pricing for the currencies.
        self.message.delete(1.0, 'end-1c')
        self.base_uri = 'https://min-api.cryptocompare.com/data/pricemulti?'
        self.cryptos_fsyms = 'fsyms='
        self.currencies_tsyms = 'tsyms=NZD,USD'
        for i in self.user_currencies:
            self.cryptos_fsyms = self.cryptos_fsyms + i + ','
        self.user_get = self.base_uri + self.cryptos_fsyms.rstrip(',') + '&' + self.currencies_tsyms
        self.get = requests.get(self.user_get)
        self.parsed_req = self.get.json()
        self.message.insert(1.0,'Currency List\n')
        self.message.insert(2.0, '=' * 30 + '\n')
        self.message.insert(3.0,'\n')
        i = 4.0
		
		# Formats the data into main window text box.
        for key in self.parsed_req.keys():
            nzd = str(self.parsed_req[key]['NZD'])
            usd = str(self.parsed_req[key]['USD'])
            self.message.insert(i,self.user_currencies_names[key] + ': \n')
            self.message.insert(i + 1, str(self.currencies['NZD']) + ' - $' + nzd + ', ' + str(self.currencies['USD']) + ' - $' + usd + '\n')
            self.message.insert(i + 2,'\n')
            i += 3
        self.message.insert(i, '=' * 30 + '\n')
        self.message.insert(i + 1, '\n')
        self.message.insert(i + 2, 'Retrieved at: ')
        self.message.insert(i + 3, str(datetime.now()) + '\n')
        self.update_crypto_list()

    def update_crypto_list(self):

        self.user_currencies.clear()
        self.display_currencies = ''

        for currency in self.var_list:
            if currency.get() != '':
                self.user_currencies.append(currency.get())
        for crypto in self.user_currencies:
            if self.user_currencies_names[crypto]:
                self.display_currencies += self.user_currencies_names[crypto] + ', '

        self.text_user_currencies.config(state='normal')
        self.text_user_currencies.delete(1.0, 'end-1c')
        self.text_user_currencies.insert(1.0, self.display_currencies)
        self.text_user_currencies.config(state='disabled')

    def schedule_notifications(self):
        pass

def main():
    root = Tk()
    LoginWindow(root)
    #MainWindow(root)
    root.withdraw()
    root.mainloop()

main()
