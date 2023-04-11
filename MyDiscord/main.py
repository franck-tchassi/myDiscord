import tkinter
from tkinter import *
from PIL import Image, ImageTk
from  ttkwidgets import *
import mysql.connector
from tkinter import messagebox
from socket import *
from threading import *
from tkinter import END
import datetime



# créer une fenetre principale
root = tkinter.Tk()
root.geometry("500x650")
root.title("DISCORD")
root.config(bg="black")
# importer une image
image = Image.open("image.png")
new_width = image.width // 8
new_height = image.height // 8
resized_image = image.resize((new_width, new_height))
photo = ImageTk.PhotoImage(resized_image)
label = Label(image=photo, bg="black")
label.place(x=150, y=37)

# se connecter à la base de donnée mysql
connecter = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "12Abcdef@",
    database = "myDiscord"
)
cursor = connecter.cursor()


class page_inscription:
    def __init__(self, master):
        self.master = master
    
    def open_inscription(self):
        inscription_root = Toplevel(self.master)
        inscription_root.geometry("500x650")
        inscription_root.title("inscription")
        inscription_root.config(bg="grey")

        titre1_label = Label(inscription_root, text="Saisissez vos informations", font= "size=25", bg="grey", fg="white")
        titre1_label.place(x=130, y=10)
        titre2_label = Label(inscription_root, text="d'inscription",font= "size=25", bg="grey", fg="white")
        titre2_label.place(x=180, y=40)

        self.nom_inscription = Label(inscription_root, text="Nom", bg="grey", fg="white")
        self.nom_inscription.place(x=100, y=80)
        self.nom_entry = Entry(inscription_root, width=48 )
        self.nom_entry.place(x=100, y=100)

        self.prenom_inscription = Label(inscription_root, text="Prenom", bg="grey", fg="white")
        self.prenom_inscription.place(x=100, y=130)
        self.prenom_entry = Entry(inscription_root, width=48 )
        self.prenom_entry.place(x=100, y=150)

        self.email_inscription = Label(inscription_root, text="Email", bg="grey", fg="white")
        self.email_inscription.place(x=100, y=180)
        self.email_entry = Entry(inscription_root, width=48 )
        self.email_entry.place(x=100, y=200)

        self.password_inscription = Label(inscription_root, text="password", bg="grey", fg="white")
        self.password_inscription.place(x=100, y=230)
        self.password_entry = Entry(inscription_root, width=48 )
        self.password_entry.place(x=100, y=250)

        self.btn_inscription = Button(inscription_root, text="S'inscrire", width=40, bg="blueviolet", fg="white", command=self.inscription_database)
        self.btn_inscription.place(x=100, y=300)
    
    def inscription_database(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        cursor = connecter.cursor()
        sql = "INSERT INTO inscription (nom, prenom, email, password) VALUES (%s, %s, %s, %s)"
        val = (nom, prenom, email, password)
        cursor.execute(sql, val)
        connecter.commit()
        print(cursor.rowcount, "personne inscrite")

        self.nom_entry.delete(0, END)
        self.prenom_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)


        cursor.close()
        connecter.close()

if connecter.is_connected:
    print("access à la base de donée")
    mon_inscription = page_inscription(root)



        

