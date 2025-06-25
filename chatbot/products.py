import os

file_name_list= os.listdir(r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\web scrapin V2\images")
images= []
f=open("chatbot\products.txt", "w")
for name in file_name_list:
    images.append(name.split(".")[0])
f.write("\n".join(images))
f.close()