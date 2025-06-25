f=open("image_desc2\products.txt","r")
ch=""
for id,i in enumerate(f):
    ch=ch+"\n"+"id:"+str(id)+"/"+i.strip()
f.close()
f=open("image_desc2\products.txt","w")
f.write(ch.strip())
f.close()
print("Products updated with IDs.")