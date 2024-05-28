from customtkinter import *
from PIL import Image

app = CTk()
app.geometry("600x480")
app.resizable(0,0)
app.iconbitmap('C:/Users/leonz/OneDrive/Área de Trabalho/collab_coins/templates/coin.ico')
app.title("Menu de login")

# Diretório de imagens
side_img_data = Image.open("C:/Users/leonz/OneDrive/Área de Trabalho/collab_coins/templates/side-img.png")
email_icon_data = Image.open("C:/Users/leonz/OneDrive/Área de Trabalho/collab_coins/templates/email-icon.png")
password_icon_data = Image.open("C:/Users/leonz/OneDrive/Área de Trabalho/collab_coins/templates/password-icon.png")

side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

# Tela principal
frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
frame.pack(expand=True, side="right")
frame.pack_propagate(0)


# Função para limpar o frame
def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()