class connexion_page:
    def __init__(self, master):

        self.master = master
    def open_login(self):
        connexion_root = Toplevel(self.master)
        connexion_root.geometry("500x650")
        connexion_root.title("Connexion")
        connexion_root.config(bg="grey")

        self.titre1_label = Label(connexion_root, text="Ha, te revoila !", font= "size=25", bg="grey", fg="white")
        self.titre1_label.pack()
        self.titre2_label = Label(connexion_root, text="Nous sommes siheureux de te revoir !", bg="grey", fg="white")
        self.titre2_label.place(x=160, y=40)


        self.nom_label = Label(connexion_root, text="Nom", bg="grey", fg="white")
        self.nom_label.place(x=100, y=80)
        self.nom_entry = Entry(connexion_root, width=48 )
        self.nom_entry.place(x=100, y=100)
        self.password_label = Label(connexion_root, text="password", bg="grey", fg="white")
        self.password_label.place(x=100, y=130)
        self.password_entry = Entry(connexion_root, width=48, show="*")
        self.password_entry.place(x=100, y=150)
        
        

        self.btn_connexion = Button(connexion_root, text="connexion", width=40, bg="blueviolet", fg="white", command=self.connexion_database)
        self.btn_connexion.place(x=100, y=200)

    def connexion_database(self):
        nom = self.nom_entry.get()
        password = self.password_entry.get()

        cursor = connecter.cursor()
        sql = "SELECT * FROM inscription WHERE nom=%s AND password=%s"
        val = (nom, password)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        if result:
            return accueil.open_accueil()
            
        else:
            messagebox.showerror("Erreur", "Nom ou mot de passe incorrect")
        
        self.nom_entry.delete(0, END)
        self.password_entry.delete(0, END)
        cursor.close()

    


if connecter.is_connected:
    se_connecter = connexion_page(root)   
#se_connecter.page_connexion()


class page_accueil:
    def __init__(self, master):
        self.master = master
        self.txtMessages = None 
        self.clientSocket = None

    def open_accueil(self):
        accueil_root = Toplevel(self.master)
        accueil_root.geometry("500x650")
        accueil_root.title("chat")
        accueil_root.config(bg="grey")

        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        hostIp = "127.0.0.1"
        portNumber = 7500
        self.clientSocket.connect((hostIp, portNumber))
        self.txtMessages = Text(accueil_root, width=50)
        self.txtMessages.grid(row=0, column=0, padx=10, pady=10)

        self.txtYourMessage = Entry(accueil_root, width=50)
        self.txtYourMessage.insert(0,"Your message")
        self.txtYourMessage.grid(row=1, column=0, padx=10, pady=10)

        btnSendMessage = Button(accueil_root, text="Send", width=20, command=self.sendMessage)
        btnSendMessage.grid(row=2, column=0, padx=10, pady=10)

        recvThread = Thread(target=self.recvMessage)
        recvThread.daemon = True
        recvThread.start()
        
    
    def sendMessage(self):
        maintenant = datetime.datetime.now()
        heure = maintenant.strftime("%H:%M:%S")
        clientMessage = self.txtYourMessage.get()
        message = f"You: {clientMessage}      {heure}"
        self.txtMessages.insert(END, "\n" + message)
        self.clientSocket.send(clientMessage.encode("utf-8"))
    
    def recvMessage(self):
        while True:
            serverMessage = self.clientSocket.recv(1024).decode("utf-8")
            print(serverMessage)
            self.txtMessages.insert(END, "\n"+serverMessage)
    
    

accueil = page_accueil(root)


    









label = tkinter.Label(root, text="Discord", fg="white", bg="black", font= "size=25")
label.place(x=250, y=50)

label = tkinter.Label(root, text="Bienvenue  sur  Discord", fg="white", bg="black", font= "size=19")
label.place(x=145, y=330)
label = tkinter.Label(root, text="Rejoins plus de 100 milloins de personnes", fg="white", bg="black")
label.place(x=140, y=380)
label = tkinter.Label(root, text="qui utilisent Discord  pour discuter avec leurs", fg="white", bg="black")
label.place(x=130, y=400)
label = tkinter.Label(root, text="communautautés et leurs amis.", fg="white", bg="black")
label.place(x=160, y=420)
inscription = tkinter.Button(root, text="S'inscrire", width=40, bg="blueviolet", fg="white", highlightthickness=0, command=mon_inscription.open_inscription)
inscription.place(x=105, y=500)
inscription.configure(bd=0)
connexion = tkinter.Button(root, text="connexion", width=40, bg="blueviolet", fg="white", highlightthickness=0, command=se_connecter.open_login)
connexion.place(x=105, y=550)
connexion.configure(bd=0)











root.mainloop()
