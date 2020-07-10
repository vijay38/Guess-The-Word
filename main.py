from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from time import *
#import pyrebase
import time
import sqlite3
from tkinter import messagebox
from tkinter.font import Font
from pymongo import MongoClient
import webbrowser
import os
import dotenv
 
dotenv.load_dotenv()
global proceed
global update
update=0
proceed=0

doc=1
try:
    client=MongoClient(os.getenv("link"))
    mongodb=client.get_database("guess_the_word")
    mongocoll=mongodb.isupdate
    check=list(mongocoll.find({},{"_id":0}))
    if check[0]["update1"]==1:
        update=1
    internet=1
except Exception:
    internet=0
    pass      
try:
    conn=sqlite3.connect(".img\\Guesstheword.db")
    c=conn.cursor()
    c.execute("SELECT * FROM Player_Info")
    records=c.fetchall()
    global que
    que=records[0][2]
    if records[0][0]!="enter your name":
        proceed=1
        global userid
        userid=records[0][0]
except Exception:
    doc=0
    messagebox.showerror("File Missing!","One of our files are Missing!\nPlease Download again!")
if doc==1 and update==1:
    root=Tk()
    root.title("Update")
    root.configure(bg="hot pink")
    root.iconbitmap(".img\\icon2.ico")
    label1=Label(root,text="We Have An update!\Please Download it\nBy pressing this button",fg="white",bg="hot pink",font="impact 20 bold")
    label1.pack()
    button1=Button(root,text="Click Here",font="times 16 bold",fg="white",bg="green",command=lambda: webbrowser.open("https://drive.google.com/drive/folders/11fP2Z-w68XH1QbEXIVmttmRDQ7E7OhWC?usp=sharing"))    
    button1.pack()
    root.mainloop()
if internet==1 and doc==1 and update==0:
    root=Tk()
    root.title("Build The Word")
    root.configure(bg="black")
    global ques
    global total_words
    global l1
    global dispque
    global dispans
    if proceed==1:
        try:
            client=MongoClient(os.getenv("link"))
            mongodb=client.get_database("guess_the_word")
            mongocoll=mongodb.users
            quelist=list(mongocoll.find({"name":userid},{"question":1,"_id":0}))
            ques=quelist[0]["question"]
            mongocoll=mongodb.pair_list
            displist=list(mongocoll.find({"_id":ques},{"_id":0}))
        except Exception:
            messagebox.showerror("No internet","Please restart again!")
            root.after(3000,lambda: root.destroy())
        dispque=displist[0]["jumble"]
        dispans=displist[0]["correct"]
        total_words=mongocoll.count_documents({})
        client.close()
    canvas=Canvas(root,height=600,width=600,bg="AntiqueWhite1")
    canvas.pack()
    global bscore
    global wscore
    global yscore
    yscore=0
    bscore=0
    wscore=0
    if wscore==0:
        try:
            client=MongoClient(os.getenv("link"))
            mongodb=client.get_database("guess_the_word")
            mongocoll=mongodb.users
            implist=list(mongocoll.find({},{"name":1,"bestscore":1}).sort("bestscore",-1).limit(1))
            wscore=implist[0]["bestscore"]
            client.close()
        except Exception:
            messagebox.showerror("No internet","Please restart again!")
            root.after(3000,lambda: root.destroy())            
    my_font1 = Font(family="Bahnschrift", size=26,weight="bold",underline=1)
    my_font = Font(family="Bauhaus 93", size=28,weight="bold",underline=1)
    myfont = Font(family="Courier New CE", size=15)
    myfon = Font(family="Arial Black", size=18,weight="bold")
    def closerules():
        global rulesframe
        rulesframe.destroy()
        root.bind("<Key>",ruleskey)
    def submitt(event):
        global proceed
        if proceed==1:
            global ques
            global frame1
            global l1
            global yscore
            global bscore
            global wscore
            global bestscore
            global curscore
            global frame3
            global dispque
            global dispans
            global worldscore
            global total_words
            if proceed==1:
                userans=en.get()
                if userans==dispans:
                    yscore+=1
                    if ques==total_words:
                        ques=1
                    else:
                        ques+=1
                    try:
                        client=MongoClient(os.getenv("link"))
                        mongodb=client.get_database("guess_the_word")
                        mongocoll=mongodb.users
                    except Exception:
                        messagebox.showerror("No internet","Please restart again!")
                        root.after(3000,lambda: root.destroy())            
                    if yscore>bscore:
                        bscore=yscore
                        try:
                            mongocoll.update_one({"name":userid},{"$set":{"bestscore":bscore}})
                        except Exception:
                            messagebox.showerror("No internet","Please restart again!")
                            root.after(3000,lambda: root.destroy())
                    try:
                        mongocoll.update_one({"name":userid},{"$set":{"question":ques}})
                        client.close()
                    except Exception:
                        messagebox.showerror("No internet","Please restart again!")
                        root.after(3000,lambda: root.destroy())
                    
                    bestscore.place_forget()
                    curscore.place_forget()
                    
                    bestscore=Label(canvas,text="Best Score: "+str(bscore),bg="PaleTurquoise1",font="impact 16",fg="dark violet")
                    bestscore.place(relx=0.02,rely=0.02,relwidth=0.31,relheight=0.05)

                    curscore=Label(canvas,text="Your Score: "+str(yscore),bg="PaleTurquoise1",font="impact 16",fg="dark violet")
                    curscore.place(relx=0.67,rely=0.02,relwidth=0.31,relheight=0.05)
            
                    if yscore>wscore:
                        wow=Label(frame3,text="Champion!!",font="impact 28 bold",bg="cornflower blue",fg="green")
                        wow.place(relx=0.24,rely=0.6)
                        wow.after(3000,lambda: wow.destroy())
                        wscore=yscore
                        worldscore.place_forget()
                        worldscore=Label(canvas,text="WORLD'S\nBEST\nSCORE:\n"+str(wscore),bg="skyblue",font="verdana 14 bold",fg="snow")
                        worldscore.place(relx=0.01,rely=0.1,relwidth=0.2)

                    correct=Label(frame3,text="YAYY!!\nCORRECT!!!",font="impact 28 bold",bg="cornflower blue",fg="green")
                    correct.place(relx=0.24,rely=0.6)
                    correct.after(3000,lambda: correct.destroy())
                    l1.place_forget()
                    try:
                        client=MongoClient(os.getenv("link"))
                        mongodb=client.get_database("guess_the_word")
                        mongocoll=mongodb.pair_list
                        displist=list(mongocoll.find({"_id":ques},{"_id":0}))
                    except Exception:
                        messagebox.showerror("No internet","Please restart again!")
                        root.after(3000,lambda: root.destroy())
                    dispque=displist[0]["jumble"]
                    dispans=displist[0]["correct"]
                    client.close()
                    l1=Label(frame1,text=dispque,font="Courier 26 bold",bg="white",fg="red")
                    l1.place(relheight=1,relwidth=0.65)
                    en.delete(0,END)
                else:
                    wrong=Label(frame3,text="OOPS!!\nWRONG ANSWER!",font="impact 25 bold",bg="cornflower blue",fg="firebrick1")
                    wrong.place(relx=0.14,rely=0.55)
                    wrong.after(3000,lambda: wrong.destroy())
                            
              
    def nextt(event):
        global proceed
        global l1
        global ques
        global dispque
        global dispans
        global total_words
        if proceed==1:
            if ques==total_words:
                ques=1
            else:
                ques+=1
            try:
                client=MongoClient(os.getenv("link"))
                mongodb=client.get_database("guess_the_word")
                mongocoll=mongodb.users
                mongocoll.update_one({"name":userid},{"$set":{"question":ques}})
                mongocoll=mongodb.pair_list
                displist=list(mongocoll.find({"_id":ques},{"_id":0}))
                dispque=displist[0]["jumble"]
                dispans=displist[0]["correct"]
                client.close()
            except Exception:
                messagebox.showerror("No internet","Please restart again!")
                root.after(3000,lambda: root.destroy())
            l1.place_forget()
            l1=Label(frame1,text=dispque,font="Courier 26 bold",bg="white",fg="red")
            l1.place(relheight=1,relwidth=0.65)
    def ruleskey(event):
        global proceed
        if proceed==1 and event.char=="5":
            root.unbind("<Key>")
            global rulesframe
            rulesframe=Frame(canvas,bg="deep pink",bd=5)
            rulesframe.place(x=0,y=0,relheight=1,relwidth=1)
            
            rulesframe2=Frame(rulesframe,bg="pink")
            rulesframe2.place(relwidth=1,relheight=1)
            
            heading=Label(rulesframe2,text="HOW TO PLAY?",font=my_font,bg="pink",fg="snow")
            heading.place(relx=0.25)
            st="""Hi!
1)The Game is simple,Once You enter username your
game will start.
2)You are Given with a jumbled text you need to
type the correct word by rearranging them and
      submit the answer.                     
3)If you dont know the answer you can press NEXT
button to get the next Jumbled word.
4)For Every Correct Answer you will be awarded
with 1 point.
5)You can end the Game whenever You want to by
pressing End Game button
6)After pressing END GAME your score will be reset
to 0.
7)You can see top 10 High scorers by clicking the
view points table button
8)For Offline players best score will always reset
to 0 when the application is started!
9)Be in the top 10 so that anyone in the world
playing this can see your name on the table!
***Words may have multiple answer but only one
of them will be correct..keep trying for that
tough one***"""
            description=Label(rulesframe2,text=st,font=myfont,bg="pink")
            description.place(relx=0.01,rely=0.1)
            closebutton=Button(rulesframe2,text="Back",font=myfon,bg="red",fg="white",command=closerules)
            closebutton.place(relx=0.8)
            

    def rulesbutton():
        if(1==1):
            root.unbind("<Key>")
            global rulesframe
            rulesframe=Frame(canvas,bg="deep pink",bd=5)
            rulesframe.place(x=0,y=0,relheight=1,relwidth=1)
            
            rulesframe2=Frame(rulesframe,bg="pink")
            rulesframe2.place(relwidth=1,relheight=1)
            
            heading=Label(rulesframe2,text="HOW TO PLAY?",font=my_font,bg="pink",fg="snow")
            heading.place(relx=0.25)
            st="""Hi!
1)The Game is simple,Once You enter username your
game will start.
2)You are Given with a jumbled text you need to
type the correct word by rearranging them and
      submit the answer.                     
3)If you dont know the answer you can press NEXT
button to get the next Jumbled word.
4)For Every Correct Answer you will be awarded
with 1 point.
5)You can end the Game whenever You want to by
pressing End Game button
6)After pressing END GAME your score will be reset
to 0.
7)You can see top 10 High scorers by clicking the
view points table button
8)For Offline players best score will always reset
to 0 when the application is started!
9)Be in the top 10 so that anyone in the world
playing this can see your name on the table!
***Words may have multiple answer but only one
of them will be correct..keep trying for that
tough one***"""
            description=Label(rulesframe2,text=st,font=myfont,bg="pink")
            description.place(relx=0.01,rely=0.1)
            closebutton=Button(rulesframe2,text="Back",font=myfon,bg="red",fg="white",command=closerules)
            closebutton.place(relx=0.8)

    def endgamee():
        global yscore
        global curscore
        global worldscore
        yscore=0

        curscore.place_forget()
        curscore=Label(canvas,text="Your Score: 0000",bg="PaleTurquoise1",font="impact 16",fg="dark violet")
        curscore.place(relx=0.67,rely=0.02,relwidth=0.31,relheight=0.05)

        worldscore.place_forget()
        try:
            client=MongoClient(os.getenv("link"))
            mongodb=client.get_database("guess_the_word")
            mongocoll=mongodb.users
            implist=list(mongocoll.find({},{"name":1,"bestscore":1}).sort("bestscore",-1).limit(1))
            wscore=implist[0]["bestscore"]
            client.close()
        except Exception:
            messagebox.showerror("No internet","Please restart again!")
            root.after(3000,lambda: root.destroy())
        worldscore=Label(canvas,text="WORLD'S\nBEST\nSCORE:\n"+str(wscore),bg="skyblue",font="verdana 14 bold",fg="snow")
        worldscore.place(relx=0.01,rely=0.1,relwidth=0.2)

    def leaderboardd():
        global bscore
        try:
            client=MongoClient(os.getenv("link"))
            mongodb=client.get_database("guess_the_word")
            mongocoll=mongodb.users
            implist=list(mongocoll.find({},{"name":1,"bestscore":1,"_id":0}).sort("bestscore",-1))
            client.close()
        except Exception:
            messagebox.showerror("No internet","Please restart again!")
            root.after(3000,lambda: root.destroy())
        canvas1=Canvas(canvas,bg="medium purple")
        canvas1.place(relheight=1,relwidth=1)

        canvas1.create_polygon(0,0,100,0,0,100,fill="yellow")
        canvas1.create_polygon(600,600,500,600,600,500,fill="yellow")

        standings=Label(canvas1,text="STANDINGS",font=my_font1,fg="snow",bg="medium purple")
        standings.place(relx=0.6,rely=0.05)

        canvas1.create_polygon(80,115,130,115,120,145,70,145,fill="snow")
        hashlabel=Label(canvas1,text="#",font="Courier 14 bold",fg="medium purple",bg="snow")
        hashlabel.place(x=88,y=117)

        canvas1.create_polygon(133,115,400,115,390,145,123,145,fill="snow")
        namelabel=Label(canvas1,text="USERNAME",font="Courier 14 bold",fg="medium purple",bg="snow")
        namelabel.place(x=203,y=117)

        canvas1.create_polygon(403,115,570,115,560,145,393,145,fill="snow")
        scorelabel=Label(canvas1,text="SCORE",font="Courier 14 bold",fg="medium purple",bg="snow")
        scorelabel.place(x=448,y=117)

        j=32
        for i in range(1,11):
            canvas1.create_polygon(80,135+(j*i),130,135+(j*i),120,165+(j*i),70,165+(j*i),fill="hot pink")
            hashname=Label(canvas1,text=str(i),font="Courier 13 bold",fg="blue2",bg="hot pink")
            hashname.place(x=88,y=137+(j*i))
            
            canvas1.create_polygon(133,135+(j*i),400,135+(j*i),390,165+(j*i),123,165+(j*i),fill="cyan2")
            namename=Label(canvas1,text=implist[i-1]["name"],font="Courier 13 bold",fg="black",bg="cyan2")
            namename.place(x=203,y=137+(j*i))
            
            canvas1.create_polygon(403,135+(j*i),570,135+(j*i),560,165+(j*i),393,165+(j*i),fill="MistyRose2")
            scorename=Label(canvas1,text=implist[i-1]["bestscore"],font="Courier 13 bold",fg="red2",bg="MistyRose2")
            scorename.place(x=448,y=137+(j*i))
        r=1
        d={"name":userid,"bestscore":bscore}
        rank=(implist.index(d))+1

        yourrank=Label(canvas1,text="Your rank is: "+str(rank+1),bg="medium purple",fg="green2",font="impact 24")
        yourrank.place(x=205,y=500)

        exitthis=Button(canvas1,text="Go Back",bg="red2",fg="ghost white",font="times 14",relief=SUNKEN,command=lambda: canvas1.destroy())
        exitthis.place(x=270,y=550)
    
    def reveall():
        global yscore
        global curscore
        en.delete(0,END)
        if yscore<-19:
            sorry=Label(frame3,text="Sorry!\nYour score is too less",font="impact 20",bg="cornflower blue",fg="red")
            sorry.place(relx=0.14,rely=0.6)
            sorry.after(3000,lambda: sorry.destroy())
        else:
            yscore-=2
            curscore.place_forget()
            curscore=Label(canvas,text="Your Score: "+str(yscore),bg="PaleTurquoise1",font="impact 16",fg="dark violet")
            curscore.place(relx=0.67,rely=0.02,relwidth=0.31,relheight=0.05)
            en.insert(0,dispans)
    def startt(event):
        global startpage
        global proceed
        global Log
        global rec
        global ques
        global total_words
        try:
            client=MongoClient(os.getenv("link"))
            mongodb=client.get_database("guess_the_word")
            mongocoll=mongodb.users
        except Exception:
            messagebox.showerror("No internet","Please restart again!")
            root.after(3000,lambda: root.destroy())
        if proceed==0:
            global rec
            userlist=Log.get().strip().split(" ")
            try:
                rec=list(mongocoll.find({"name":userlist[0]},{"name":1,"_id":0}))
            except Exception:
                messagebox.showerror("No internet","Please restart again!")
                root.after(3000,lambda: root.destroy())
            if len(userlist)>1 or len(rec)>=1 or Log.get()=="":
                alreadytaken=Label(startpage,text="Username already taken",font="times 14",bg="black",fg="red")
                alreadytaken.place(relx=0.309,rely=0.47)
                Log.delete(0,END)
            else:
                global dispque
                global dispans
                proceed=1
                try:
                    cou=mongocoll.count_documents({})
                except Exception:
                    messagebox.showerror("No internet","Please restart again!")
                    root.after(3000,lambda: root.destroy())
                dat={"name":Log.get(),"bestscore":bscore,"worldrank":cou+1,"question":1}
                try:
                    mongocoll.insert_one(dat)
                except Exception:
                    messagebox.showerror("No internet","Please restart again!")
                    root.after(3000,lambda: root.destroy())
                ques=1
                try:
                    mongocoll=mongodb.pair_list
                    displist=list(mongocoll.find({"_id":ques},{"_id":0}))
                except Exception:
                    messagebox.showerror("No internet","Please restart again!")
                    root.after(3000,lambda: root.destroy())
                dispque=displist[0]["jumble"]
                dispans=displist[0]["correct"]
                try:
                    total_words=mongocoll.count_documents({})
                    client.close()
                except Exception:
                    messagebox.showerror("No internet","Please restart again!")
                    root.after(3000,lambda: root.destroy())
                global userid
                userid=Log.get()
                root.bind("<Return>",submitt)
                conn=sqlite3.connect(".img\\Guesstheword.db")
                name=Log.get()
                c=conn.cursor()
                c.execute("""UPDATE Player_Info SET
                          username = :un
                          WHERE oid = :num""",
                          {"un":name,
                           "num":1
                           }
                              )
                conn.commit()
                conn.close()
                startpage.place_forget()
                global l1
                l1=Label(frame1,text=dispque,font="Courier 26 bold",bg="white",fg="red")
                l1.place(relheight=1,relwidth=0.65)
    if proceed==1:
        try:
            client=MongoClient(os.getenv("link"))
            mongodb=client.get_database("guess_the_word")
            mongocoll=mongodb.users
            userobject=list(mongocoll.find({"name":userid}))
            bscore=userobject[0]["bestscore"]
            client.close()
        except Exception:
            messagebox.showerror("No internet","Please restart again!")
            root.after(3000,lambda: root.destroy())
    i1=ImageTk.PhotoImage(Image.open(".img\\GTW.jpg"))
    backg=Label(canvas,image=i1)
    backg.place(x=0,y=0)
                            
    bestscore=Label(canvas,text="Best Score: "+str(bscore),bg="PaleTurquoise1",font="impact 16",fg="dark violet")
    bestscore.place(relx=0.02,rely=0.02,relwidth=0.31,relheight=0.05)

    curscore=Label(canvas,text="Your Score: 0000",bg="PaleTurquoise1",font="impact 16",fg="dark violet")
    curscore.place(relx=0.67,rely=0.02,relwidth=0.31,relheight=0.05)

    worldscore=Label(canvas,text="WORLD'S\nBEST\nSCORE:\n"+str(wscore),bg="skyblue",font="verdana 14 bold",fg="snow")
    worldscore.place(relx=0.01,rely=0.1,relwidth=0.2)

    frame1=Frame(canvas,bg="cadet blue",bd=5)
    frame1.place(relx=0.23,rely=0.1,relwidth=0.6,relheight=0.1)
    if proceed==1:
        global l1
        l1=Label(frame1,text=dispque,font="Courier 26 bold",bg="white",fg="red")
        l1.place(relheight=1,relwidth=0.65)

    nex=Button(frame1,text="NEXT",bg="steelblue1",font="Helvetica 16 bold",fg="red3",command=lambda: nextt(1))
    nex.place(relx=0.67,relwidth=0.33,relheight=1)
    root.bind("<Right>",nextt)

    frame2=Frame(canvas,bg="cyan3")
    frame2.place(relx=0.23,rely=0.25,relwidth=0.6,relheight=0.05)

    l2=Label(frame2,text="Type Your Answer",font="verdana 16 bold",bg="cyan3",fg="maroon4")
    l2.place(relheight=1,relwidth=1)

    frame3=Frame(canvas,bg="cornflower blue",bd=5)
    frame3.place(relx=0.23,rely=0.32,relwidth=0.6,relheight=0.5)

    en=Entry(frame3,font="Helvetica 16")
    en.insert(0,"Type Here...")
    en.place(x=0,y=0,relwidth=1,relheight=0.3)

    submit=Button(frame3,text="Submit Answer",bg="wheat1",font="Helvetica 16 bold",fg="red3",command=lambda: submitt(1))
    submit.place(relx=0.5,rely=0.35)
    root.bind("<Return>",submitt)

    reveal=Button(frame3,text=" Reveal(-2) ",bg="wheat1",font="Helvetica 16 bold",fg="red3",command=reveall)
    reveal.place(rely=0.35)
    
    endgame=Button(canvas,bg="LightSkyBlue3",text="E N D   G A M E",font="impact 22",fg="red3",command=endgamee)
    endgame.place(relx=0.23,rely=0.85,relheight=0.1,relwidth=0.6)

    rules=Button(canvas,text="HOW \nTO \nPLAY\n?",bg="black",fg="white",font="verdana 12 bold",command=rulesbutton)
    rules.place(relx=0.85,rely=0.65,relheight=0.25,relwidth=0.14)
    root.bind("<Key>",ruleskey)

    keynote=Label(canvas,text="Press \n'5'\n for \nhelp",font="impact 16 ",fg="white",bg="gold")
    keynote.place(relx=0.85,rely=0.45,relwidth=0.135)

    leaderboard=Button(canvas,text="View\nPoints\nTable",bg="red",font="Times 18 bold",fg="yellow",command=leaderboardd)
    leaderboard.place(relx=0.01,rely=0.32,relwidth=0.2)
    
    if proceed==0:
        startpage=Frame(canvas)
        startpage.place(relheight=1,relwidth=1)
        frames=[PhotoImage(file=".img\\Login.gif",format = 'gif -index %i' %(i)) for i in range(100)]

        def update(ind):
            frame = frames[ind]
            ind += 1
            ind=ind%100
            label.configure(image=frame)
            startpage.after(100, update, ind)
        label = Label(startpage)
        label.pack()
        startpage.after(0, update, 0)

        descc=Label(startpage,text="This is one time Process \nif you have \nInternet Connection",fg="snow",font="verdana 16",bg="black")
        descc.place(relx=0.22,rely=0.2,relwidth=0.6)

        Log=Entry(startpage,fg="black",font="Courier 20 bold",bg="snow")
        Log.insert(0,"Username")
        Log.place(relx=0.3,rely=0.4,relwidth=0.4)

        startbut=Button(startpage,text="START",fg="white",bg="green",font="impact 14",command=lambda: startt(1))
        startbut.place(relx=0.3,rely=0.53,relwidth=0.4)
        root.bind("<Return>",startt)
        

    root.mainloop()
elif doc==1 and update==0:
    global ys
    global bs
    ys,bs=0,0
    root=Tk()
    root.title("Build The Word")
    root.iconbitmap(".img\\icon2.ico")
    root.configure(bg="black")
    global d
    d={1:['unbso','bonus'],2:['ulinsra','insular'],3:['ipsetox','exposit'],4:['tubr','brut'],5:['uipghtr','upright'],6:['iltsebr','bristle'],7:['inptedo','pointed'],8:['iznpceoa','caponize'],9:['lisetd','idlest'],10:['ulceda','cedula'],11:['inger','reign'],12:['ilmsedba','semibald'],
13:['lhtscka','klatsch'],14:['ilser','liers'],15:['pouc','coup'],16:['dbte','debt'],17:['ilngja','jingal'],18:['ypera','apery'],19:['lgseba','gables'],20:['lgedra','argled'],21:['liser','riels'],22:['tcera','caret'],23:['ulnedb','bundle'],24:['ojsa','soja'],
25:['ympghora','myograph'],26:['mseora','ramose'],27:['nwdoa','adown'],28:['uinpgsr','pursing'],29:['usctora','surcoat'],30:['linhwpge','whelping'],31:['vyilda','avidly'],32:['lgsca','clags'],33:['pseox','expos'],34:['yrac','racy'],35:['ylifhsda','ladyfish'],36:['lfseora','loafers'],
37:['utesdo','toused'],38:['uihgsobr','broguish'],39:['inptera','painter'],40:['ilnftora','flatiron'],41:['unsetdkr','drunkest'],42:['insedo','noised'],43:['ysetdr','dryest'],44:['npsora','aprons'],45:['phta','phat'],46:['ulipcs','piculs'],47:['rmac','marc'],48:['danl','land'],
49:['uinfgedz','defuzing'],50:['ingwsr','wrings'],51:['uinphcer','punchier'],52:['ilnpstok','slipknot'],53:['imgtesd','midgets'],54:['unmedkra','unmarked'],55:['ifskra','fakirs'],56:['vnmsea','mavens'],57:['lkhceba','bechalk'],58:['unsedor','sounder'],59:['uilpght','uplight'],60:['untera','nature'],
61:['gseda','degas'],62:['ipgseor','porgies'],63:['ulnscba','subclan'],64:['ntsdra','strand'],65:['vingsora','savoring'],66:['apcl','clap'],67:['inmped','impend'],68:['ulincesa','lunacies'],69:['ngtsa','angst'],70:['ultcer','cutler'],71:['uilngea','unagile'],72:['lhwea','whale'],
73:['imsek','mikes'],74:['untskr','trunks'],75:['isetcdok','diestock'],76:['yilhtera','earthily'],77:['uimpjer','jumpier'],78:['mhgeora','homager'],79:['htceor','troche'],80:['fkei','kief'],81:['dhut','thud'],82:['inftes','feints'],83:['lnmteoa','lomenta'],84:['aynz','zany'],
85:['ugstdra','dustrag'],86:['uobt','bout'],87:['amerz','mazer'],88:['uicer','ureic'],89:['ilngcs','clings'],90:['uintsck','unstick'],91:['inpgora','pignora'],92:['inpedo','opined'],93:['ultsobr','brulots'],94:['likctba','backlit'],95:['infceda','faciend'],96:['uyilqce','cliquey'],
97:['psecta','aspect'],98:['uilpco','upcoil'],99:['uilksetb','bulkiest'],100:['ylnwa','wanly'],101:['ugsdobr','dorbugs'],102:['hpstdoa','dashpot'],103:['viska','kivas'],104:['ucedba','abduce'],105:['phera','raphe'],106:['unftso','founts'],107:['yifpsec','specify'],108:['fcesra','facers'],
109:['ingto','tigon'],110:['nwedo','owned'],111:['ylsdo','sloyd'],112:['inedra','rained'],113:['yphser','sypher'],114:['medra','madre'],115:['uyqseka','squeaky'],116:['yiskr','risky'],117:['uilpcb','public'],118:['ylnmea','meanly'],119:['ingseoa','agonies'],120:['linftera','inflater'],
121:['ngebra','banger'],122:['lingteda','delating'],123:['ihtsedo','hoisted'],124:['vunhteor','overhunt'],125:['inpgtsra','partings'],126:['vitser','stiver'],127:['nteoa','oaten'],128:['lwteoba','teabowl'],129:['ulinfger','feruling'],130:['ulqtsoa','loquats'],131:['ugedb','debug'],132:['lhwteso','howlets'],
133:['ylfwsa','sawfly'],134:['mhsoba','abmhos'],135:['ilhebra','hirable'],136:['uynpedra','underpay'],137:['uilnco','uncoil'],138:['umpjs','jumps'],139:['vulseor','louvers'],140:['zsiy','sizy'],141:['mpedoa','pomade'],142:['poks','kops'],143:['inmgskra','markings'],144:['hgsa','gash'],
145:['imgted','midget'],146:['nsora','sonar'],147:['uyldbra','durably'],148:['lijst','jilts'],149:['ysetdor','destroy'],150:['ledora','ordeal'],151:['pghedra','graphed'],152:['uintesd','dunites'],153:['itsra','stair'],154:['ykta','kyat'],155:['ungceda','uncaged'],156:['aosl','sola'],
157:['ilmheoa','hemiola'],158:['uinmtoa','tinamou'],159:['uihsedr','hurdies'],160:['sobra','boras'],161:['lngsdora','goldarns'],162:['pous','opus'],163:['vlcea','calve'],164:['ipsetr','ripest'],165:['vlingsoa','salvoing'],166:['obsm','mobs'],167:['vinhseda','vanished'],168:['dnei','dine'],
169:['nmgteoa','megaton'],170:['phcesra','parches'],171:['vyceo','covey'],172:['nmhtesa','anthems'],173:['nwedra','warned'],174:['zsebra','zebras'],175:['gtri','trig'],176:['ulntseba','unstable'],177:['nmpgoka','kampong'],178:['ywdobr','byword'],179:['inmwsok','misknow'],180:['onym','mony'],
181:['uyhgtdra','draughty'],182:['ilnek','liken'],183:['uyledobr','bouldery'],184:['ilptsa','pastil'],185:['uinser','insure'],186:['psri','rips'],187:['vilnhge','helving'],188:['msekr','merks'],189:['uidoa','audio'],190:['linpgera','grapline'],191:['ulkctoba','blackout'],192:['hosm','mhos'],
193:['ptsor','strop'],194:['inphseda','pinheads'],195:['lincsra','carlins'],196:['ilhgted','lighted'],197:['wkea','weka'],198:['vlingca','calving'],199:['yinfga','faying'],200:['uinedr','ruined'],201:['yilngs','lysing'],202:['vulora','valour'],203:['lhsecokr','sherlock'],204:['iwteba','bawtie'],
205:['iltea','telia'],206:['vwsoa','avows'],207:['ifhts','shift'],208:['inmpte','pitmen'],209:['tour','rout'],210:['yingtora','gyration'],211:['imtecsdo','demotics'],212:['uitsrz','tzuris'],213:['znoa','azon'],214:['ifmto','motif'],215:['ylsoba','boylas'],216:['lmscea','mescal'],
217:['lmfeora','femoral'],218:['uinpedra','unpaired'],219:['ingcer','cering'],220:['uincsoz','zincous'],221:['onea','aeon'],222:['uifphst','upshift'],223:['inceso','conies'],224:['uhgsbr','burghs'],225:['lhcesora','choleras'],226:['uyiltsdr','sturdily'],227:['uisebr','buries'],228:['ulpcsoa','cupolas'],
229:['lhcesa','laches'],230:['uipcter','cuprite'],231:['ubel','lube'],232:['uinmtes','minutes'],233:['ilcedk','licked'],234:['ilntebz','blintze'],235:['nmeoba','bemoan'],236:['viedr','drive'],237:['ligcra','garlic'],238:['vywea','wavey'],239:['ulfhtsea','hasteful'],240:['uyhtdor','drouthy'],
241:['ulkgeba','bulkage'],242:['uylptco','octuply'],243:['ylpeb','blype'],244:['pwte','wept'],245:['ilnedbr','blinder'],246:['phsera','phrase'],247:['yusk','yuks'],248:['usel','lues'],249:['inmtsed','mistend'],250:['uiqltea','tequila'],251:['vinme','vimen'],252:['viwser','wivers'],
253:['ynher','henry'],254:['npeoa','paeon'],255:['npedkra','pranked'],256:['iltebra','librate'],257:['uimcekr','muckier'],258:['jcedka','jacked'],259:['insedok','doeskin'],260:['vilntera','interval'],261:['fedbra','barfed'],262:['ipscedr','crisped'],263:['dwka','dawk'],264:['isedz','sized'],
265:['lpgdoa','lapdog'],266:['linwedk','winkled'],267:['umbra','umbra'],268:['ylpstera','psaltery'],269:['ilngtcsa','catlings'],270:['ulphs','plush'],271:['uylper','purely'],272:['vunpsera','parvenus'],273:['imtcoa','atomic'],274:['inhgts','nights'],275:['uinmtse','mistune'],276:['yiljekr','jerkily'],
277:['ltcea','eclat'],278:['ltei','tile'],279:['ulntesba','abluents'],280:['lori','roil'],281:['inforx','fornix'],282:['jbsa','jabs'],283:['uylnpta','unaptly'],284:['ictsdo','dicots'],285:['unpset','upsent'],286:['cesox','coxes'],287:['imeda','amide'],288:['lkpctoba','blacktop'],
289:['usdor','duros'],290:['obsw','bows'],291:['uftcedoa','outfaced'],292:['uinfgcso','focusing'],293:['ingstera','ganister'],294:['hteso','ethos'],295:['ulpsc','sculp'],296:['vingeda','deaving'],297:['ncesdokr','dornecks'],298:['yilnmpgo','mopingly'],299:['vihcera','archive'],300:['viher','hiver'],
301:['ilngcer','clinger'],302:['uynta','aunty'],303:['inmceokr','monicker'],304:['unhgseor','roughens'],305:['umtsra','struma'],306:['umsedra','remudas'],307:['ulsekr','sulker'],308:['vfteora','overfat'],309:['lneda','naled'],310:['pugh','pugh'],311:['uliedbr','builder'],312:['uedbra','dauber'],
313:['istra','airts'],314:['unsedor','undoers'],315:['uyfptse','stupefy'],316:['yihwtes','whiteys'],317:['lifsa','alifs'],318:['inmtera','minaret'],319:['nphsect','pschent'],320:['npsedor','respond'],321:['yldor','lordy'],322:['lmhsedba','shambled'],323:['lnsedra','landers'],324:['mfedor','formed'],
325:['ilnpekr','plinker'],326:['aingcrz','crazing'],327:['dbri','drib'],328:['ulseb','lubes'],329:['ilhgtb','blight'],330:['inteska','intakes'],331:['ylmpeoa','maypole'],332:['dlei','diel'],333:['ucsedra','crusade'],334:['ulhcek','huckle'],335:['ljwedo','jowled'],336:['umpgsr','grumps'],
337:['ijsteora','jarosite'],338:['ilpcda','placid'],339:['lipseoka','soaplike'],340:['uigsd','guids'],341:['zfae','faze'],342:['ngsora','organs'],343:['wseob','bowse'],344:['fsekr','kerfs'],345:['ilzsedoa','diazoles'],346:['lnhpeo','holpen'],347:['yilfhsoa','oafishly'],348:['ylimsora','royalism'],
349:['obsk','bosk'],350:['lfsebra','fablers'],351:['dmle','meld'],352:['inmgcso','comings'],353:['ulmced','culmed'],354:['pora','proa'],355:['imhtra','thiram'],356:['ingsta','gainst'],357:['lingsba','ablings'],358:['ksetba','basket'],359:['unmhseda','unshamed'],360:['inpcets','incepts'],
361:['inedx','nixed'],362:['ingora','oaring'],363:['uingtsea','sauteing'],364:['lfgso','flogs'],365:['vnmea','maven'],366:['meobr','brome'],367:['ynix','nixy'],368:['ktis','kits'],369:['ipcetsk','pickets'],370:['lihteora','aerolith'],371:['ujdoka','judoka'],372:['ulmpsa','ampuls'],
373:['imwseobr','imbowers'],374:['unjctda','adjunct'],375:['lnwtedo','letdown'],376:['uscedobr','obscured'],377:['uintora','rainout'],378:['mpera','remap'],379:['psector','prosect'],380:['injteor','jointer'],381:['ilngcesr','cringles'],382:['nmeda','maned'],383:['nmpeora','manrope'],384:['ylkra','larky'],
385:['ynoi','yoni'],386:['npgsor','prongs'],387:['ncesda','dances'],388:['ingseob','biogens'],389:['ilfsra','flairs'],390:['pgtesora','portages'],391:['vinsea','savine'],392:['tecsra','traces'],393:['dbre','bred'],394:['unmtsor','nostrum'],395:['inwgkra','warking'],396:['ugscedor','scrouged'],
397:['ynsedob','beyonds'],398:['inmpgo','moping'],399:['ntseor','nestor'],400:['vuincsa','vicunas'],401:['ltsob','bolts'],402:['infgera','fearing'],403:['tpra','prat'],404:['iftebra','barefit'],405:['trfe','fret'],406:['ytsra','satyr'],407:['ilhca','laich'],408:['ulptedra','preadult'],
409:['ywcka','wacky'],410:['unpwteor','uptowner'],411:['lifmora','aliform'],412:['uhceobra','barouche'],413:['yilpsoa','soapily'],414:['medkra','demark'],415:['uylhsco','slouchy'],416:['yihsdbr','hybrids'],417:['vimto','vomit'],418:['ubhskra','kurbash'],419:['inptsdoa','satinpod'],420:['ilnpces','pencils'],
421:['uiqpcets','picquets'],422:['inphgcra','parching'],423:['ylihsdoa','hyaloids'],424:['yilnger','relying'],425:['nsedor','drones'],426:['itsed','sited'],427:['yhsdor','hydros'],428:['ipser','peris'],429:['uliseor','soilure'],430:['vygseoa','voyages'],431:['inhgtec','etching'],432:['ihwted','whited'],
433:['gobn','bong'],434:['ulscedk','suckled'],435:['wcsdora','cowards'],436:['ylwedo','yowled'],437:['iyra','airy'],438:['izera','zaire'],439:['yneokr','yonker'],440:['intes','tines'],441:['ugtsoa','outgas'],442:['uingedr','dungier'],443:['npsedora','padrones'],444:['imwedoa','miaowed'],
445:['unfsedor','refounds'],446:['liwse','wiles'],447:['yliper','ripely'],448:['ftsedra','strafed'],449:['uilnpe','lineup'],450:['ulfhser','flusher'],451:['ulnsedbr','bundlers'],452:['yiftedox','detoxify'],453:['uylqtsa','squatly'],454:['nphcesoa','panoches'],455:['linfmera','inflamer'],456:['imsbr','brims'],
457:['yncsora','crayons'],458:['yinsrx','syrinx'],459:['valisz','vizsla'],460:['hbre','herb'],461:['iuel','lieu'],462:['ijedb','jibed'],463:['phtesra','tephras'],464:['ngsedoba','bondages'],465:['vylmoba','movably'],466:['ulced','clued'],467:['impcsr','crimps'],468:['uingdo','guidon'],
469:['lngwsea','wangles'],470:['ihcedok','hoicked'],471:['ilmed','limed'],472:['pwra','warp'],473:['inmedo','domine'],474:['pseok','spoke'],475:['voni','vino'],476:['ilnpteoa','antipole'],477:['ilnhgera','nargileh'],478:['mhedobra','rhabdome'],479:['lnsedor','rondels'],480:['hcetsr','cherts'],
481:['ionl','lino'],482:['nmhtea','anthem'],483:['tgus','gust'],484:['btea','beat'],485:['uilngts','lutings'],486:['ilhster','slither'],487:['uwtsora','outwars'],488:['umhgseo','gumshoe'],489:['ylmstra','smartly'],490:['sedra','rased'],491:['mtedobra','bromated'],492:['ihgte','eight'],
493:['ifmcesto','comfiest'],494:['mgseba','gambes'],495:['icdbra','bardic'],496:['wsobr','brows'],497:['lipteda','taliped'],498:['uinfgtr','turfing'],499:['nptsdoa','dopants'],500:['ilsdo','lidos'],501:['uypedr','dupery'],502:['dnmi','mind'],503:['imstedo','modiste'],504:['inkgebra','breaking'],
505:['lhcesor','cholers'],506:['vltesa','valets'],507:['ulnsk','lunks'],508:['intcedo','ctenoid'],509:['iwcetk','wicket'],510:['msetdo','modest'],511:['iptsdor','torpids'],512:['ilntesra','entrails'],513:['uiqmsra','marquis'],514:['dore','redo'],515:['ymhtes','thymes'],516:['pgsera','gasper'],
517:['ilnpsa','lapins'],518:['infsecor','forensic'],519:['ynwsea','sawney'],520:['yjseo','joeys'],521:['ilhtecdr','eldritch'],522:['ltsea','stela'],523:['inmhpcoa','champion'],524:['npgobra','probang'],525:['uynmfter','frumenty'],526:['ascl','lacs'],527:['ingdo','doing'],528:['lsdra','lards'],
529:['ynheo','honey'],530:['umged','degum'],531:['tcesa','cesta'],532:['gkow','gowk'],533:['ynwso','snowy'],534:['unctsora','courants'],535:['vyliba','viably'],536:['nfeorz','frozen'],537:['uhser','usher'],538:['umpwsra','warmups'],539:['lmfi','film'],540:['vyingera','vinegary'],
541:['yksetbra','basketry'],542:['impgsera','primages'],543:['vira','vair'],544:['uipsedr','updries'],545:['nkte','kent'],546:['lngea','angel'],547:['vilgedor','overgild'],548:['inmweora','airwomen'],549:['linwgka','walking'],550:['yinpcka','panicky'],551:['ynmseobr','embryons'],552:['lipteso','piolets'],
553:['unjsekr','junkers'],554:['nwsera','resawn'],555:['ulngwoba','bungalow'],556:['ntesor','noters'],557:['ulpbra','burlap'],558:['inhwgse','shewing'],559:['uilnfpgs','upflings'],560:['ltcseor','costrel'],561:['unptea','peanut'],562:['vilnsea','valines'],563:['mtedob','tombed'],564:['yilpwka','pawkily'],
565:['ynsi','yins'],566:['ljsto','jolts'],567:['uylnsdo','soundly'],568:['uilnsdra','diurnals'],569:['injsex','jinxes'],570:['inmhsedo','hedonism'],571:['ybsa','abys'],572:['uifjs','fujis'],573:['ukteoba','outbake'],574:['uqcetor','croquet'],575:['yinpck','pyknic'],576:['ilfse','flies'],
577:['ulneda','unlade'],578:['ntak','tank'],579:['uimsera','uremias'],580:['vyre','very'],581:['ilzsdra','lizards'],582:['yhcteoa','chayote'],583:['ntsora','tronas'],584:['itskra','traiks'],585:['lgsetra','largest'],586:['bsei','bise'],587:['insba','basin'],588:['duso','duos'],
589:['ifgted','gifted'],590:['tesorx','oxters'],591:['upjteka','kajeput'],592:['lhwor','whorl'],593:['indora','inroad'],594:['nokra','krona'],595:['vuilsbra','subviral'],596:['ukpebra','breakup'],597:['psedra','spread'],598:['ynmhsa','mynahs'],599:['mseba','bemas'],600:['ingsed','singed'],
601:['hsci','chis'],602:['mpsceora','mesocarp'],603:['phcera','eparch'],604:['uinjgdra','adjuring'],605:['nwseoa','weason'],606:['infcera','fancier'],607:['ulnfgwor','wrongful'],608:['uinmco','muonic'],609:['ibhcskra','brackish'],610:['ilnfedr','flinder'],611:['yptso','potsy'],612:['mgtsoa','magots'],
613:['uylstobr','robustly'],614:['infpsera','firepans'],615:['ilngsea','leasing'],616:['lwsera','walers'],617:['kcedobr','bedrock'],618:['yimcek','mickey'],619:['ymgeoax','exogamy'],620:['vgtoa','gavot'],621:['libhska','kiblahs'],622:['igteor','goiter'],623:['ilnmsobr','nombrils'],624:['vmsedoa','vamosed'],
625:['inhcra','inarch'],626:['lmsea','almes'],627:['uimtedbr','imbruted'],628:['ingtcso','costing'],629:['uimsetdr','diestrum'],630:['iphtsceo','postiche'],631:['uiqnta','quaint'],632:['mpsta','tamps'],633:['imhcsra','chimars'],634:['vinhgera','havering'],635:['yilftesr','flytiers'],636:['uinmgts','musting'],
637:['unwsdra','sunward'],638:['ilngera','nargile'],639:['ingsed','signed'],640:['seobrax','boraxes'],641:['inmfgtes','figments'],642:['dgri','grid'],643:['vinceobx','biconvex'],644:['inhtcesk','thickens'],645:['intsoka','kations'],646:['ulmda','almud'],647:['hteso','those'],648:['vlneo','novel'],
649:['lifka','kalif'],650:['yolw','yowl'],651:['ysex','sexy'],652:['uihwtso','outwish'],653:['uinpcdk','duckpin'],654:['ulmtesbr','tumblers'],655:['lnmsoa','salmon'],656:['linhcor','chlorin'],657:['ilfhgt','flight'],658:['ylebra','bleary'],659:['lihse','shiel'],660:['linmpora','prolamin'],
661:['lfhpseto','fleshpot'],662:['hwedokra','headwork'],663:['vlweokra','walkover'],664:['uinhgcdo','douching'],665:['unmhera','humaner'],666:['utebra','arbute'],667:['linfseob','lobefins'],668:['intesra','retsina'],669:['ulfeda','feudal'],670:['lpsca','scalp'],671:['uinmsd','nudism'],672:['vuiltora','outrival'],
673:['htcesob','botches'],674:['imtedr','mitred'],675:['uilnhgsr','hurlings'],676:['hwseor','reshow'],677:['inedoax','dioxane'],678:['ilnhgto','tholing'],679:['isedra','irades'],680:['iftser','strife'],681:['ulfgseb','begulfs'],682:['yphcoa','poachy'],683:['tfre','reft'],684:['iedbra','abider'],
685:['lihtea','halite'],686:['lpcea','place'],687:['pyti','pity'],688:['inmteoa','amniote'],689:['ilmtesba','bimetals'],690:['yhtra','rhyta'],691:['icesra','caries'],692:['lingter','tingler'],693:['ilgea','agile'],694:['nmgteoa','montage'],695:['htebra','bertha'],696:['inftskra','ratfinks'],
697:['umskr','murks'],698:['gore','ogre'],699:['pgtedora','portaged'],700:['uintes','tenuis'],701:['inwgco','cowing'],702:['vlieda','vialed'],703:['augez','gauze'],704:['yihtsera','hysteria'],705:['ulhsco','slouch'],706:['igsor','giros'],707:['lctoba','cobalt'],708:['uhpcba','hubcap'],
709:['vilne','levin'],710:['ibsl','libs'],711:['itceso','cestoi'],712:['vlmseora','removals'],713:['ptesdora','adopters'],714:['srma','arms'],715:['uhgtsa','aughts'],716:['unksob','bunkos'],717:['pnko','knop'],718:['ugsbr','burgs'],719:['imkbra','imbark'],720:['ihgedba','bighead'],
721:['guml','glum'],722:['inmpsora','rampions'],723:['inhwte','whiten'],724:['ltcseoa','lactose'],725:['ulmtso','moults'],726:['lieokra','oarlike'],727:['iwtesr','writes'],728:['vinse','vines'],729:['ilngcsa','lacings'],730:['pubr','burp'],731:['ulnsda','suldan'],732:['ilmsetdo','moldiest'],
733:['ilsra','rails'],734:['ulpcedoa','cupolaed'],735:['iwtesba','bawties'],736:['ulmsebr','rumbles'],737:['thos','host'],738:['ihsed','shied'],739:['ylmwba','wambly'],740:['usfl','flus'],741:['isdbr','birds'],742:['unhpsra','unsharp'],743:['dgsa','gads'],744:['ulinmpgr','rumpling'],
745:['ungtsoa','outsang'],746:['ungtoba','gunboat'],747:['nmix','minx'],748:['wnto','wont'],749:['upgsr','sprug'],750:['uimsc','music'],751:['ipscdora','sporadic'],752:['ilgsobra','garboils'],753:['ylhpsra','sharply'],754:['lkcestba','blackest'],755:['ipsl','slip'],756:['ipser','spire'],
757:['cetsdora','redcoats'],758:['yptebra','typebar'],759:['nweor','owner'],760:['ilmper','limper'],761:['ulimsa','miauls'],762:['wtser','strew'],763:['poke','poke'],764:['hosw','hows'],765:['ncedokr','dorneck'],766:['ilnmedba','mandible'],767:['doyz','dozy'],768:['ntex','next'],
769:['yipws','wispy'],770:['vultera','vaulter'],771:['mhedra','harmed'],772:['ilngjsa','jingals'],773:['isebrax','braxies'],774:['osra','sora'],775:['nsteora','treason'],776:['mjsora','jorams'],777:['lmpseda','psalmed'],778:['ulscea','clause'],779:['uqtesor','torques'],780:['gnaw','gnaw'],
781:['ulmpcedr','crumpled'],782:['fwera','wafer'],783:['yimts','misty'],784:['nsedra','redans'],785:['ngjsora','jargons'],786:['uimcsb','cubism'],787:['meobr','ombre'],788:['ynse','syne'],789:['upsera','pauser'],790:['ulnfsekr','flunkers'],791:['vltera','varlet'],792:['uimtsda','stadium'],
793:['inhedor','hordein'],794:['yptceso','cotypes'],795:['jtoa','jato'],796:['vmsetoz','zemstvo'],797:['cesdkr','drecks'],798:['hsebra','basher'],799:['ilmtecra','metrical'],800:['stic','tics'],801:['mjteso','jetsom'],802:['ylnmora','almonry'],803:['inwda','diwan'],804:['ulseo','louse'],
805:['uimterx','mixture'],806:['fmhtoa','fathom'],807:['vaki','kiva'],808:['yilsedba','biasedly'],809:['uhgcoa','gaucho'],810:['mhcsoa','machos'],811:['ulmfsra','fulmars'],812:['lmpsa','plasm'],813:['yingedra','readying'],814:['mtsdora','tsardom'],815:['lingtsea','stealing'],816:['ntesd','dents'],
817:['ulpscted','sculpted'],818:['utsor','tours'],819:['limebra','balmier'],820:['gsma','gams'],821:['infpera','firepan'],822:['vised','vised'],823:['hcesok','chokes'],824:['nseob','ebons'],825:['yimgera','imagery'],826:['ylmseobr','sombrely'],827:['hwsdoa','shadow'],828:['inmhtea','hematin'],
829:['lfie','file'],830:['uypso','soupy'],831:['gsceoa','socage'],832:['htorax','thorax'],833:['lmhsoa','shalom'],834:['vuliged','divulge'],835:['yliteokr','kryolite'],836:['vlsea','laves'],837:['inftcsoa','factions'],838:['lhtesbra','halberts'],839:['ocfi','fico'],840:['liptesda','talipeds'],
841:['lhtcedra','trachled'],842:['inmedbr','birdmen'],843:['ilfteoba','lifeboat'],844:['uyltsebr','blustery'],845:['inhtsced','snitched'],846:['ulmco','locum'],847:['dsfe','feds'],848:['vyipr','privy'],849:['viptedo','pivoted'],850:['inwse','wines'],851:['tcedokr','trocked'],852:['lwsob','bowls'],
853:['ntceso','centos'],854:['imtsed','misted'],855:['ntedor','rodent'],856:['inweobr','brownie'],857:['pseobr','probes'],858:['imdoa','amido'],859:['inpgser','springe'],860:['mseobr','ombers'],861:['intscera','scantier'],862:['nphtera','panther'],863:['lmsobra','bromals'],864:['izsra','izars'],
865:['lntcera','central'],866:['ikra','raki'],867:['dgye','edgy'],868:['lerax','laxer'],869:['ymsba','abysm'],870:['ilpst','split'],871:['ntea','etna'],872:['uisctera','suricate'],873:['urma','arum'],874:['uilfz','fuzil'],875:['inwgekra','rewaking'],876:['uingtsk','tusking'],
877:['vyifser','versify'],878:['igsedr','ridges'],879:['ngwedoa','wagoned'],880:['hceora','chorea'],881:['yhtsa','hasty'],882:['yuro','your'],883:['linseoax','siloxane'],884:['ptsora','pastor'],885:['lncesdra','candlers'],886:['msedra','dermas'],887:['unmcea','acumen'],888:['lnpgera','grapnel'],
889:['upghtera','upgather'],890:['infceor','coinfer'],891:['unhgser','hungers'],892:['lpsdo','plods'],893:['nptedor','protend'],894:['ihskr','shirk'],895:['ulngeo','lounge'],896:['lpsera','lapser'],897:['ilptcoa','optical'],898:['injgcka','jacking'],899:['nftdoa','fantod'],900:['pore','rope'],
901:['lingtska','talkings'],902:['ulnse','lunes'],903:['mhsceda','chasmed'],904:['ucsedora','caroused'],905:['ngcoa','conga'],906:['lingseka','snaglike'],907:['yipst','tipsy'],908:['lwdoa','woald'],909:['itcor','toric'],910:['unpgedoa','poundage'],911:['ykebra','bakery'],912:['inhgceba','beaching'],
913:['lipobra','bipolar'],914:['mhcedra','charmed'],915:['lited','tilde'],916:['yinpcsk','pyknics'],917:['uiqmsr','squirm'],918:['onme','nome'],919:['ptsera','paster'],920:['lnhcdora','chlordan'],921:['inmteax','taximen'],922:['ilnpcea','panicle'],923:['ulphser','plusher'],924:['drei','dire'],
925:['utesdor','redouts'],926:['phce','pech'],927:['yinpgt','typing'],928:['vlfedora','flavored'],929:['lipseor','spoiler'],930:['yinpgse','pigsney'],931:['hteor','other'],932:['mhwsa','whams'],933:['yilnwgob','bowingly'],934:['ulnpged','plunged'],935:['vgus','vugs'],936:['ilmwseoa','wailsome'],
937:['uinjsek','junkies'],938:['uliska','saluki'],939:['uledobra','laboured'],940:['ulifcor','fluoric'],941:['lhtceso','clothes'],942:['inwced','winced'],943:['ulfcera','careful'],944:['inmgseta','mangiest'],945:['ylpora','pyrola'],946:['lidbra','ribald'],947:['inhteora','antihero'],948:['tokra','troak'],
949:['ymhce','chyme'],950:['umhor','mohur'],951:['lfedba','fabled'],952:['vincetra','navicert'],953:['umkgceba','megabuck'],954:['uynhtedr','thundery'],955:['ilnsdora','ordinals'],956:['ungsedr','nudgers'],957:['inpser','repins'],958:['igedr','gride'],959:['ylctesoa','acolytes'],960:['upcdobra','cupboard'],
961:['inmeora','romaine'],962:['uifmtobr','tubiform'],963:['vlted','veldt'],964:['inmtsa','matins'],965:['psedor','dopers'],966:['mjtesa','jetsam'],967:['lpeora','parole'],968:['uinfgdo','fungoid'],969:['imptoa','optima'],970:['lebra','baler'],971:['uyimftr','furmity'],972:['uyinhcso','cushiony'],
973:['uysdra','sudary'],974:['lpeobra','ropable'],975:['ilngeo','legion'],976:['psti','tips'],977:['mptsa','stamp'],978:['ifedr','fried'],979:['yultsoa','layouts'],980:['uiqlpsa','pasquil'],981:['uinmtedr','unmitred'],982:['hsfi','fish'],983:['vinmgsea','veganism'],984:['groy','gory'],
985:['nhgtedo','thonged'],986:['ulqimhsa','qualmish'],987:['yilmseor','rimosely'],988:['inhwgta','thawing'],989:['uliter','rutile'],990:['yilpwsa','slipway'],991:['imgstera','magister'],992:['yilmtsca','mystical'],993:['uimptor','protium'],994:['uyhwtsra','thruways'],995:['ungter','urgent'],996:['linmstea','smaltine'],
997:['sedobr','sorbed'],998:['ilhsce','chisel'],999:['infcdora','fricando'],1000:['ltesb','belts'],1001:['inmgedo','mendigo'],1002:['inptecda','pedantic'],1003:['ilngtea','atingle'],1004:['ulncdora','crunodal'],1005:['mhtedo','method'],1006:['thur','hurt'],1007:['ulgtso','glouts'],1008:['dgun','dung'],
1009:['lhscor','schorl'],1010:['nptesa','patens'],1011:['lifed','field'],1012:['imtsdoa','mastoid'],1013:['ilmgtsa','stigmal'],1014:['uyiteb','ubiety'],1015:['ingtso','stingo'],1016:['uleob','boule'],1017:['ntsera','astern'],1018:['inpedkr','prinked'],1019:['licob','cibol'],1020:['pwso','swop'],
1021:['inhpceso','chopines'],1022:['steax','taxes'],1023:['yincsda','cyanids'],1024:['yimkr','mirky'],1025:['vlseoba','absolve'],1026:['ingtcoa','coating'],1027:['ngsob','bongs'],1028:['yilngtka','takingly'],1029:['wcms','cwms'],1030:['ltcera','cartel'],1031:['umtcseor','costumer'],1032:['litedo','toiled'],
1033:['ulimha','hamuli'],1034:['umpcsr','crumps'],1035:['uingsca','saucing'],1036:['ilsed','slide'],1037:['uphwtor','upthrow'],1038:['nbte','bent'],1039:['imtse','stime'],1040:['lgtesora','legators'],1041:['ulftesor','flouters'],1042:['ylnseobz','benzoyls'],1043:['ilweba','bewail'],1044:['itcskr','tricks'],
1045:['uiqsedra','queridas'],1046:['vuilne','unveil'],1047:['nbti','bint'],1048:['yligor','gorily'],1049:['yhdra','hardy'],1050:['mpseo','pomes'],1051:['ilnwsekr','wrinkles'],1052:['uyimftor','fumitory'],1053:['ylitsdo','styloid'],1054:['uyhtcebr','butchery'],1055:['uilnpr','purlin'],1056:['nmtsea','stamen'],
1057:['vitca','vatic'],1058:['lhteo','hotel'],1059:['uintcs','cutins'],1060:['ylera','leary'],1061:['yilnhtso','tonishly'],1062:['aitcoz','azotic'],1063:['ulfwcekr','wreckful'],1064:['iphtecra','phreatic'],1065:['tsec','sect'],1066:['hgsta','ghats'],1067:['litsdora','dilators'],1068:['cobrax','boxcar'],
1069:['unfsra','furans'],1070:['lmseor','morsel'],1071:['gcedra','cadger'],1072:['nmtsora','matrons'],1073:['inmgsedo','mendigos'],1074:['inptsed','stipend'],1075:['lngda','gland'],1076:['ungwtoa','outgnaw'],1077:['nkedba','banked'],1078:['pcetra','preact'],1079:['inwer','rewin'],1080:['ulpcesba','bluecaps'],
1081:['ilmhseb','blemish'],1082:['lnfmpora','planform'],1083:['itskr','stirk'],1084:['ilnhebra','hibernal'],1085:['ylifwe','wifely'],1086:['ipstra','rapist'],1087:['uinpsz','unzips'],1088:['yhtces','chesty'],1089:['yiwseo','yowies'],1090:['yiltdora','adroitly'],1091:['ulfso','fouls'],1092:['ilsedr','slider'],
1093:['uqcetso','coquets'],1094:['limteoka','moatlike'],1095:['ibmoka','akimbo'],1096:['umhsbra','rhumbas'],1097:['ubta','tabu'],1098:['insbra','brains'],1099:['nhtcesra','chanters'],1100:['yinwtes','witneys'],1101:['dksi','skid'],1102:['ysel','leys'],1103:['imsra','simar'],1104:['ilntesd','dentils'],
1105:['ipska','paiks'],1106:['ilngseo','eloigns'],1107:['ytsor','ryots'],1108:['tscoa','ascot'],1109:['uyilnhgr','hungrily'],1110:['uisecbr','suberic'],1111:['fgtesor','forgets'],1112:['ilhgwsor','showgirl'],1113:['fsdra','fards'],1114:['aulnhtez','hazelnut'],1115:['nsdora','adorns'],1116:['vteobr','obvert'],
1117:['otrw','trow'],1118:['lmhse','helms'],1119:['ilgsed','glides'],1120:['wtseob','bestow'],1121:['ilcedra','radicle'],1122:['izphtea','zaptieh'],1123:['eobrx','boxer'],1124:['mhea','haem'],1125:['hceokr','hocker'],1126:['uinhgsa','anguish'],1127:['ylisedra','dialyser'],1128:['mpsek','kemps'],
1129:['unmedra','maunder'],1130:['liwseobr','blowsier'],1131:['gsdra','grads'],1132:['ahsl','lash'],1133:['htcra','ratch'],1134:['nmgera','german'],1135:['umpjed','jumped'],1136:['uilnmsoa','laminous'],1137:['nsedoz','dozens'],1138:['ulcesor','colures'],1139:['yintokra','karyotin'],1140:['unmgs','mungs'],
1141:['nsak','sank'],1142:['uingtsb','tubings'],1143:['ulfper','purfle'],1144:['utedbr','bruted'],1145:['fwsor','frows'],1146:['unsed','nudes'],1147:['ilmgba','gimbal'],1148:['unhtcsa','canthus'],1149:['ulngsebr','blungers'],1150:['yfsra','frays'],1151:['umhsca','sumach'],1152:['lnpska','planks'],
1153:['ulncea','unlace'],1154:['lbda','bald'],1155:['wtsor','worst'],1156:['lhcesoa','loaches'],1157:['insco','sonic'],1158:['inwta','twain'],1159:['ilfhwsob','fishbowl'],1160:['npgedra','pranged'],1161:['ncsobra','carbons'],1162:['uqntceoa','cotquean'],1163:['gsel','gels'],1164:['ilsdra','lidars'],
1165:['ilfser','lifers'],1166:['ncik','nick'],1167:['inmhea','haemin'],1168:['vseor','roves'],1169:['uiphra','rupiah'],1170:['unfeorz','unfroze'],1171:['uicsor','curios'],1172:['dmae','made'],1173:['uinctdor','inductor'],1174:['ulpedo','louped'],1175:['phcor','porch'],1176:['lgseo','ogles'],
1177:['hteorx','exhort'],1178:['fcera','farce'],1179:['uibkr','krubi'],1180:['ulngser','lungers'],1181:['ylipsdra','pyralids'],1182:['linmgsra','marlings'],1183:['yilngs','lyings'],1184:['uligseto','eulogist'],1185:['tcedo','coted'],1186:['uiqcsor','croquis'],1187:['aysl','lays'],1188:['vinhter','thriven'],
1189:['uilnmgc','culming'],1190:['uilnmpta','platinum'],1191:['lseca','scale'],1192:['ngtsa','tangs'],1193:['lingebra','blearing'],1194:['uilceob','ciboule'],1195:['yisekr','kyries'],1196:['unmptoa','pantoum'],1197:['ainhtsoz','hoatzins'],1198:['thsi','sith'],1199:['unfgo','fungo'],1200:['nfmtoa','fantom'],
1201:['ulnpdora','pauldron'],1202:['ingstoka','goatskin'],1203:['ynmsedor','syndrome'],1204:['uliftsor','floruits'],1205:['lcekra','lacker'],1206:['ingtsea','easting'],1207:['uifger','figure'],1208:['umedr','demur'],1209:['iphcer','ceriph'],1210:['nseka','kanes'],1211:['lnsoa','solan'],1212:['dwei','wide'],
1213:['ingwsa','wigans'],1214:['pose','epos'],1215:['lngcsa','clangs'],1216:['lcora','claro'],1217:['linpseo','pinoles'],1218:['npsed','spend'],1219:['dgow','gowd'],1220:['umsedo','moused'],1221:['inskr','rinks'],1222:['nmteax','taxmen'],1223:['inwgdor','wording'],1224:['inpsor','orpins'],
1225:['lfsekra','flakers'],1226:['imfcor','formic'],1227:['linceoba','bioclean'],1228:['mhcoa','macho'],1229:['isera','raise'],1230:['uijcer','juicer'],1231:['mtsra','marts'],1232:['liebr','birle'],1233:['vcesor','corves'],1234:['iphstora','aphorist'],1235:['uytsb','busty'],1236:['ulfmwsea','wamefuls'],
1237:['ujtser','juster'],1238:['incetsra','ceratins'],1239:['vlhsea','halves'],1240:['ingsbra','sabring'],1241:['lingtes','tingles'],1242:['utesdb','debuts'],1243:['linwek','winkle'],1244:['ucetd','educt'],1245:['litceskr','ticklers'],1246:['msedo','demos'],1247:['uilwtedo','outwiled'],1248:['hceska','haceks'],
1249:['inkgcba','backing'],1250:['dyno','yond'],1251:['unhcbr','brunch'],1252:['uinjgka','jauking'],1253:['mtri','trim'],1254:['vylictoa','vocality'],1255:['zmtsdora','tzardoms'],1256:['unted','tuned'],1257:['hcora','orach'],1258:['ifkedobr','biforked'],1259:['uiftedr','fruited'],1260:['ulmtesor','moulters'],
1261:['uqteo','toque'],1262:['hwsea','hawse'],1263:['uingdr','during'],1264:['ilcera','lacier'],1265:['umpwra','warmup'],1266:['indoa','danio'],1267:['ulmpseoa','ampoules'],1268:['uileda','audile'],1269:['ltri','tirl'],1270:['ustda','adust'],1271:['yilngtoa','antilogy'],1272:['tpos','spot'],
1273:['inwgte','tewing'],1274:['nedkra','danker'],1275:['igma','magi'],1276:['vilftsea','festival'],1277:['lwsdo','wolds'],1278:['ihgcora','choragi'],1279:['uingsdo','guidons'],1280:['utesbr','burets'],1281:['ptcesa','epacts'],1282:['hjseda','hadjes'],1283:['infsora','insofar'],1284:['ilwse','lewis'],
1285:['uilorax','uxorial'],1286:['lmae','male'],1287:['lnmsedo','dolmens'],1288:['uilnfga','gainful'],1289:['unmpea','pneuma'],1290:['visedora','avodires'],1291:['ulpghso','ploughs'],1292:['ingsedoa','diagnose'],1293:['yinjgo','joying'],1294:['uyliqfa','qualify'],1295:['uilhseb','blueish'],1296:['uimfcra','fumaric'],
1297:['mhgsoa','oghams'],1298:['impor','primo'],1299:['ilngtobr','ringbolt'],1300:['lsedba','blades'],1301:['lseda','lades'],1302:['duse','dues'],1303:['unpekr','punker'],1304:['iftsed','fisted'],1305:['iptsra','tapirs'],1306:['unsdoba','abounds'],1307:['lstoa','lotas'],1308:['untsa','aunts'],
1309:['imerx','mirex'],1310:['linba','binal'],1311:['vingedor','ringdove'],1312:['uilngeb','blueing'],1313:['ulncesa','lacunes'],1314:['pseobr','rebops'],1315:['imphsor','rompish'],1316:['yilnta','litany'],1317:['itedoax','oxidate'],1318:['lmheora','armhole'],1319:['iltesr','liters'],1320:['ylmceo','comely'],
1321:['ngsera','sanger'],1322:['viceso','voices'],1323:['uedor','uredo'],1324:['ulcska','caulks'],1325:['ymseo','mosey'],1326:['insedr','diners'],1327:['ulngjse','jungles'],1328:['imhpsr','shrimp'],1329:['ptedo','depot'],1330:['ugteo','togue'],1331:['ynhseok','honkeys'],1332:['kric','rick'],
1333:['lmsoa','molas'],1334:['iphsez','phizes'],1335:['uimces','cesium'],1336:['uiqsa','quais'],1337:['ipgsr','prigs'],1338:['ylwsa','yawls'],1339:['nmdora','rodman'],1340:['vsetbra','bravest'],1341:['mebra','embar'],1342:['afle','flea'],1343:['ilnsa','nails'],1344:['inmsera','remains'],
1345:['ypceor','recopy'],1346:['intera','retina'],1347:['pjea','jape'],1348:['inhgset','nighest'],1349:['uilnfgts','flutings'],1350:['ihcestok','chokiest'],1351:['linsda','island'],1352:['limst','milts'],1353:['impgea','magpie'],1354:['wnte','went'],1355:['ulpseca','specula'],1356:['lhsdora','holards'],
1357:['nbak','bank'],1358:['lnfsekra','flankers'],1359:['uilnfgo','fouling'],1360:['ulnmcora','columnar'],1361:['hotl','loth'],1362:['ilnhgso','longish'],1363:['ltesra','talers'],1364:['ulhtcera','trauchle'],1365:['ulsce','luces'],1366:['uilfda','aidful'],1367:['insedora','aneroids'],1368:['vuyscr','scurvy'],
1369:['hseda','hades'],1370:['inwgdo','dowing'],1371:['tpsa','spat'],1372:['ytsra','stray'],1373:['iceso','cosie'],1374:['lgsea','gales'],1375:['inwgtsra','strawing'],1376:['ifcera','fiacre'],1377:['luma','alum'],1378:['mhpsdora','dramshop'],1379:['inmhtsoa','manihots'],1380:['ilnseok','sonlike'],
1381:['lsekra','slaker'],1382:['drei','ired'],1383:['ulstea','salute'],1384:['yintce','nicety'],1385:['psera','rapes'],1386:['ulihscek','suchlike'],1387:['ilmob','limbo'],1388:['ucedr','crude'],1389:['uipcsd','cuspid'],1390:['vilcera','clavier'],1391:['mpctora','compart'],1392:['nhwgeda','whanged'],
1393:['inmgcera','creaming'],1394:['iltcera','article'],1395:['lnsora','lorans'],1396:['updoka','padouk'],1397:['vneka','knave'],1398:['uqhsba','buqsha'],1399:['ulfso','sulfo'],1400:['uilnfedr','unrifled'],1401:['uilmpcb','upclimb'],1402:['inmgsea','enigmas'],1403:['insdk','dinks'],1404:['npedra','pander'],
1405:['ipsedora','diaspore'],1406:['uinsedbx','subindex'],1407:['ilobra','bailor'],1408:['yimdra','myriad'],1409:['yilzsba','sizably'],1410:['vlntesra','ventrals'],1411:['ylftsoba','flyboats'],1412:['nteda','anted'],1413:['ltera','ratel'],1414:['imhwtceo','chowtime'],1415:['lptesa','pleats'],1416:['uilncto','linocut'],
1417:['linkgcba','blacking'],1418:['ilfst','flits'],1419:['uwtedor','outdrew'],1420:['ulfgsba','bagsful'],1421:['yilmtea','meatily'],1422:['vlsedo','solved'],1423:['npsdora','pardons'],1424:['uylhgte','teughly'],1425:['nhcetora','anchoret'],1426:['ilnhteca','ethnical'],1427:['onex','oxen'],1428:['uyintra','unitary'],
1429:['yinteax','anxiety'],1430:['yipcr','pyric'],1431:['untdo','donut'],1432:['ulicdobr','colubrid'],1433:['inmtseka','mistaken'],1434:['ulingsta','saluting'],1435:['ulima','miaul'],1436:['isedr','sired'],1437:['rtei','tier'],1438:['nmtseba','batsmen'],1439:['insdr','rinds'],1440:['ingscka','casking'],
1441:['untcedor','trounced'],1442:['ilpscer','splicer'],1443:['yihdo','hyoid'],1444:['unpka','punka'],1445:['yihcesk','hickeys'],1446:['jtos','jots'],1447:['ujedk','juked'],1448:['lnhgtes','lengths'],1449:['ypsor','prosy'],1450:['igbl','glib'],1451:['lkta','talk'],1452:['linpgsa','sapling'],
1453:['ulpghedo','ploughed'],1454:['doix','oxid'],1455:['uyhgto','toughy'],1456:['uctdba','abduct'],1457:['ihwteorz','howitzer'],1458:['inksbr','brinks'],1459:['hcma','mach'],1460:['ulmcesk','muckles'],1461:['yroe','yore'],1462:['dhol','hold'],1463:['vrli','virl'],1464:['lntera','rental'],
1465:['ugsra','guars'],1466:['pcedka','packed'],1467:['uhgsob','boughs'],1468:['ltsoka','skatol'],1469:['ncedo','coned'],1470:['psedra','padres'],1471:['wsta','wats'],1472:['ukrs','rusk'],1473:['isebr','ribes'],1474:['vedra','raved'],1475:['ulcetsr','relucts'],1476:['yihtc','itchy'],
1477:['znteba','bezant'],1478:['tcsora','actors'],1479:['iskra','rakis'],1480:['ilhgter','lighter'],1481:['vyipcra','privacy'],1482:['linhgsea','shealing'],1483:['wstea','twaes'],1484:['ungwtsoa','outgnaws'],1485:['uinhcsr','urchins'],1486:['uhgso','sough'],1487:['tedba','bated'],1488:['uksa','skua'],
1489:['imgseo','egoism'],1490:['lihst','hilts'],1491:['sector','escort'],1492:['vylintea','venality'],1493:['viscoa','ovisac'],1494:['nmcsora','macrons'],1495:['hptesda','heptads'],1496:['uilgser','ligures'],1497:['pseca','space'],1498:['otac','taco'],1499:['inwsed','widens'],1500:['lfwseor','wolfers'],
1501:['hwscea','cashew'],1502:['fcera','facer'],1503:['wcedobra','becoward'],1504:['ylnhcer','lyncher'],1505:['gzae','gaze'],1506:['uhgta','aught'],1507:['viger','giver'],1508:['sedbra','bardes'],1509:['uhgta','ghaut'],1510:['yiftcka','tackify'],1511:['onsf','fons'],1512:['ncesra','cranes'],
1513:['unfgseo','fungoes'],1514:['linpsec','splenic'],1515:['mwteokra','teamwork'],1516:['ulfscka','sackful'],1517:['mtsokra','ostmark'],1518:['ntsedra','stander'],1519:['vlnera','vernal'],1520:['ilntesr','linters'],1521:['hwpa','whap'],1522:['yitsx','xysti'],1523:['lhtcesra','trachles'],1524:['utsba','abuts'],
1525:['daei','idea'],1526:['imfgstra','misgraft'],1527:['yphtca','patchy'],1528:['ifhtces','fitches'],1529:['ylftoa','floaty'],1530:['ulged','glued'],1531:['lmebra','marble'],1532:['ucedkr','rucked'],1533:['vuedor','devour'],1534:['linctora','cilantro'],1535:['kseobr','bosker'],1536:['upsetrax','supertax'],
1537:['imsetbra','barmiest'],1538:['lncedkra','crankled'],1539:['iwsteda','waisted'],1540:['lmtea','metal'],1541:['umseo','mouse'],1542:['ylictda','dactyli'],1543:['ulnedkr','runkled'],1544:['lzedba','blazed'],1545:['nmteo','monte'],1546:['uliphsed','sulphide'],1547:['yimteda','daytime'],1548:['lnpsea','panels'],
1549:['ucestdr','crudest'],1550:['csokr','corks'],1551:['hcobra','broach'],1552:['ilmsebr','limbers'],1553:['umhtseoa','outshame'],1554:['ylgea','agley'],1555:['inptsr','prints'],1556:['ulngsebr','bunglers'],1557:['cedokr','docker'],1558:['hwsta','thaws'],1559:['uymhgcer','chemurgy'],1560:['uqtedor','torqued'],
1561:['mwsebra','beswarm'],1562:['viwseta','waviest'],1563:['utedba','tabued'],1564:['ypwka','pawky'],1565:['lwsco','cowls'],1566:['vylpeor','overply'],1567:['hgtsedo','ghosted'],1568:['ulngseo','lounges'],1569:['vylsera','slavery'],1570:['unmsekra','unmasker'],1571:['ulngtes','engluts'],1572:['ilmkcesb','limbecks'],
1573:['ilnhteo','neolith'],1574:['nweor','rowen'],1575:['ilnpgsra','springal'],1576:['linhgtca','latching'],1577:['lwebra','bawler'],1578:['ihcesra','cahiers'],1579:['linpgoka','polkaing'],1580:['vimtesor','vomiters'],1581:['unebra','unbear'],1582:['tseka','stake'],1583:['lmpceso','compels'],1584:['ilgcesra','glaciers'],
1585:['ngsda','dangs'],1586:['ulinmgsc','muscling'],1587:['ncesra','caners'],1588:['mbea','beam'],1589:['ylfea','leafy'],1590:['nhgcera','changer'],1591:['ulnhcdba','clubhand'],1592:['nphcea','pechan'],1593:['sckra','racks'],1594:['inmsed','denims'],1595:['ilpct','clipt'],1596:['unmte','unmet'],
1597:['ibhsedok','kiboshed'],1598:['uynpsk','spunky'],1599:['untsd','dunts'],1600:['upsca','scaup'],1601:['uyifjts','justify'],1602:['lihcesd','chields'],1603:['vylpeora','overplay'],1604:['yedoka','kayoed'],1605:['uinwse','unwise'],1606:['ulftesr','restful'],1607:['yibckr','bricky'],1608:['unfra','furan'],
1609:['uhtsed','shuted'],1610:['ulnfseo','sulfone'],1611:['mhre','herm'],1612:['ylsedor','yodlers'],1613:['yneorax','anorexy'],1614:['ynhtcesa','chanteys'],1615:['lipedor','leporid'],1616:['liwsed','wields'],1617:['inmsra','inarms'],1618:['yipgdor','prodigy'],1619:['auitskrz','zikurats'],1620:['lbmseoka','smokable'],
1621:['incekr','nicker'],1622:['aimtecoz','azotemic'],1623:['vlinsa','vinals'],1624:['lifca','calif'],1625:['lised','isled'],1626:['uhgto','ought'],1627:['hwcesdor','cowherds'],1628:['hsceda','cashed'],1629:['vicetsor','evictors'],1630:['lsdor','lords'],1631:['npseka','pekans'],1632:['yiltebr','liberty'],
1633:['ihsedr','hiders'],1634:['ynpho','phony'],1635:['istck','ticks'],1636:['mwsor','worms'],1637:['ylngeora','yearlong'],1638:['itscedk','sticked'],1639:['ymhsca','chasmy'],1640:['ptea','pate'],1641:['iphsecr','spheric'],1642:['yilnhor','hornily'],1643:['liteor','toiler'],1644:['ujcsoba','jacobus'],
1645:['ilfcor','frolic'],1646:['ingtedba','debating'],1647:['ynma','myna'],1648:['uhtcseoa','cathouse'],1649:['igteda','gaited'],1650:['yinwte','witney'],1651:['lceda','laced'],1652:['lihgsdoa','hidalgos'],1653:['lnhcesoa','chalones'],1654:['ynseo','nosey'],1655:['uijob','bijou'],1656:['uliqted','quilted'],
1657:['mptcso','compts'],1658:['inmsera','seminar'],1659:['lngseo','longes'],1660:['imseokr','smokier'],1661:['yhtesdra','hydrates'],1662:['uligseoa','eulogias'],1663:['ilgco','logic'],1664:['mhse','hems'],1665:['hukl','hulk'],1666:['uinmte','mutine'],1667:['yntseo','stoney'],1668:['unmtser','sternum'],
1669:['vlingtea','valeting'],1670:['uiqnedo','quoined'],1671:['hsea','haes'],1672:['ynpsedoa','dyspnoea'],1673:['vlingera','raveling'],1674:['itesbra','terbias'],1675:['ueax','eaux'],1676:['ingtedra','gradient'],1677:['uktedoba','outbaked'],1678:['nhtscera','stancher'],1679:['onme','omen'],1680:['ylipsda','display'],
1681:['uiqnce','cinque'],1682:['gbye','gybe'],1683:['uptseoka','outspeak'],1684:['inpwgeor','powering'],1685:['nhgtsea','stengah'],1686:['imptera','primate'],1687:['yifmdo','modify'],1688:['hsera','hares'],1689:['ilntea','entail'],1690:['unmhcer','muncher'],1691:['uinpgso','souping'],1692:['uinfgser','gunfires'],
1693:['goyl','logy'],1694:['vusetbr','subvert'],1695:['untcka','untack'],1696:['ptesdor','redtops'],1697:['imter','mitre'],1698:['inhor','rhino'],1699:['htea','hate'],1700:['istoa','iotas'],1701:['jeokr','joker'],1702:['dwea','wade'],1703:['ingor','groin'],1704:['uncedra','durance'],
1705:['ulikebra','baulkier'],1706:['iwcsdobr','cowbirds'],1707:['iptcor','tropic'],1708:['ylnmtora','matronly'],1709:['intseda','stained'],1710:['vimser','vermis'],1711:['ifser','fries'],1712:['vilpseo','plosive'],1713:['yimtsed','stymied'],1714:['lnpgedoa','anglepod'],1715:['ylnckra','crankly'],1716:['nfheo','foehn'],
1717:['igteor','goitre'],1718:['pceba','becap'],1719:['ulinmdr','drumlin'],1720:['ulqingca','calquing'],1721:['vlnfeoa','flavone'],1722:['jkca','jack'],1723:['inmed','mined'],1724:['viner','riven'],1725:['ynmska','skyman'],1726:['linhgeax','exhaling'],1727:['ylceda','clayed'],1728:['ypwsa','waspy'],
1729:['ytser','treys'],1730:['ngweda','gnawed'],1731:['lhwseor','howlers'],1732:['ingsdra','gradins'],1733:['ulnfscor','scornful'],1734:['lweda','lawed'],1735:['ledora','loader'],1736:['ousl','soul'],1737:['itsex','exist'],1738:['intedr','rident'],1739:['fedra','fader'],1740:['iedbr','bride'],
1741:['insera','arsine'],1742:['ftedra','rafted'],1743:['ulitsor','troilus'],1744:['yljto','jolty'],1745:['lwei','wile'],1746:['mgdoa','dogma'],1747:['ulinjgts','justling'],1748:['imtecr','metric'],1749:['gnoe','gone'],1750:['inmcor','micron'],1751:['ulmpse','plumes'],1752:['ligteoka','goatlike'],
1753:['ulfed','flued'],1754:['vilpse','pelvis'],1755:['uilqsor','liquors'],1756:['yisek','skiey'],1757:['dhsi','dish'],1758:['htesba','bathes'],1759:['ilngdra','darling'],1760:['vunpedor','unproved'],1761:['uilmpset','lumpiest'],1762:['uhgtso','toughs'],1763:['yncedra','ardency'],1764:['yhtec','techy'],
1765:['nwtso','towns'],1766:['intsera','stearin'],1767:['unhceo','cohune'],1768:['ugsedor','gourdes'],1769:['uinmcora','coumarin'],1770:['nmsedba','bedamns'],1771:['yilzgera','glaziery'],1772:['umhgsbra','hamburgs'],1773:['ilptesor','poitrels'],1774:['mpceora','compare'],1775:['uqnsedra','squander'],1776:['ynmpta','tympan'],
1777:['uilngce','clueing'],1778:['lnseda','naleds'],1779:['uilntces','cutlines'],1780:['ulpstob','subplot'],1781:['home','home'],1782:['ihtseor','shortie'],1783:['aumgsez','zeugmas'],1784:['vedor','drove'],1785:['nwsdor','drowns'],1786:['honr','horn'],1787:['cesdkra','dackers'],1788:['vylea','leavy'],
1789:['lpedo','loped'],1790:['urel','lure'],1791:['ulftsoba','boastful'],1792:['incsa','cains'],1793:['ulpwka','walkup'],1794:['ulfted','fluted'],1795:['aiedz','azide'],1796:['tyur','yurt'],1797:['ihtecd','itched'],1798:['ainhtoz','hoatzin'],1799:['ulinteka','auntlike'],1800:['yksa','kays'],
1801:['nksi','skin'],1802:['uncebra','unbrace'],1803:['viwset','swivet'],1804:['inkgebra','beraking'],1805:['imgcesra','grimaces'],1806:['ngsra','gnars'],1807:['ylpsa','plays'],1808:['yilperax','pyrexial'],1809:['cedkr','dreck'],1810:['fsora','sofar'],1811:['yingtax','taxying'],1812:['hsedor','horsed'],
1813:['lbihokra','kohlrabi'],1814:['litora','rialto'],1815:['usdbr','burds'],1816:['pgseor','gropes'],1817:['inpgscra','scraping'],1818:['gbol','glob'],1819:['imhscr','smirch'],1820:['ymsez','zymes'],1821:['ulnedo','nodule'],1822:['ilged','glide'],1823:['uisetdb','subedit'],1824:['liteso','toiles'],
1825:['msbra','barms'],1826:['ulfcea','fecula'],1827:['hpcora','carhop'],1828:['ptea','tape'],1829:['htcea','cheat'],1830:['ulkwsbra','bulwarks'],1831:['ilngso','losing'],1832:['nfteo','often'],1833:['linwgsco','scowling'],1834:['wbsa','wabs'],1835:['mhgeoa','homage'],1836:['osmi','miso'],
1837:['ulngwtor','lungwort'],1838:['uimpebr','bumpier'],1839:['ypsedra','sprayed'],1840:['inhtcesz','chintzes'],1841:['ilnweob','bowline'],1842:['uilnfpa','painful'],1843:['nmpcora','crampon'],1844:['ulndra','lurdan'],1845:['heoba','obeah'],1846:['vlimtsoa','voltaism'],1847:['okme','moke'],1848:['mpsca','scamp'],
1849:['vilhsera','lavisher'],1850:['ubnk','bunk'],1851:['lpcetska','plackets'],1852:['vuyicta','vacuity'],1853:['mhsea','shame'],1854:['ytseda','stayed'],1855:['twse','stew'],1856:['ymfoa','foamy'],1857:['tedra','dater'],1858:['lwsco','scowl'],1859:['duel','leud'],1860:['lingtcka','tackling'],
1861:['injtsora','janitors'],1862:['unhcsobr','bronchus'],1863:['usebz','zebus'],1864:['cedoax','coaxed'],1865:['ihtsbr','births'],1866:['ulfta','fault'],1867:['uingsecr','recusing'],1868:['injtesor','jointers'],1869:['puel','pule'],1870:['mhobr','rhomb'],1871:['ylsdka','alkyds'],1872:['yilngeb','belying'],
1873:['ylera','layer'],1874:['impeora','meropia'],1875:['uinmted','mutined'],1876:['uptsedra','upstared'],1877:['lwsoa','awols'],1878:['peax','apex'],1879:['imeob','biome'],1880:['ultser','ulster'],1881:['gedbra','badger'],1882:['unwsera','unswear'],1883:['iptesr','tripes'],1884:['ingcedr','cringed'],
1885:['uilhtek','hutlike'],1886:['mhwpo','whomp'],1887:['wedob','bowed'],1888:['ylmra','marly'],1889:['unta','aunt'],1890:['inmseora','romaines'],1891:['lgsoa','gaols'],1892:['lintsea','elastin'],1893:['liteka','talkie'],1894:['inteca','enatic'],1895:['nhtes','thens'],1896:['iscedbra','ascribed'],
1897:['iwedbra','bawdier'],1898:['ifhce','chief'],1899:['imhtecdo','methodic'],1900:['ihgwt','wight'],1901:['lgweokr','legwork'],1902:['uylcseor','crousely'],1903:['ipceokr','pockier'],1904:['uilntes','luteins'],1905:['yilftsor','frostily'],1906:['utcsora','turacos'],1907:['ilsedob','bolides'],1908:['yhpcora','charpoy'],
1909:['ngceor','conger'],1910:['ulgcseo','glucose'],1911:['hwzi','whiz'],1912:['pgsor','progs'],1913:['ungedr','nudger'],1914:['lnseob','nobles'],1915:['uigsed','guised'],1916:['virax','varix'],1917:['lcska','lacks'],1918:['cmae','mace'],1919:['ultsedo','tousled'],1920:['yilnwgo','yowling'],
1921:['uktc','tuck'],1922:['inpgseor','spongier'],1923:['icesor','cosier'],1924:['ltera','alter'],1925:['nfgtera','engraft'],1926:['iznctesa','zincates'],1927:['tceso','cotes'],1928:['inhwgco','chowing'],1929:['ntes','nets'],1930:['lphwedoa','plowhead'],1931:['upsor','roups'],1932:['wtseobax','sweatbox'],
1933:['ifedr','fired'],1934:['tedoba','boated'],1935:['owsc','scow'],1936:['itdba','tabid'],1937:['nhgsa','hangs'],1938:['ilnmpsea','maniples'],1939:['inwtsa','twains'],1940:['isedob','dobies'],1941:['intser','sinter'],1942:['mpceoa','pomace'],1943:['gunl','lung'],1944:['ilmpb','blimp'],
1945:['yngora','orangy'],1946:['pusl','plus'],1947:['ylnpedra','repandly'],1948:['vlcokra','lavrock'],1949:['ulncso','consul'],1950:['npceo','copen'],1951:['nmsea','manes'],1952:['nceda','caned'],1953:['pgheor','gopher'],1954:['gcesk','gecks'],1955:['yinmstda','dynamist'],1956:['injdoa','adjoin'],
1957:['yusca','saucy'],1958:['ucetdor','eductor'],1959:['intsra','santir'],1960:['dnsi','dins'],1961:['uimhcer','rheumic'],1962:['ulinmpco','pulmonic'],1963:['vntesda','advents'],1964:['ipcdora','picador'],1965:['ilpseca','special'],1966:['ygseoz','zygose'],1967:['ulnfera','flaneur'],1968:['vlgedo','gloved'],
1969:['posy','posy'],1970:['ultedobr','troubled'],1971:['brea','brae'],1972:['ilpcera','replica'],1973:['yilnk','linky'],1974:['vugeo','vogue'],1975:['utsdr','turds'],1976:['inmpgra','ramping'],1977:['lncesor','cornels'],1978:['ulcda','cauld'],1979:['ulgtsera','gestural'],1980:['lteok','ketol'],
1981:['inmcsora','minorcas'],1982:['vlweor','wolver'],1983:['ihtedor','theroid'],1984:['ulmseda','almudes'],1985:['ylneda','adenyl'],1986:['iltedbz','blitzed'],1987:['inmwgo','mowing'],1988:['yimseok','misyoke'],1989:['inmgora','roaming'],1990:['uinmcesr','numerics'],1991:['inwsdra','inwards'],1992:['gjsi','jigs'],
1993:['ilhteso','eoliths'],1994:['lnkceba','blacken'],1995:['gtera','great'],1996:['nwsera','answer'],1997:['hgso','gosh'],1998:['ktre','trek'],1999:['liwebra','brawlie'],2000:['uilnmfed','fulmined'],2001:['vista','vista'],2002:['uyiltcsr','crustily'],2003:['dubr','burd'],2004:['ylhpcea','cheaply'],
2005:['inmphcea','camphine'],2006:['ihctesoa','achiotes'],2007:['lwsba','bawls'],2008:['ylimsera','mislayer'],2009:['hsedra','dasher'],2010:['umhtesa','humates'],2011:['ngteor','tonger'],2012:['lihces','chiles'],2013:['unpter','punter'],2014:['ingrax','raxing'],2015:['obrax','borax'],2016:['yihcskra','hayricks'],
2017:['dpum','dump'],2018:['licax','calix'],2019:['imgebra','gambier'],2020:['inpwsra','inwraps'],2021:['hgni','nigh'],2022:['ltsekra','stalker'],2023:['ntesob','betons'],2024:['ilmtsoa','somital'],2025:['ulnea','ulnae'],2026:['aingdz','dazing'],2027:['iktsbra','britska'],2028:['iptco','picot'],
2029:['hsecorz','scherzo'],2030:['yimhts','smithy'],2031:['ymhtscoa','stomachy'],2032:['yilha','haily'],2033:['yizneka','kyanize'],2034:['uylpsebr','superbly'],2035:['vlmsera','marvels'],2036:['uces','cues'],2037:['hgwtor','growth'],2038:['ylnmhto','monthly'],2039:['vnceo','coven'],2040:['ingsetda','sedating'],
2041:['inger','reign'],2042:['uilnfces','funicles'],2043:['uimhdor','humidor'],2044:['mwsedor','deworms'],2045:['ltedka','talked'],2046:['uptbra','abrupt'],2047:['ugdobr','dorbug'],2048:['ylfptsra','flytraps'],2049:['uinhsor','nourish'],2050:['lngedra','dangler'],2051:['vuicestr','curviest'],2052:['inmseda','maidens'],
2053:['mekra','maker'],2054:['lmebra','ambler'],2055:['pwso','wops'],2056:['lwedob','bowled'],2057:['lwya','waly'],2058:['inphsedo','siphoned'],2059:['uyfsr','surfy'],2060:['kseba','bakes'],2061:['vihgteo','eightvo'],2062:['inkbr','brink'],2063:['lhsera','lasher'],2064:['inmptsoa','maintops'],
2065:['icesra','ericas'],2066:['mpcetora','mercapto'],2067:['pyua','yaup'],2068:['uiqcer','cirque'],2069:['ulipseor','perilous'],2070:['yisetobr','sobriety'],2071:['uylhser','hurleys'],2072:['vlingsea','sleaving'],2073:['liptedo','piloted'],2074:['ulmpeo','pumelo'],2075:['wscora','sowcar'],2076:['inhwgtor','throwing'],
2077:['ilptsoa','topsail'],2078:['apel','leap'],2079:['unte','tune'],2080:['ncdora','candor'],2081:['linmged','mingled'],2082:['viler','livre'],2083:['nphtesoa','phonates'],2084:['ulfsor','flours'],2085:['ngwseora','wagoners'],2086:['nmedoa','daemon'],2087:['puns','puns'],2088:['isetdr','driest'],
2089:['lnfseo','felons'],2090:['ynmphte','nymphet'],2091:['iltesbz','blitzes'],2092:['lifteka','fatlike'],2093:['unpsedr','spurned'],2094:['ypsdor','dropsy'],2095:['lceobr','corbel'],2096:['uinhtsda','dianthus'],2097:['ynmeobr','embryon'],2098:['ylebr','beryl'],2099:['gcesdora','cordages'],2100:['tesba','bates'],
2101:['uyincsor','cousinry'],2102:['fgsor','frogs'],2103:['imsetk','kismet'],2104:['iptobr','probit'],2105:['vedbra','braved'],2106:['bcra','crab'],2107:['uqsekra','quakers'],2108:['impsetk','miskept'],2109:['lieor','reoil'],2110:['tmae','mate'],2111:['usckr','rucks'],2112:['uilfhws','wishful'],
2113:['sdbra','brads'],2114:['uhgcta','caught'],2115:['uingceda','guidance'],2116:['viser','siver'],2117:['yingts','stying'],2118:['inpgcok','pocking'],2119:['ilznga','lazing'],2120:['uligedoa','dialogue'],2121:['yimta','amity'],2122:['uincesd','incudes'],2123:['vlseoa','loaves'],2124:['sedkra','drakes'],
2125:['ungtesdr','trudgens'],2126:['ufmwseoa','wamefous'],2127:['ulipa','pilau'],2128:['uilfmso','foliums'],2129:['ingceoz','cognize'],2130:['lgebra','garble'],2131:['dgri','gird'],2132:['nhteobr','bethorn'],2133:['neorz','zoner'],2134:['inwgca','cawing'],2135:['ztesra','ersatz'],2136:['ipstdor','disport'],
2137:['yhsedra','hydrase'],2138:['ugsra','gaurs'],2139:['yphsced','psyched'],2140:['ipsca','spica'],2141:['vilhcer','chervil'],2142:['injso','joins'],2143:['iblseka','skiable'],2144:['lnpteda','planted'],2145:['itsedkr','skirted'],2146:['unpgsr','sprung'],2147:['uylcr','curly'],2148:['vyiwe','viewy'],
2149:['ingted','nidget'],2150:['utces','cutes'],2151:['uympghr','grumphy'],2152:['unjceso','jounces'],2153:['imhced','chimed'],2154:['ipcedkr','pricked'],2155:['mhcteora','chromate'],2156:['lingje','jingle'],2157:['uinmtesr','terminus'],2158:['yntesoba','bayonets'],2159:['lhcesora','chorales'],2160:['ultesdob','doublets'],
2161:['posh','soph'],2162:['yltseba','beastly'],2163:['uiqps','quips'],2164:['phcedoa','poached'],2165:['lwcesbra','becrawls'],2166:['msera','marse'],2167:['inmgsedo','smidgeon'],2168:['vlceso','cloves'],2169:['inwtes','twines'],2170:['msebra','breams'],2171:['urme','mure'],2172:['unwtcdo','cutdown'],
2173:['incdra','rancid'],2174:['uinmser','mureins'],2175:['uctdobra','abductor'],2176:['lpsa','pals'],2177:['pusa','upas'],2178:['ilmpera','lempira'],2179:['infsk','finks'],2180:['ihwces','wiches'],2181:['mhceor','chrome'],2182:['limcesax','exclaims'],2183:['phtso','tophs'],2184:['yilnpheb','biphenyl'],
2185:['uqtesora','equators'],2186:['ynmgseoz','zymogens'],2187:['uinmctoa','aconitum'],2188:['umsra','ramus'],2189:['yilpted','tepidly'],2190:['yipstdoa','dystopia'],2191:['umle','mule'],2192:['vfmweora','waveform'],2193:['acedrz','crazed'],2194:['ylinsdka','ladykins'],2195:['vylnsora','sovranly'],2196:['iseca','saice'],
2197:['uinmpger','impugner'],2198:['yptesoa','teapoys'],2199:['inmdoa','domain'],2200:['ilhedba','hidable'],2201:['inpsor','prison'],2202:['yphsce','psyche'],2203:['uimsok','koumis'],2204:['infcesda','faciends'],2205:['lihcedra','heraldic'],2206:['uinftx','unfixt'],2207:['uyltoa','outlay'],2208:['ylnfdo','fondly'],
2209:['ihtca','aitch'],2210:['ynwska','swanky'],2211:['uytcsr','curtsy'],2212:['istl','slit'],2213:['ftera','after'],2214:['unmeda','unmade'],2215:['ynmseo','moneys'],2216:['ilnpceso','pinocles'],2217:['ulinhgdr','hurdling'],2218:['npwtsea','stewpan'],2219:['inmgco','coming'],2220:['dous','ouds'],
2221:['ltsedba','stabled'],2222:['uinjedr','injured'],2223:['iltseobr','strobile'],2224:['unfset','funest'],2225:['uynhsta','unhasty'],2226:['uyintbra','urbanity'],2227:['unmsba','busman'],2228:['ncobra','carbon'],2229:['tmie','mite'],2230:['fstea','fates'],2231:['dfea','deaf'],2232:['yilnwta','tawnily'],
2233:['done','done'],2234:['yhcetr','cherty'],2235:['bsfi','fibs'],2236:['ulnfge','engulf'],2237:['lktscoba','slotback'],2238:['ylgor','glory'],2239:['lseda','dales'],2240:['ypgseo','pogeys'],2241:['lingjse','jingles'],2242:['injseba','basenji'],2243:['umgera','mauger'],2244:['ulingcdo','clouding'],
2245:['ulijeb','jubile'],2246:['uingtedb','debuting'],2247:['uinjgtso','jousting'],2248:['vylsta','vastly'],2249:['unpedobr','unprobed'],2250:['lpgsea','plages'],2251:['yimcsra','myricas'],2252:['vyusdor','dyvours'],2253:['inmtedob','intombed'],2254:['ilnpto','pontil'],2255:['ulpedora','poularde'],2256:['ybea','abye'],
2257:['ilnhsoba','hobnails'],2258:['uimgto','gomuti'],2259:['pocy','copy'],2260:['domi','modi'],2261:['ilngseda','signaled'],2262:['nhtceso','notches'],2263:['vtsera','starve'],2264:['ynmseba','bynames'],2265:['limpsda','plasmid'],2266:['uylser','surely'],2267:['gsea','ages'],2268:['uylngta','gauntly'],
2269:['luca','caul'],2270:['uylmpcr','crumply'],2271:['vsetr','verst'],2272:['nedobra','bandore'],2273:['unhwstea','unswathe'],2274:['ilnteora','oriental'],2275:['uncsokr','uncorks'],2276:['ylimpdoa','olympiad'],2277:['npsea','napes'],2278:['iphedra','raphide'],2279:['vuntesra','vaunters'],2280:['tosl','lost'],
2281:['uynphc','punchy'],2282:['nris','rins'],2283:['yihtsr','yirths'],2284:['unpsedox','expounds'],2285:['lgtedoa','gloated'],2286:['tgra','grat'],2287:['aulnoz','zonula'],2288:['ylfhtera','fatherly'],2289:['vinseokr','invokers'],2290:['unjcea','jaunce'],2291:['lnptesax','explants'],2292:['ihgteo','hogtie'],
2293:['ulhseo','housel'],2294:['lmedba','lambed'],2295:['ntesa','nates'],2296:['ylmtea','tamely'],2297:['hwser','shrew'],2298:['uons','nous'],2299:['yilpsor','prosily'],2300:['nmphtoa','phantom'],2301:['gtel','gelt'],2302:['lipra','pilar'],2303:['dnsa','ands'],2304:['lgya','agly'],
2305:['ulmera','mauler'],2306:['uynger','gurney'],2307:['uhgcera','gaucher'],2308:['inmseda','medians'],2309:['yinpgco','copying'],2310:['wnya','wany'],2311:['yliwed','dewily'],2312:['ylimedo','myeloid'],2313:['ylnso','sonly'],2314:['vulseo','ovules'],2315:['ilfeda','failed'],2316:['lmsedora','earldoms'],
2317:['vilne','liven'],2318:['ingcra','caring'],2319:['aleoz','azole'],2320:['lota','alto'],2321:['ulitera','uralite'],2322:['ilnfgsea','finagles'],2323:['hjeda','jehad'],2324:['yedbra','redbay'],2325:['nptdoa','dopant'],2326:['igtsedor','stodgier'],2327:['uncsob','buncos'],2328:['fekra','faker'],
2329:['oryx','oryx'],2330:['ulnte','unlet'],2331:['ulinfhgs','lungfish'],2332:['lihgteda','gilthead'],2333:['ilnwek','welkin'],2334:['psma','pams'],2335:['inhjctea','jacinthe'],2336:['upscer','spruce'],2337:['inhgcra','arching'],2338:['ltseb','blest'],2339:['imscea','camise'],2340:['imsba','bimas'],
2341:['linmgteo','longtime'],2342:['ukhsebra','hauberks'],2343:['yinmhces','chimneys'],2344:['ilmhso','holism'],2345:['unhgteso','toughens'],2346:['guns','snug'],2347:['ykfe','fyke'],2348:['lcetsba','cablets'],2349:['ygsor','gyros'],2350:['ictdoa','dacoit'],2351:['linmedob','imbolden'],2352:['dpor','dorp'],
2353:['iphcor','orphic'],2354:['vulipsea','plausive'],2355:['ulcex','culex'],2356:['untcedoa','outdance'],2357:['vnsetra','versant'],2358:['unkob','bunko'],2359:['vlncetoa','covalent'],2360:['linhceor','chlorine'],2361:['unjcdo','jocund'],2362:['lhwek','whelk'],2363:['izptesba','baptizes'],2364:['uifgteda','fatigued'],
2365:['ilster','lister'],2366:['uynphca','paunchy'],2367:['lpteoba','potable'],2368:['tsea','east'],2369:['uilcd','lucid'],2370:['ncedok','nocked'],2371:['litsebra','blastier'],2372:['yihtsecr','hysteric'],2373:['nteobra','reboant'],2374:['inhcs','chins'],2375:['imerx','mixer'],2376:['unptso','putons'],
2377:['ytesbra','barytes'],2378:['ifsdo','fidos'],2379:['ngedra','ranged'],2380:['imptedra','preadmit'],2381:['fdobra','forbad'],2382:['ulmsdkra','mudlarks'],2383:['utcera','acuter'],2384:['ylinpta','ptyalin'],2385:['inwtesr','winters'],2386:['nhpceora','chaperon'],2387:['lingtcoa','locating'],2388:['ultebr','butler'],
2389:['ipscr','crisp'],2390:['nhtedor','thorned'],2391:['ylcea','lycea'],2392:['ilpsedba','piebalds'],2393:['hwtsra','swarth'],2394:['ilzseta','laziest'],2395:['nhseora','hoarsen'],2396:['ungsb','bungs'],2397:['hpseda','hasped'],2398:['litsdoba','tabloids'],2399:['ulstebra','baluster'],2400:['lmptsora','marplots'],
2401:['utesbr','brutes'],2402:['uicra','curia'],2403:['iftdr','drift'],2404:['unsobr','suborn'],2405:['gwsa','wags'],2406:['dhel','held'],2407:['gcedora','cordage'],2408:['vlisa','silva'],2409:['yuiqphse','physique'],2410:['mceoa','cameo'],2411:['ulmgwsor','lugworms'],2412:['yilnhte','ethinyl'],
2413:['uilmper','lumpier'],2414:['ylmea','mealy'],2415:['nkti','knit'],2416:['mfsera','frames'],2417:['edoba','adobe'],2418:['nhgseda','gnashed'],2419:['iodl','lido'],2420:['ifgsr','frigs'],2421:['doul','loud'],2422:['yledbra','dryable'],2423:['intcdora','tornadic'],2424:['ipsectd','discept'],
2425:['lfweor','reflow'],2426:['ylfweor','flowery'],2427:['inpcsa','panics'],2428:['pcetsok','pockets'],2429:['viwera','waiver'],2430:['inmtea','etamin'],2431:['ultesb','bluets'],2432:['unsdobra','baudrons'],2433:['ypsora','payors'],2434:['intse','senti'],2435:['dsra','rads'],2436:['csokra','croaks'],
2437:['nfgoa','ganof'],2438:['ipgsetdo','podgiest'],2439:['uimgtso','gomutis'],2440:['unmsted','dustmen'],2441:['limhedoa','halidome'],2442:['utel','lute'],2443:['uisdbra','subarid'],2444:['lbak','balk'],2445:['ulcesr','lucres'],2446:['prma','pram'],2447:['dhca','chad'],2448:['ingtesra','ingrates'],
2449:['ipsedr','redips'],2450:['okna','kaon'],2451:['ngtsoa','tangos'],2452:['nhcedbra','branched'],2453:['hpsea','shape'],2454:['ulfpwedo','upflowed'],2455:['uylnsa','unlays'],2456:['unmgtea','mutagen'],2457:['uwtsr','wurst'],2458:['ultska','taluks'],2459:['uylsk','sulky'],2460:['nmsea','manse'],
2461:['hseda','shade'],2462:['gots','togs'],2463:['psti','pits'],2464:['ilnso','loins'],2465:['yhtedk','kythed'],2466:['uilfsed','sulfide'],2467:['yptcr','crypt'],2468:['nweda','waned'],2469:['gwsea','wages'],2470:['ilnfgea','leafing'],2471:['lipser','perils'],2472:['ilceor','recoil'],
2473:['ilngbra','blaring'],2474:['iktsba','batiks'],2475:['wsdra','sward'],2476:['vinpgsa','pavings'],2477:['nmedor','normed'],2478:['nhcedora','anchored'],2479:['lwsebra','warbles'],2480:['lpseo','poles'],2481:['izcstra','czarist'],2482:['npedora','aproned'],2483:['vigsera','rivages'],2484:['ipseorx','proxies'],
2485:['lgedoa','gaoled'],2486:['incetsba','cabinets'],2487:['terax','taxer'],2488:['ulnsdo','unsold'],2489:['ilnwgte','welting'],2490:['vlfora','flavor'],2491:['ulmora','morula'],2492:['limtera','marlite'],2493:['iphscdoa','scaphoid'],2494:['ildra','drail'],2495:['ltsedka','stalked'],2496:['ltsea','slate'],
2497:['inpse','penis'],2498:['inpgeor','perigon'],2499:['kcsob','bocks'],2500:['uhpseka','shakeup'],2501:['ingcdor','cording'],2502:['igcedbra','birdcage'],2503:['nwcesdor','decrowns'],2504:['uimptes','uptimes'],2505:['osel','sole'],2506:['ylnphe','phenyl'],2507:['ufcesor','refocus'],2508:['ilnger','linger'],
2509:['lnptsora','plastron'],2510:['vinedok','invoked'],2511:['vlinser','silvern'],2512:['usecr','sucre'],2513:['linmga','malign'],2514:['ifptsox','postfix'],2515:['uptsdra','updarts'],2516:['uinfgsdo','fungoids'],2517:['uimtesd','tediums'],2518:['linhstda','handlist'],2519:['wsera','resaw'],2520:['vynsedka','vandykes'],
2521:['nmhcera','marchen'],2522:['heoba','bohea'],2523:['ygebr','gyber'],2524:['vilnek','kelvin'],2525:['iftedo','foetid'],2526:['pjsea','japes'],2527:['ulmwekra','lukewarm'],2528:['incetdra','dicentra'],2529:['nseobra','boranes'],2530:['inscteoa','sonicate'],2531:['hsera','share'],2532:['mpcetso','coempts'],
2533:['imtsekra','mistaker'],2534:['obrw','brow'],2535:['uptso','stoup'],2536:['ilnfgdo','folding'],2537:['yseobra','rosebay'],2538:['ungse','negus'],2539:['ligda','algid'],2540:['ilfhgts','flights'],2541:['unlk','lunk'],2542:['wtedor','trowed'],2543:['wteka','tweak'],2544:['insedra','randies'],
2545:['imheorz','rhizome'],2546:['uinfgsr','surfing'],2547:['mhteor','mother'],2548:['ulmse','mules'],2549:['yilhsda','ladyish'],2550:['untceora','outrance'],2551:['lised','sidle'],2552:['inpcetor','inceptor'],2553:['nhdora','hadron'],2554:['ylfcekr','freckly'],2555:['lnmpwoa','plowman'],2556:['uinmstdo','dismount'],
2557:['inhgeda','heading'],2558:['unhgeor','roughen'],2559:['inmgebra','breaming'],2560:['iedba','abied'],2561:['ylnpte','plenty'],2562:['inphskra','prankish'],2563:['lnera','renal'],2564:['unsdoba','bausond'],2565:['uphwter','upthrew'],2566:['uyfgra','argufy'],2567:['dsma','dams'],2568:['yinhgs','shying'],
2569:['linmpgsa','psalming'],2570:['lhteora','rathole'],2571:['mwtoba','wombat'],2572:['uftse','fetus'],2573:['imsera','aimers'],2574:['uqcka','quack'],2575:['ilpght','plight'],2576:['vuilseca','vesicula'],2577:['ilmdoa','amidol'],2578:['yijedor','joyride'],2579:['uitesda','dauties'],2580:['vuipseor','pervious'],
2581:['ingera','reagin'],2582:['inphtera','perianth'],2583:['lnmgseor','mongrels'],2584:['auitedz','deutzia'],2585:['inpgseka','speaking'],2586:['lweobr','bowler'],2587:['ilmge','glime'],2588:['hota','oath'],2589:['uinjser','injures'],2590:['uimsebr','imbrues'],2591:['ulper','puler'],2592:['ynceo','coney'],
2593:['uhgtdor','drought'],2594:['iphstcda','dispatch'],2595:['uinmhse','inhumes'],2596:['lnptesa','planets'],2597:['uhtcso','couths'],2598:['npcedra','pranced'],2599:['inptsor','tropins'],2600:['ledobr','bolder'],2601:['uqtera','quarte'],2602:['inmgsed','smidgen'],2603:['uinfmha','hafnium'],2604:['nsoka','koans'],
2605:['uinpsdb','upbinds'],2606:['liptesr','triples'],2607:['vylsa','sylva'],2608:['ingsr','grins'],2609:['ylnmhsa','hymnals'],2610:['inmhgcor','chroming'],2611:['pseora','operas'],2612:['ilnfwgo','wolfing'],2613:['icestokr','rockiest'],2614:['ilnptera','interlap'],2615:['ulmteb','tumble'],2616:['ultesbr','butlers'],
2617:['imcedr','dermic'],2618:['neoax','axone'],2619:['ylnsebra','blarneys'],2620:['iscor','coirs'],2621:['ihgedr','dreigh'],2622:['nkteob','beknot'],2623:['ulnmhe','unhelm'],2624:['nwsbra','brawns'],2625:['lpcsdoka','padlocks'],2626:['uymck','mucky'],2627:['uinmsra','uranism'],2628:['tisa','sati'],
2629:['nhwgsa','whangs'],2630:['htceor','hector'],2631:['gonl','long'],2632:['yiltecra','literacy'],2633:['ulftedo','flouted'],2634:['ulcka','caulk'],2635:['yinps','spiny'],2636:['nsik','sink'],2637:['ipedra','repaid'],2638:['yimsdra','myriads'],2639:['imcekra','keramic'],2640:['igsta','agist'],
2641:['cerax','carex'],2642:['pwei','wipe'],2643:['uilnfsk','skinful'],2644:['wgedora','wordage'],2645:['otyw','towy'],2646:['unts','tuns'],2647:['vuleor','louver'],2648:['inmsea','animes'],2649:['ulsetb','sublet'],2650:['ilgwedr','wergild'],2651:['inhgceo','echoing'],2652:['uptcesra','captures'],
2653:['inphsedo','sphenoid'],2654:['mktsoba','tombaks'],2655:['uligse','guiles'],2656:['lhseda','lashed'],2657:['lmtse','smelt'],2658:['ylinht','thinly'],2659:['inmpseo','impones'],2660:['ipcesdor','percoids'],2661:['uynpsek','punkeys'],2662:['inmdoa','daimon'],2663:['iphtcoa','aphotic'],2664:['inwgda','wading'],
2665:['tsex','sext'],2666:['lmwsdoa','wadmols'],2667:['uitcsor','citrous'],2668:['yilhdoa','holiday'],2669:['uqhto','quoth'],2670:['liedor','roiled'],2671:['uqseka','quakes'],2672:['fgeora','forage'],2673:['lgsda','glads'],2674:['sedor','redos'],2675:['wsca','caws'],2676:['inhgtk','knight'],
2677:['inhgso','hosing'],2678:['vsedora','savored'],2679:['iltcedkr','trickled'],2680:['umwtsoa','outswam'],2681:['gutl','glut'],2682:['uincs','incus'],2683:['hsera','shear'],2684:['lnedobra','banderol'],2685:['htedo','doeth'],2686:['inhcobra','bronchia'],2687:['uinedob','bedouin'],2688:['intcsor','citrons'],
2689:['inhce','niche'],2690:['ynphsedo','syphoned'],2691:['umkcbra','buckram'],2692:['nobra','baron'],2693:['inmphtce','pitchmen'],2694:['ptedobra','probated'],2695:['hcedra','arched'],2696:['ykel','yelk'],2697:['uintera','taurine'],2698:['uikhcsb','buckish'],2699:['ifgser','griefs'],2700:['uinser','inures'],
2701:['ulintca','lunatic'],2702:['ostl','lots'],2703:['vilwsedo','oldwives'],2704:['ihwsedk','whisked'],2705:['ynseoba','soybean'],2706:['itobr','orbit'],2707:['lkcedob','blocked'],2708:['inpseo','opines'],2709:['uqseor','roques'],2710:['pghra','graph'],2711:['yilngsa','slaying'],2712:['hwtsa','swath'],
2713:['ynmpeo','eponym'],2714:['ulintoa','outlain'],2715:['unpgwor','upgrown'],2716:['dlei','deil'],2717:['yuipwck','wickyup'],2718:['tfae','fate'],2719:['yngeob','bygone'],2720:['usebra','bursae'],2721:['uysedbr','rudesby'],2722:['brea','bare'],2723:['ulpsced','sculped'],2724:['uyiqnra','quinary'],
2725:['ingtsokr','stroking'],2726:['uincteso','counties'],2727:['uilqa','quail'],2728:['vhsi','shiv'],2729:['iosl','soli'],2730:['psra','rasp'],2731:['ugsobr','bourgs'],2732:['umpsd','dumps'],2733:['vulsea','values'],2734:['ulteska','auklets'],2735:['htera','earth'],2736:['inwgsdo','dowsing'],
2737:['vulingta','vaulting'],2738:['iwedr','wired'],2739:['litra','trial'],2740:['uifhwse','huswife'],2741:['ulpsedr','slurped'],2742:['inhgtcka','thacking'],2743:['pgol','glop'],2744:['ingseka','sinkage'],2745:['inmgtsea','steaming'],2746:['umhtesor','mouthers'],2747:['ulfpweor','powerful'],2748:['ynpeor','pyrone'],
2749:['inhtesra','inearths'],2750:['ygtsa','stagy'],2751:['fhtera','hafter'],2752:['lftesor','lofters'],2753:['tsem','stem'],2754:['ilmfseta','flamiest'],2755:['vulscoba','subvocal'],2756:['utsea','saute'],2757:['ilmkceb','limbeck'],2758:['ipsedra','praised'],2759:['hrei','hire'],2760:['ineobz','bizone'],
2761:['nmtesda','tandems'],2762:['ulntceo','noctule'],2763:['inmgtsor','storming'],2764:['mpceda','decamp'],2765:['imedr','mired'],2766:['uiqte','quite'],2767:['iceobra','aerobic'],2768:['ungsora','ourangs'],2769:['auhptcz','chutzpa'],2770:['nhtor','north'],2771:['ilnwtesk','twinkles'],2772:['ainhwgbz','whizbang'],
2773:['yitcskr','tricksy'],2774:['iksa','saki'],2775:['imstera','smartie'],2776:['ilnpsekr','plinkers'],2777:['lgseora','gaolers'],2778:['nhcedra','endarch'],2779:['htcesor','troches'],2780:['uimhdor','rhodium'],2781:['lfseka','flakes'],2782:['ilngtsoa','antilogs'],2783:['phka','kaph'],2784:['htcsra','charts'],
2785:['icbra','baric'],2786:['uptedo','pouted'],2787:['umfer','fumer'],2788:['limceba','alembic'],2789:['ylfhtes','thyself'],2790:['bnsok','knobs'],2791:['ywtsra','wastry'],2792:['ligeoa','goalie'],2793:['ihwpt','whipt'],2794:['iwedr','wider'],2795:['gwsok','gowks'],2796:['ukhcsba','chabuks'],
2797:['onci','cion'],2798:['agnl','lang'],2799:['ylmtba','tymbal'],2800:['fhtedor','frothed'],2801:['ylhtes','ethyls'],2802:['inpgcka','packing'],2803:['stcoa','tacos'],2804:['uintesbr','turbines'],2805:['nfpedora','profaned'],2806:['wteor','wrote'],2807:['ilfsetax','flaxiest'],2808:['lfgedo','golfed'],
2809:['umptera','tempura'],2810:['uimpsetb','bumpiest'],2811:['vuilnga','valuing'],2812:['lfsera','flares'],2813:['ilhcsa','laichs'],2814:['ilngser','lingers'],2815:['vinra','invar'],2816:['zscra','czars'],2817:['lingtera','alerting'],2818:['ungtora','outrang'],2819:['nwcesoba','cowbanes'],2820:['yimhtser','smithery'],
2821:['listedb','bilsted'],2822:['uilsced','sluiced'],2823:['ulkhedba','bulkhead'],2824:['ulinped','unpiled'],2825:['ilngca','lacing'],2826:['uncdob','bonduc'],2827:['vmseor','movers'],2828:['lmtera','armlet'],2829:['ysceto','coyest'],2830:['lnseoa','lanose'],2831:['infgcor','forcing'],2832:['hyea','yeah'],
2833:['aunl','luna'],2834:['uilng','lungi'],2835:['litesda','dilates'],2836:['ilnwsedr','swindler'],2837:['irla','rail'],2838:['linda','nidal'],2839:['hwces','chews'],2840:['stma','mats'],2841:['tmae','tame'],2842:['punk','punk'],2843:['lintedoa','delation'],2844:['uebax','beaux'],
2845:['intesd','teinds'],2846:['lipseora','polarise'],2847:['lncka','clank'],2848:['ynwbra','brawny'],2849:['ipedorx','peroxid'],2850:['ifhtc','fitch'],2851:['linmgedo','modeling'],2852:['vipsera','paviser'],2853:['yfekra','fakery'],2854:['ilmhcoa','mochila'],2855:['infkcba','finback'],2856:['uiqctsa','acquits'],
2857:['vihsora','haviors'],2858:['ilfhsok','folkish'],2859:['inmgta','taming'],2860:['ntcesra','trances'],2861:['incedk','nicked'],2862:['fwtesor','twofers'],2863:['unmha','human'],2864:['ifhgt','fight'],2865:['igtedr','girted'],2866:['inmpgcra','cramping'],2867:['pedor','pedro'],2868:['mcesbra','crambes'],
2869:['linmgeda','maligned'],2870:['inhgcok','choking'],2871:['imced','medic'],2872:['intera','retain'],2873:['ipsctera','crispate'],2874:['phceora','poacher'],2875:['iptsor','tripos'],2876:['ulinstea','insulate'],2877:['uhjse','jehus'],2878:['iwtesdra','tawdries'],2879:['uingtcor','courting'],2880:['nkea','kane'],
2881:['imtsedor','mortised'],2882:['lptse','slept'],2883:['unmtsca','sanctum'],2884:['ulinpta','unplait'],2885:['ilnpceda','panicled'],2886:['yilnska','snakily'],2887:['vntedra','verdant'],2888:['uipsb','pubis'],2889:['oscy','coys'],2890:['azel','laze'],2891:['vuwor','vrouw'],2892:['nwseda','snawed'],
2893:['nsedka','snaked'],2894:['ihsera','ashier'],2895:['unpgwor','grownup'],2896:['ihja','haji'],2897:['inmwge','mewing'],2898:['fscea','faces'],2899:['yihpcr','chirpy'],2900:['ifmpedor','pediform'],2901:['ylimtr','trimly'],2902:['unokra','koruna'],2903:['uljser','jurels'],2904:['lhwtesor','whortles'],
2905:['inmgcok','mocking'],2906:['dgsi','gids'],2907:['ylctera','treacly'],2908:['unwsedo','unsowed'],2909:['yilgra','glairy'],2910:['ilngcsdo','lingcods'],2911:['vlied','devil'],2912:['ymeobr','embryo'],2913:['ylitk','kilty'],2914:['cedra','raced'],2915:['lpsedor','presold'],2916:['ylctda','dactyl'],
2917:['uilner','lunier'],2918:['igsdr','girds'],2919:['ulcedob','becloud'],2920:['umwtcor','cutworm'],2921:['inser','serin'],2922:['ilhgst','slight'],2923:['yimftor','mortify'],2924:['ynmcsora','acronyms'],2925:['fwsdra','dwarfs'],2926:['inmwseor','winsomer'],2927:['ulpedba','dupable'],2928:['yinpseta','epinasty'],
2929:['uyltcr','curtly'],2930:['uiqekra','quakier'],2931:['ihwtced','witched'],2932:['lhsoa','halos'],2933:['inmter','remint'],2934:['yilfgted','giftedly'],2935:['vmpeda','vamped'],2936:['ulmseoba','albumose'],2937:['hwpso','whops'],2938:['ugka','kagu'],2939:['lingcba','cabling'],2940:['intoba','obtain'],
2941:['uqscea','casque'],2942:['yilwax','waxily'],2943:['ytserx','xyster'],2944:['limteo','motile'],2945:['ulncseo','counsel'],2946:['lnhcdora','chaldron'],2947:['ilpeobr','preboil'],2948:['hung','hung'],2949:['cesoax','coaxes'],2950:['inmgsora','organism'],2951:['hwtcska','thwacks'],2952:['lihgteca','teiglach'],
2953:['ulintoba','ablution'],2954:['ucesr','ecrus'],2955:['hops','hops'],2956:['hwcedka','whacked'],2957:['ilnhgtsa','lathings'],2958:['inmgera','mangier'],2959:['lpseor','proles'],2960:['uqtesra','quartes'],2961:['mcsora','macros'],2962:['ylheo','hoyle'],2963:['lhcedoka','headlock'],2964:['ylncedo','condyle'],
2965:['licetdra','lacertid'],2966:['liteska','talkies'],2967:['inpteda','painted'],2968:['unwedr','undrew'],2969:['limeob','mobile'],2970:['lobra','lobar'],2971:['vuigteso','outgives'],2972:['viorz','vizor'],2973:['uilnst','sunlit'],2974:['lhtoa','altho'],2975:['dpma','damp'],2976:['imter','merit'],
2977:['uilqeobr','beliquor'],2978:['ilfte','flite'],2979:['wsetda','wadset'],2980:['ilnpgca','placing'],2981:['uhpsteda','dustheap'],2982:['ulinfeb','bluefin'],2983:['undkr','drunk'],2984:['nhseka','shaken'],2985:['ynedok','donkey'],2986:['reac','race'],2987:['untl','lunt'],2988:['ilter','liter'],
2989:['ylinfger','reflying'],2990:['hugs','hugs'],2991:['ihtedba','habited'],2992:['inkhgteb','beknight'],2993:['ikedb','biked'],2994:['infgse','feigns'],2995:['lieor','oriel'],2996:['uylmbr','rumbly'],2997:['ilnfger','flinger'],2998:['inpgtera','tapering'],2999:['unwseor','unswore'],3000:['lnwceob','beclown'],
3001:['ulintea','alunite'],3002:['imhska','hakims'],3003:['inmhcera','chairmen'],3004:['unweda','unawed'],3005:['frei','reif'],3006:['wyax','waxy'],3007:['uiqzntea','quantize'],3008:['ilnpgo','loping'],3009:['ulmtebr','tumbrel'],3010:['ylpeda','played'],3011:['uhtesora','outhears'],3012:['pnri','pirn'],
3013:['tsobra','tabors'],3014:['ingseor','signore'],3015:['hwsedoba','beshadow'],3016:['lfweda','flawed'],3017:['lnhpsera','shrapnel'],3018:['yilnsek','skyline'],3019:['unfsekr','funkers'],3020:['liptecor','petrolic'],3021:['idaq','qaid'],3022:['fwtera','wafter'],3023:['itsebr','bistre'],3024:['dwro','word'],
3025:['dgoa','dago'],3026:['infed','fined'],3027:['vkhsobra','boshvark'],3028:['hyte','they'],3029:['lpgsdoa','lapdogs'],3030:['limsera','realism'],3031:['inwgso','sowing'],3032:['uipgeor','pirogue'],3033:['ulnseda','unleads'],3034:['yilfwea','lifeway'],3035:['npteda','pentad'],3036:['ingera','regina'],
3037:['npwedra','predawn'],3038:['ulimf','filum'],3039:['imgtera','migrate'],3040:['ulwtoka','outwalk'],3041:['ailbrz','brazil'],3042:['ilsca','laics'],3043:['inpgso','pingos'],3044:['lphsera','spheral'],3045:['intesa','tineas'],3046:['nwtsor','strown'],3047:['inhca','china'],3048:['uilnctso','linocuts'],
3049:['linfmsoa','foilsman'],3050:['ukpcba','backup'],3051:['ncedra','dancer'],3052:['yncest','encyst'],3053:['vulheora','overhaul'],3054:['iptedo','podite'],3055:['lipst','spilt'],3056:['hpcea','chape'],3057:['dbsa','bads'],3058:['intseor','stonier'],3059:['ultce','culet'],3060:['uptedor','trouped'],
3061:['inhgtea','heating'],3062:['ulistedk','dustlike'],3063:['ihtsdo','dhotis'],3064:['ilnjeoba','joinable'],3065:['yifera','aerify'],3066:['ulfjsra','jarfuls'],3067:['imcea','amice'],3068:['hsora','hoars'],3069:['liscedk','sickled'],3070:['ipcetk','picket'],3071:['ungeda','augend'],3072:['ubfl','flub'],
3073:['lnfpsdoa','plafonds'],3074:['vylnceox','convexly'],3075:['unmjtka','muntjak'],3076:['intska','takins'],3077:['ulnpgse','plunges'],3078:['ilneo','olein'],3079:['uhtsor','rouths'],3080:['vinpceor','province'],3081:['nmseor','sermon'],3082:['ymtea','matey'],3083:['ympca','campy'],3084:['ingsedo','dingoes'],
3085:['vfedora','favored'],3086:['ylift','fitly'],3087:['ihjcska','hijacks'],3088:['incea','eniac'],3089:['lzcoa','colza'],3090:['lgceskra','grackles'],3091:['umgeor','morgue'],3092:['lised','deils'],3093:['mctsoba','combats'],3094:['ilstda','distal'],3095:['lizmedba','imblazed'],3096:['ingedr','girned'],
3097:['ntcora','contra'],3098:['uimtsra','atriums'],3099:['uinhgser','ushering'],3100:['lseax','axels'],3101:['vimser','verism'],3102:['ylipghtr','triglyph'],3103:['nsac','scan'],3104:['voel','vole'],3105:['lnseo','enols'],3106:['iljsora','jailors'],3107:['ligsedr','gilders'],3108:['gjsa','jags'],
3109:['ymbra','ambry'],3110:['ulmseo','oleums'],3111:['onse','eons'],3112:['ulimpsed','impulsed'],3113:['pcsora','copras'],3114:['imted','demit'],3115:['wsya','ways'],3116:['ngdoa','gonad'],3117:['nmhcea','manche'],3118:['nmeora','enamor'],3119:['uylmpr','rumply'],3120:['vilwgera','lawgiver'],
3121:['hpsera','shaper'],3122:['unhgteob','boughten'],3123:['ligseoa','goalies'],3124:['vulgsra','vulgars'],3125:['ynjcesoa','joyances'],3126:['inhgtba','bathing'],3127:['edorx','redox'],3128:['urea','urea'],3129:['wtea','twae'],3130:['lijweka','jawlike'],3131:['voel','levo'],3132:['usedk','dukes'],
3133:['imsda','maids'],3134:['yuipsra','pyurias'],3135:['inscedk','snicked'],3136:['yilstr','lyrist'],3137:['ihedr','hider'],3138:['yilnga','gainly'],3139:['yncsedoa','cyanosed'],3140:['ubyo','buoy'],3141:['uyntcer','century'],3142:['lnhtesoa','ethanols'],3143:['lhtca','latch'],3144:['uilngt','luting'],
3145:['litcsdra','triclads'],3146:['uigseob','bougies'],3147:['lfhsa','flash'],3148:['ylngcoa','aglycon'],3149:['wbso','swob'],3150:['yilhtsa','hastily'],3151:['ugseor','rouges'],3152:['yilng','lingy'],3153:['gwera','wager'],3154:['ulpdora','poulard'],3155:['uiqntea','antique'],3156:['ulnfhda','handful'],
3157:['nmhseora','menorahs'],3158:['ncetsra','recants'],3159:['uynwra','runway'],3160:['vgia','vagi'],3161:['gyua','yuga'],3162:['ulifteso','outflies'],3163:['ylinpgsa','splaying'],3164:['uilfpter','uplifter'],3165:['lnwcso','clowns'],3166:['lhctoa','chalot'],3167:['infera','infare'],3168:['intl','lint'],
3169:['umsedr','demurs'],3170:['ivel','live'],3171:['uimtecsa','autecism'],3172:['kcedba','backed'],3173:['uigtser','gustier'],3174:['ulcsor','clours'],3175:['iwstera','waister'],3176:['mscea','acmes'],3177:['ilnhgser','shingler'],3178:['yingcka','yacking'],3179:['msoba','sambo'],3180:['ilngtsa','slating'],
3181:['inscebra','brisance'],3182:['lpctora','caltrop'],3183:['vuntex','unvext'],3184:['dgon','dong'],3185:['unmstedo','mudstone'],3186:['oume','moue'],3187:['uyptsora','outprays'],3188:['gtora','argot'],3189:['uifgso','fugios'],3190:['wgtedora','waterdog'],3191:['yilnma','mainly'],3192:['ubrl','blur'],
3193:['lhcteoa','cholate'],3194:['vyilnsoa','synovial'],3195:['uhcebr','cherub'],3196:['ypdra','pardy'],3197:['pgtera','parget'],3198:['uingsora','arousing'],3199:['vpora','vapor'],3200:['linpgsek','skelping'],3201:['usml','slum'],3202:['gsera','sager'],3203:['lisedo','siloed'],3204:['ltseobr','bolster'],
3205:['isectobr','bisector'],3206:['htesor','throes'],3207:['mtsoa','stoma'],3208:['unta','tuna'],3209:['hseda','heads'],3210:['uhtco','touch'],3211:['ingcsedo','cognised'],3212:['uigseda','gaudies'],3213:['umfpr','frump'],3214:['tscekra','stacker'],3215:['gure','urge'],3216:['uliqt','quilt'],
3217:['gocl','clog'],3218:['nphcesa','pechans'],3219:['ihscera','cashier'],3220:['nhcesbra','branches'],3221:['vyilneba','enviably'],3222:['lihcekra','hacklier'],3223:['dhos','hods'],3224:['ylftso','softly'],3225:['inmfeor','fermion'],3226:['uhsba','subah'],3227:['pksi','kips'],3228:['ilgteoba','obligate'],
3229:['uimtso','ostium'],3230:['unpwto','uptown'],3231:['unsb','nubs'],3232:['ylfpsera','palfreys'],3233:['lheoa','haole'],3234:['iltsceor','coistrel'],3235:['inmcsoa','maniocs'],3236:['inwez','winze'],3237:['ulcetsd','dulcets'],3238:['ihptca','haptic'],3239:['iphseda','aphides'],3240:['yilkseb','beyliks'],
3241:['vtesra','traves'],3242:['lingtesa','gelatins'],3243:['yimcdo','cymoid'],3244:['vltesora','levators'],3245:['lmeba','melba'],3246:['ylptra','paltry'],3247:['mpcoa','campo'],3248:['vsebr','verbs'],3249:['yimht','thymi'],3250:['uinsex','unisex'],3251:['yingter','retying'],3252:['nbri','brin'],
3253:['alhsez','hazels'],3254:['lngse','glens'],3255:['wskra','warks'],3256:['uyigstor','rugosity'],3257:['inwed','wined'],3258:['pgea','gape'],3259:['isctda','dicast'],3260:['aygsoz','azygos'],3261:['ynmcdora','dormancy'],3262:['ucel','luce'],3263:['yfokr','forky'],3264:['ynib','inby'],
3265:['ainsz','nazis'],3266:['unseor','rouens'],3267:['untesr','tuners'],3268:['nmhceka','hackmen'],3269:['anhsekz','khazens'],3270:['yntsa','nasty'],3271:['vylteoa','ovately'],3272:['vufsora','favours'],3273:['hptcesra','chapters'],3274:['intscer','cistern'],3275:['inmcera','carmine'],3276:['ultces','culets'],
3277:['dpei','pied'],3278:['linwsek','winkles'],3279:['vyilnex','vixenly'],3280:['vuinpger','prevuing'],3281:['ingwsedo','widgeons'],3282:['wtsea','sweat'],3283:['yncra','carny'],3284:['inpseok','pinkoes'],3285:['ulncera','unclear'],3286:['ilctdora','dicrotal'],3287:['uyljeba','bluejay'],3288:['uledor','louder'],
3289:['lhdora','holard'],3290:['uitesbax','bauxites'],3291:['ocrw','crow'],3292:['untcseo','contuse'],3293:['yngeox','oxygen'],3294:['vngera','graven'],3295:['lingscdo','scolding'],3296:['linwed','windle'],3297:['ihgtsbr','brights'],3298:['ilgdora','goliard'],3299:['ilfsa','fails'],3300:['inmgtsoa','antismog'],
3301:['inkgsba','basking'],3302:['nmteso','montes'],3303:['linpseta','panelist'],3304:['unhcsk','chunks'],3305:['lhpcesa','chapels'],3306:['ulnfte','unfelt'],3307:['npsedka','spanked'],3308:['htesorax','thoraxes'],3309:['yilwtera','waterily'],3310:['cedra','cedar'],3311:['oubm','umbo'],3312:['aobl','bola'],
3313:['ilnmpsoa','lampions'],3314:['nmpseora','manropes'],3315:['lncsoax','claxons'],3316:['nhcesra','ranches'],3317:['ynmea','yamen'],3318:['limpghe','megilph'],3319:['ikel','like'],3320:['viptesr','privets'],3321:['ngtsera','strange'],3322:['asel','leas'],3323:['lingjer','jingler'],3324:['pwseor','powers'],
3325:['usta','utas'],3326:['wsera','sawer'],3327:['mhcedor','chromed'],3328:['ubts','buts'],3329:['vihtesr','thrives'],3330:['intedoba','obtained'],3331:['ifmctso','comfits'],3332:['nfgtesra','engrafts'],3333:['unphces','punches'],3334:['itcsdora','carotids'],3335:['thos','shot'],3336:['ngwta','twang'],
3337:['gsera','gears'],3338:['nkto','knot'],3339:['diel','deli'],3340:['ulskr','lurks'],3341:['htscra','starch'],3342:['ulmgedbr','grumbled'],3343:['gkaw','gawk'],3344:['ynpghor','gryphon'],3345:['uilnces','leucins'],3346:['uyilsdk','duskily'],3347:['ylitera','reality'],3348:['unhtesbr','burthens'],
3349:['lnhteba','benthal'],3350:['vpedor','proved'],3351:['lstca','talcs'],3352:['ruse','suer'],3353:['vupedora','vapoured'],3354:['ihtsba','habits'],3355:['imae','amie'],3356:['yilnpge','yelping'],3357:['ylmteso','motleys'],3358:['ulnebra','nebular'],3359:['nmtedor','mordent'],3360:['lmseda','lameds'],
3361:['mgser','germs'],3362:['vilnea','venial'],3363:['lhsedo','dholes'],3364:['umebr','umber'],3365:['ulwsa','wauls'],3366:['pwtse','swept'],3367:['limpscea','misplace'],3368:['uylhgso','sloughy'],3369:['ipser','spier'],3370:['wsokr','works'],3371:['ilnseora','ailerons'],3372:['inhser','shiner'],
3373:['uymsetkr','musketry'],3374:['ilmwsor','wormils'],3375:['nmedoa','moaned'],3376:['nsdobax','sandbox'],3377:['uiqhca','quaich'],3378:['liftesr','trifles'],3379:['lsecda','scaled'],3380:['upseb','pubes'],3381:['liteskr','kirtles'],3382:['uimscd','muscid'],3383:['dobn','bond'],3384:['ulger','gruel'],
3385:['wbra','braw'],3386:['dnfi','find'],3387:['vingse','givens'],3388:['lphea','aleph'],3389:['nkow','know'],3390:['ounm','muon'],3391:['inpsecdr','prescind'],3392:['yjcka','jacky'],3393:['lnstdoa','sandlot'],3394:['lngcora','clangor'],3395:['inpcseor','conspire'],3396:['uyqcetor','coquetry'],
3397:['yilhdra','hardily'],3398:['visecokr','oversick'],3399:['intcso','tonics'],3400:['lhseo','sheol'],3401:['ltcedka','talcked'],3402:['uiptsra','upstair'],3403:['dsmi','mids'],3404:['tseor','store'],3405:['pgsea','pages'],3406:['uipteor','poutier'],3407:['ynmsora','masonry'],3408:['uitcra','uratic'],
3409:['lnceora','corneal'],3410:['uinmgso','mousing'],3411:['ulncora','courlan'],3412:['ywsebra','bewrays'],3413:['unmcedob','uncombed'],3414:['lpsedoa','deposal'],3415:['ilhtsdo','doltish'],3416:['ulincesd','includes'],3417:['ulnra','lunar'],3418:['ulingtoz','touzling'],3419:['ylwso','yowls'],3420:['csobra','cobras'],
3421:['hgsi','sigh'],3422:['inwseo','winoes'],3423:['uintc','cutin'],3424:['isedoax','oxidase'],3425:['lftesoa','folates'],3426:['ligseb','bilges'],3427:['inteskra','keratins'],3428:['insdk','kinds'],3429:['pone','peon'],3430:['inpgseo','pigeons'],3431:['lgedo','ogled'],3432:['yftcora','factory'],
3433:['inmpora','rampion'],3434:['uilnmpg','lumping'],3435:['uilsekr','sulkier'],3436:['ipsetdo','deposit'],3437:['inhtscer','snitcher'],3438:['idra','raid'],3439:['inwseobr','brownies'],3440:['uyteskr','turkeys'],3441:['lmgjoa','logjam'],3442:['uintcsra','curtains'],3443:['pwera','pawer'],3444:['lihcesdo','cheloids'],
3445:['dunk','dunk'],3446:['iqfra','faqir'],3447:['lfhsera','flasher'],3448:['tsorax','storax'],3449:['mgseobra','embargos'],3450:['ulcda','ducal'],3451:['ifska','kaifs'],3452:['vlera','laver'],3453:['dwra','draw'],3454:['ihptecsa','hepatics'],3455:['yilpdo','ploidy'],3456:['icedr','cider'],
3457:['lmpeobr','problem'],3458:['imtesbr','timbres'],3459:['ulinpor','purloin'],3460:['uleobr','rouble'],3461:['useckr','sucker'],3462:['linmpgea','empaling'],3463:['yinmga','maying'],3464:['yilnpte','ineptly'],3465:['lntoa','tolan'],3466:['ihcedax','hexadic'],3467:['lingse','single'],3468:['ihwtes','whites'],
3469:['lnteoa','tolane'],3470:['uilnfce','funicle'],3471:['uilmhse','heliums'],3472:['ifserz','frizes'],3473:['hsora','horas'],3474:['ulsbr','slurb'],3475:['vnteda','advent'],3476:['ulhgbra','burghal'],3477:['ufjgedor','forjudge'],3478:['lnfmdora','landform'],3479:['vinda','divan'],3480:['unmgte','nutmeg'],
3481:['ptsea','septa'],3482:['uhtsco','scouth'],3483:['ilntedr','tendril'],3484:['vicet','civet'],3485:['vyitera','variety'],3486:['vyincera','vicenary'],3487:['unceobr','bouncer'],3488:['yuphts','typhus'],3489:['yultesor','elytrous'],3490:['inhsd','hinds'],3491:['mhpceda','champed'],3492:['itsbr','brits'],
3493:['uilftedo','outfield'],3494:['vigteora','ravigote'],3495:['vlei','evil'],3496:['ingtsk','tsking'],3497:['icetsdr','directs'],3498:['vweora','avower'],3499:['vliek','kevil'],3500:['ilhtor','liroth'],3501:['inpgkra','parking'],3502:['lpsoa','opals'],3503:['ledoba','albedo'],3504:['htesdra','threads'],
3505:['isetdra','aridest'],3506:['inwged','dewing'],3507:['lingcra','carling'],3508:['lnfpdoa','plafond'],3509:['ylnhc','lynch'],3510:['ulnhs','shuln'],3511:['nhsedor','dehorns'],3512:['uhtcesor','touchers'],3513:['lncetsa','lancets'],3514:['yntca','canty'],3515:['vliedora','overlaid'],3516:['stak','task'],
3517:['ncoba','banco'],3518:['pceso','copse'],3519:['atez','zeta'],3520:['unmsdo','mounds'],3521:['iwsed','wides'],3522:['infhc','finch'],3523:['inmpgtco','compting'],3524:['ulsed','slued'],3525:['lmeoa','amole'],3526:['ylhce','chyle'],3527:['yntoba','botany'],3528:['htesobax','hatboxes'],
3529:['uincbr','brucin'],3530:['ledox','loxed'],3531:['ulhgces','gulches'],3532:['yinpger','preying'],3533:['uilsedra','residual'],3534:['linmpgsa','sampling'],3535:['linftesa','inflates'],3536:['inmwseoa','womanise'],3537:['ipsctea','spicate'],3538:['uiqnts','quints'],3539:['untceor','trounce'],3540:['lzgera','glazer'],
3541:['lhceora','cholera'],3542:['umted','muted'],3543:['obsi','bios'],3544:['pscra','carps'],3545:['ynwtsera','sternway'],3546:['uingtcr','trucing'],3547:['icesdra','radices'],3548:['ylktsba','bytalks'],3549:['ilngob','globin'],3550:['iphsra','parish'],3551:['vati','vita'],3552:['inmter','minter'],
3553:['inmwgeo','meowing'],3554:['lsceor','closer'],3555:['ilhgsted','slighted'],3556:['ulmceta','calumet'],3557:['ysra','rays'],3558:['lhtera','thaler'],3559:['ulpseor','leprous'],3560:['ifhgtesr','fighters'],3561:['ylnkra','rankly'],3562:['uyltseor','urostyle'],3563:['pseca','scape'],3564:['insdobra','inboards'],
3565:['ilceora','cariole'],3566:['visdo','voids'],3567:['dgre','dreg'],3568:['nseok','kenos'],3569:['ylihcr','richly'],3570:['ytsea','yeast'],3571:['ilfebra','friable'],3572:['usedba','abused'],3573:['pseco','scope'],3574:['ncesk','necks'],3575:['vncetor','convert'],3576:['isdoa','adios'],
3577:['ilftes','flites'],3578:['uilnged','eluding'],3579:['ulmhebr','humbler'],3580:['ncedo','coden'],3581:['lmsebra','lambers'],3582:['ucsdor','durocs'],3583:['utsedo','ousted'],3584:['ingwo','owing'],3585:['uyiqnger','querying'],3586:['ljra','jarl'],3587:['umgter','tergum'],3588:['lincseo','inclose'],
3589:['uinmhgor','humoring'],3590:['ingtdra','trading'],3591:['ylnhptea','enthalpy'],3592:['ugedra','argued'],3593:['ulkcesbr','bucklers'],3594:['hcez','chez'],3595:['yobra','boyar'],3596:['cedbra','braced'],3597:['unpseka','unspeak'],3598:['ihgtsd','dights'],3599:['nhtcora','chantor'],3600:['intsra','strain'],
3601:['ulmtedo','moulted'],3602:['uiqst','quits'],3603:['uiqcdra','quadric'],3604:['vwseor','vowers'],3605:['lceskr','clerks'],3606:['lgeba','gable'],3607:['ynwto','towny'],3608:['unmedra','manured'],3609:['inwts','twins'],3610:['uimgsora','gouramis'],3611:['grea','rage'],3612:['uktesoba','outbakes'],
3613:['ntcera','canter'],3614:['vitser','strive'],3615:['unfsea','unsafe'],3616:['lnhsedra','handlers'],3617:['uinmtesr','unmiters'],3618:['hsdka','dhaks'],3619:['yiblskr','briskly'],3620:['edrax','raxed'],3621:['untes','tunes'],3622:['lwteso','towels'],3623:['uimpsr','primus'],3624:['vlceoa','alcove'],
3625:['khgcoba','hogback'],3626:['ilnmtser','minstrel'],3627:['ingtsca','casting'],3628:['linhpteo','tholepin'],3629:['ugsetd','degust'],3630:['wnea','wean'],3631:['ulgsebr','buglers'],3632:['ulpte','letup'],3633:['uilfcesr','lucifers'],3634:['inmhgwea','weighman'],3635:['ilpeda','elapid'],3636:['uipdbra','upbraid'],
3637:['lhtsoa','lotahs'],3638:['vlisea','silvae'],3639:['ilfsca','fiscal'],3640:['amhcorz','machzor'],3641:['uqseobra','baroques'],3642:['mhtceo','cometh'],3643:['usedor','douser'],3644:['tres','rest'],3645:['lpya','paly'],3646:['edobr','orbed'],3647:['ingtsco','gnostic'],3648:['mfedra','framed'],
3649:['yumcso','cymous'],3650:['yilnksob','linkboys'],3651:['mhtesor','thermos'],3652:['lgsedor','lodgers'],3653:['unmseba','sunbeam'],3654:['mgsora','orgasm'],3655:['ungcesa','cangues'],3656:['ulmtcs','mulcts'],3657:['unfmser','frenums'],3658:['lihtso','thiols'],3659:['vysta','vasty'],3660:['ulnsctoa','osculant'],
3661:['imptra','armpit'],3662:['oslw','slow'],3663:['nwsetobr','brownest'],3664:['utesb','tubes'],3665:['ingora','origan'],3666:['ihsek','sheik'],3667:['uptsedo','spouted'],3668:['ylsedo','yodles'],3669:['uinmcera','manicure'],3670:['mpteo','tempo'],3671:['vinwedor','overwind'],3672:['ulintesd','diluents'],
3673:['uyhgter','theurgy'],3674:['npwedra','prawned'],3675:['vupsora','vapours'],3676:['inpgseor','reposing'],3677:['linsedk','kindles'],3678:['lfsea','leafs'],3679:['ftcor','croft'],3680:['weobr','bower'],3681:['lscda','scald'],3682:['imwsoa','miaows'],3683:['uilsedba','audibles'],3684:['uhtecora','outreach'],
3685:['uipsetor','roupiest'],3686:['ypcetsdr','decrypts'],3687:['wsekra','wreaks'],3688:['vinsda','viands'],3689:['nwseob','besnow'],3690:['ulmdo','mould'],3691:['ilsted','listed'],3692:['iedra','deair'],3693:['lihce','chiel'],3694:['serax','raxes'],3695:['lhtco','cloth'],3696:['yilnhda','handily'],
3697:['uilnps','lupins'],3698:['nskra','karns'],3699:['uigsetda','gaudiest'],3700:['ilhsto','holist'],3701:['lsera','earls'],3702:['inmea','anime'],3703:['sedbra','beards'],3704:['insedor','ordines'],3705:['lnmera','almner'],3706:['ihced','chide'],3707:['uinctd','induct'],3708:['uilmsb','limbus'],
3709:['ltsce','celts'],3710:['uphtra','prutah'],3711:['pcesor','copers'],3712:['inhgkra','harking'],3713:['lwsdor','worlds'],3714:['nsera','saner'],3715:['wtera','tawer'],3716:['yiptcda','diptyca'],3717:['uimphtr','triumph'],3718:['lfedra','flared'],3719:['sdobra','boards'],3720:['lmsedba','bedlams'],
3721:['ubra','bura'],3722:['nfwtsora','fanworts'],3723:['ugcsk','gucks'],3724:['hcdor','chord'],3725:['uilmgsob','gumboils'],3726:['vseobr','bevors'],3727:['yilsedo','doylies'],3728:['uiltseb','subtile'],3729:['uinseor','urinose'],3730:['inmsto','monist'],3731:['fhtsa','shaft'],3732:['ndora','radon'],
3733:['lfwtokra','flatwork'],3734:['vlora','valor'],3735:['mpcra','cramp'],3736:['vuilea','eluvia'],3737:['ulpgera','graupel'],3738:['useobr','bourse'],3739:['yingco','coying'],3740:['uqtera','quatre'],3741:['viwse','views'],3742:['vingceor','covering'],3743:['lmtedo','molted'],3744:['yimpsoa','myopias'],
3745:['bcak','back'],3746:['vileo','olive'],3747:['uilsbra','burials'],3748:['umhts','musth'],3749:['lfpsedra','feldspar'],3750:['nhtcedo','notched'],3751:['imhtsra','thirams'],3752:['ultso','tolus'],3753:['ukhcsoba','chabouks'],3754:['ilmteor','motlier'],3755:['ilbra','libra'],3756:['yhtca','yacht'],
3757:['ltcseoa','talcose'],3758:['umcesora','racemous'],3759:['ylnpeo','poleyn'],3760:['linsoka','kaolins'],3761:['inmgsea','seaming'],3762:['ihgsra','garish'],3763:['ipedr','pried'],3764:['ubsm','bums'],3765:['ultsebr','bluster'],3766:['ylifsa','salify'],3767:['ibsedkr','brisked'],3768:['imseox','moxies'],
3769:['vultedoa','ovulated'],3770:['uinpda','unpaid'],3771:['igna','agin'],3772:['imhcsea','chamise'],3773:['ilnwgba','blawing'],3774:['iphsecra','aspheric'],3775:['nhjso','johns'],3776:['yihtsr','thyrsi'],3777:['yilpceto','epicotyl'],3778:['yedra','deray'],3779:['utsdr','durst'],3780:['lfea','alef'],
3781:['lwsobra','barlows'],3782:['yilctra','clarity'],3783:['vimsea','mavies'],3784:['ypeox','epoxy'],3785:['iseckr','sicker'],3786:['ihwtser','swither'],3787:['nseoz','zones'],3788:['ihcsor','orchis'],3789:['usdor','sudor'],3790:['visteda','vistaed'],3791:['tesobra','boaters'],3792:['ulmfra','fulmar'],
3793:['nmgseo','genoms'],3794:['yihcokr','hickory'],3795:['dysa','days'],3796:['lmpcera','clamper'],3797:['ngedra','danger'],3798:['inwedr','winder'],3799:['lmtsora','mortals'],3800:['ymcea','cymae'],3801:['impteco','metopic'],3802:['ilhgtces','glitches'],3803:['imtecsr','metrics'],3804:['vylfseor','flyovers'],
3805:['pysr','spry'],3806:['npdobra','proband'],3807:['ilfhgted','flighted'],3808:['uhsck','shuck'],3809:['inpedo','ponied'],3810:['turs','ruts'],3811:['posi','pois'],3812:['unmeka','unmake'],3813:['ilnpa','plain'],3814:['mphtesoa','apothems'],3815:['yimtesda','daytimes'],3816:['yulnhgsa','nylghaus'],
3817:['inmhso','monish'],3818:['fhtera','father'],3819:['pubs','pubs'],3820:['ilnkb','blink'],3821:['ulngseb','blunges'],3822:['inhwge','hewing'],3823:['yhptera','therapy'],3824:['imfeora','foamier'],3825:['lnsedo','lodens'],3826:['yihtdor','thyroid'],3827:['visera','varies'],3828:['ilgcera','glacier'],
3829:['inhtsk','thinks'],3830:['uyilptsd','stupidly'],3831:['vihcesra','archives'],3832:['nmscoka','sockman'],3833:['uqztra','quartz'],3834:['unhtcor','cothurn'],3835:['intsera','stainer'],3836:['itfl','flit'],3837:['lpcetsoa','polecats'],3838:['mgeobra','embargo'],3839:['inmhcora','harmonic'],3840:['npsok','knosp'],
3841:['ylntoba','notably'],3842:['nhwga','whang'],3843:['pcsor','corps'],3844:['pbel','pleb'],3845:['yingsedr','syringed'],3846:['ifgtesra','frigates'],3847:['ultceor','clouter'],3848:['ingeb','being'],3849:['uilnsra','urinals'],3850:['inhgeobr','neighbor'],3851:['lnfcsoa','flacons'],3852:['yilngobr','boringly'],
3853:['ulsecra','secular'],3854:['vyjsera','jarveys'],3855:['lntcesa','cantles'],3856:['uifcdo','fucoid'],3857:['ilnmged','melding'],3858:['vinsea','naives'],3859:['linedbra','bilander'],3860:['imseokr','irksome'],3861:['ilnpgte','pelting'],3862:['vlgeoa','lovage'],3863:['dpus','spud'],3864:['ihwsra','rawish'],
3865:['inmphsor','morphins'],3866:['ligtesb','giblets'],3867:['ylhtesox','ethoxyls'],3868:['mftesora','formates'],3869:['ptedor','ported'],3870:['tobs','stob'],3871:['icfl','flic'],3872:['ulipcera','peculiar'],3873:['lneka','ankle'],3874:['licdbra','baldric'],3875:['inmsez','mizens'],3876:['yngsa','yangs'],
3877:['uinptsr','turnips'],3878:['uledr','ruled'],3879:['ihwceskr','whickers'],3880:['ayugsoz','azygous'],3881:['vuilobra','biovular'],3882:['uhgco','cough'],3883:['unpgwsor','grownups'],3884:['yltera','realty'],3885:['ipcdora','parodic'],3886:['ulint','until'],3887:['dpos','pods'],3888:['yedbra','brayed'],
3889:['ihcesdr','chiders'],3890:['losi','soil'],3891:['ihcok','hoick'],3892:['uinptd','pundit'],3893:['dwea','awed'],3894:['ucestbr','becrust'],3895:['nwsekra','swanker'],3896:['ucrs','curs'],3897:['ylsedo','yodels'],3898:['ihtesbz','zibeths'],3899:['atrs','tsar'],3900:['lisdobra','labroids'],
3901:['lihwedr','whirled'],3902:['ulmgeoa','moulage'],3903:['uinmscto','miscount'],3904:['uintsra','nutrias'],3905:['unfdo','found'],3906:['ylpseor','leprosy'],3907:['uqhseda','quashed'],3908:['untbra','turban'],3909:['ntesa','etnas'],3910:['ulinmda','maudlin'],3911:['inwgebr','brewing'],3912:['inmeo','monie'],
3913:['vyilneob','bovinely'],3914:['ulipsedo','euploids'],3915:['ulmhseoa','hamulose'],3916:['ulmteor','moulter'],3917:['ypwedor','powdery'],3918:['ilnmpoa','lampion'],3919:['lnwcedo','clowned'],3920:['ukceobr','roebuck'],3921:['yipsr','spiry'],3922:['yinhga','haying'],3923:['uylnho','unholy'],3924:['imgsera','mirages'],
3925:['ihwtces','witches'],3926:['ylnhgte','thegnly'],3927:['dhsa','dash'],3928:['vilhse','elvish'],3929:['ftseor','softer'],3930:['drta','dart'],3931:['lsera','lears'],3932:['uliphste','sulphite'],3933:['nmhsoa','hansom'],3934:['vuilteso','outlives'],3935:['kcmi','mick'],3936:['ungsoa','guanos'],
3937:['npwsora','pawnors'],3938:['fhtes','hefts'],3939:['ihtedra','airthed'],3940:['ilnekra','lankier'],3941:['ulnhc','lunch'],3942:['uyteax','eutaxy'],3943:['phta','path'],3944:['linmpcso','complins'],3945:['limgsea','milages'],3946:['lmedo','model'],3947:['tsea','sate'],3948:['mgsea','games'],
3949:['lseka','kales'],3950:['gsoa','sago'],3951:['imcra','micra'],3952:['isedba','abides'],3953:['edbra','ardeb'],3954:['vylebra','bravely'],3955:['ligteb','giblet'],3956:['uilntbra','tribunal'],3957:['imhsdra','dirhams'],3958:['lnfedor','fondler'],3959:['uylfg','gulfy'],3960:['yilcera','clayier'],
3961:['iphsca','phasic'],3962:['uyligt','guilty'],3963:['uyilfg','uglify'],3964:['brei','bier'],3965:['mjora','major'],3966:['mpsor','romps'],3967:['ulinceba','baculine'],3968:['inmekra','ramekin'],3969:['ifhgtedr','frighted'],3970:['lsdora','dorsal'],3971:['yisedob','disobey'],3972:['tcesora','coaters'],
3973:['lifseob','foibles'],3974:['linea','alien'],3975:['inptcoa','paction'],3976:['gteora','garote'],3977:['lhtesobr','brothels'],3978:['ulkedba','baulked'],3979:['linmebr','nimbler'],3980:['vitsobra','vibratos'],3981:['uphso','ouphs'],3982:['vulncseo','convulse'],3983:['ilporx','prolix'],3984:['ihpsc','chips'],
3985:['lnmpseoa','neoplasm'],3986:['lnptea','planet'],3987:['dmae','dame'],3988:['yilngc','glycin'],3989:['yipse','yipes'],3990:['pnsa','pans'],3991:['mwbo','womb'],3992:['iptera','pirate'],3993:['yilzwdra','wizardly'],3994:['linfgta','fatling'],3995:['utcesa','acutes'],3996:['lihsera','shalier'],
3997:['nseorz','zoners'],3998:['kgseobra','brokages'],3999:['mjeba','jambe'],4000:['tceso','coset'],4001:['uinmgtra','maturing'],4002:['uinpt','input'],4003:['inmsetca','amnestic'],4004:['uilnteso','elutions'],4005:['lfgsa','flags'],4006:['tseda','stade'],4007:['inwsekra','swankier'],4008:['ftsor','frost'],
4009:['uylgsd','sludgy'],4010:['dpse','peds'],4011:['dnei','nide'],4012:['liphseor','repolish'],4013:['ulteskz','klutzes'],4014:['nmdoa','monad'],4015:['inpteor','protein'],4016:['uilnek','unlike'],4017:['mfae','fame'],4018:['uyldor','dourly'],4019:['wseor','worse'],4020:['isdbr','dribs'],
4021:['uinpgor','pouring'],4022:['ufze','fuze'],4023:['ylpcesa','cypsela'],4024:['ihsoa','ohias'],4025:['ingcsra','racings'],4026:['uiftsora','faitours'],4027:['vlsea','valse'],4028:['ipsedra','despair'],4029:['upsedr','pursed'],4030:['vlsea','vales'],4031:['mpsetda','dampest'],4032:['linhwcso','clownish'],
4033:['limsta','smalti'],4034:['ulmebr','lumber'],4035:['inmeoa','anomie'],4036:['ipul','puli'],4037:['lncsok','clonks'],4038:['seckra','screak'],4039:['ilphsoba','basophil'],4040:['ilngtea','elating'],4041:['uimeobra','aerobium'],4042:['ulcedka','caulked'],4043:['orma','mora'],4044:['linsdra','aldrins'],
4045:['obsa','boas'],4046:['uitdob','outbid'],4047:['mhseca','schema'],4048:['uinmer','murein'],4049:['yintsk','stinky'],4050:['dhei','hide'],4051:['ilgseob','obliges'],4052:['inteox','toxine'],4053:['ltseoa','solate'],4054:['ylpera','parley'],4055:['ynpgeor','pyrogen'],4056:['yigtcoz','zygotic'],
4057:['ihtcesd','ditches'],4058:['intesoa','atonies'],4059:['ilnsea','lianes'],4060:['yinmedra','dairymen'],4061:['mfsea','fames'],4062:['yntoa','atony'],4063:['liteoka','keitloa'],4064:['wnso','wons'],4065:['uyneok','unyoke'],4066:['vnsedo','devons'],4067:['yifcedor','recodify'],4068:['lingcoka','cloaking'],
4069:['ilmpcesr','crimples'],4070:['inhstba','absinth'],4071:['yfgseo','fogeys'],4072:['untceda','unacted'],4073:['vrea','aver'],4074:['unfed','unfed'],4075:['lrfa','farl'],4076:['nfcedor','cornfed'],4077:['itecsox','exotics'],4078:['lhscok','shlock'],4079:['ihtec','ethic'],4080:['vusera','suaver'],
4081:['untcesra','centaurs'],4082:['uhcsedor','chorused'],4083:['insbr','brins'],4084:['lwedo','lowed'],4085:['ylmedkra','markedly'],4086:['limpge','megilp'],4087:['uyger','guyer'],4088:['limsetd','mildest'],4089:['uncsea','uncase'],4090:['imhsera','mishear'],4091:['inmgedra','margined'],4092:['inpstra','spirant'],
4093:['yhpso','hypos'],4094:['uqnhce','quench'],4095:['umhtcora','outcharm'],4096:['lingtsba','stabling'],4097:['licsob','cibols'],4098:['vulinsoa','avulsion'],4099:['lmsoa','loams'],4100:['ylinpgsa','palsying'],4101:['tsea','seat'],4102:['wscra','craws'],4103:['infeobr','bonfire'],4104:['unhtser','shunter'],
4105:['vael','vela'],4106:['lnfcoa','flacon'],4107:['hynm','hymn'],4108:['yinfgr','frying'],4109:['isedob','bodies'],4110:['yhwseor','showery'],4111:['dbsa','dabs'],4112:['yilptsor','sportily'],4113:['ylgra','gyral'],4114:['iwtesda','dawties'],4115:['ntseora','senator'],4116:['osme','some'],
4117:['ihjsda','jihads'],4118:['anlk','lank'],4119:['ingcso','incogs'],4120:['thra','hart'],4121:['inphgcea','peaching'],4122:['impsctea','campsite'],4123:['ptedra','petard'],4124:['ilptso','pistol'],4125:['inpgto','toping'],4126:['ynmhse','hymens'],4127:['unhgteo','toughen'],4128:['inpter','pterin'],
4129:['sebra','bares'],4130:['imstedra','misrated'],4131:['nhtcer','trench'],4132:['unmseda','medusan'],4133:['vigseda','visaged'],4134:['npwscoa','snowcap'],4135:['unmjtcsa','muntjacs'],4136:['ailnhtez','zenithal'],4137:['lnmgdoa','mangold'],4138:['uhsba','habus'],4139:['intsera','anestri'],4140:['ifhstr','shrift'],
4141:['inhgsa','ashing'],4142:['instceda','distance'],4143:['ylgwor','growly'],4144:['ilpghts','plights'],4145:['ulncer','lucern'],4146:['sectok','socket'],4147:['itsora','satori'],4148:['lphtek','klepht'],4149:['lgoa','gaol'],4150:['vlheda','halved'],4151:['ylinsera','inlayers'],4152:['limwtokr','milkwort'],
4153:['ylgwoa','logway'],4154:['uigeob','bougie'],4155:['uiqcekr','quicker'],4156:['ihwtecb','bewitch'],4157:['yfedora','forayed'],4158:['ulnedbr','bundler'],4159:['itebra','barite'],4160:['nfseokra','forsaken'],4161:['ukcebr','bucker'],4162:['itedobr','orbited'],4163:['yimcsora','cramoisy'],4164:['inpekra','ranpike'],
4165:['yimwda','midway'],4166:['uijser','juries'],4167:['uipctesr','cuprites'],4168:['unmfsa','fanums'],4169:['inpse','peins'],4170:['ingjseo','jingoes'],4171:['hcerax','exarch'],4172:['iftse','feist'],4173:['fedox','foxed'],4174:['hora','hoar'],4175:['medra','derma'],4176:['uyhtoba','hautboy'],
4177:['uifgedr','figured'],4178:['inmwsea','manwise'],4179:['ufgtoa','fugato'],4180:['ynpgseor','pyrogens'],4181:['jseokr','jokers'],4182:['ngsdra','grands'],4183:['ihgtes','eights'],4184:['ledobr','bordel'],4185:['ulmps','lumps'],4186:['psca','pacs'],4187:['ilngsekr','erlkings'],4188:['lmseora','morales'],
4189:['imsedr','dimers'],4190:['uyingb','buying'],4191:['pceor','coper'],4192:['onse','nose'],4193:['infhseob','fishbone'],4194:['yleda','layed'],4195:['ingtdoa','doating'],4196:['ljceoa','cajole'],4197:['uintera','uranite'],4198:['uintecra','anuretic'],4199:['ilngseo','lingoes'],4200:['lnsra','snarl'],
4201:['kcesbra','backers'],4202:['iptcso','picots'],4203:['dwya','wady'],4204:['nwsedor','wonders'],4205:['lmgsora','glamors'],4206:['obye','obey'],4207:['ilncsk','clinks'],4208:['uifgser','figures'],4209:['infteda','fainted'],4210:['imgera','maigre'],4211:['ugsob','bogus'],4212:['ynsdo','synod'],
4213:['ultceor','coulter'],4214:['yugtora','grayout'],4215:['uqncesor','conquers'],4216:['yilfter','flytier'],4217:['intcora','carotin'],4218:['dsac','scad'],4219:['yihwt','withy'],4220:['ptedor','redtop'],4221:['ntedrax','dextran'],4222:['intsoba','bastion'],4223:['ulngtea','languet'],4224:['hgwtcdoa','dogwatch'],
4225:['vlinjsea','javelins'],4226:['inmtea','inmate'],4227:['ilntsra','ratlins'],4228:['nwsora','rowans'],4229:['vutedo','devout'],4230:['lnsedra','snarled'],4231:['vyilnedb','vendibly'],4232:['uinstbr','inburst'],4233:['nhgsa','sangh'],4234:['limceba','cembali'],4235:['heorax','hoaxer'],4236:['inmpgco','comping'],
4237:['ulfhtsa','hatfuls'],4238:['lcetsra','clarets'],4239:['orly','lory'],4240:['vnei','vine'],4241:['nhcebra','brechan'],4242:['hwsedo','showed'],4243:['uledobr','doubler'],4244:['ylmhedor','hydromel'],4245:['uihgedor','doughier'],4246:['mtceo','comte'],4247:['ypedr','perdy'],4248:['ulmpa','ampul'],
4249:['lncok','clonk'],4250:['mkceob','bemock'],4251:['dpel','pled'],4252:['ynphso','syphon'],4253:['infsekr','knifers'],4254:['ftel','left'],4255:['uinhgcr','ruching'],4256:['uynjeor','journey'],4257:['ylngwor','wrongly'],4258:['lhteda','lathed'],4259:['upsra','supra'],4260:['ungter','gurnet'],
4261:['imped','imped'],4262:['uints','suint'],4263:['awnl','lawn'],4264:['psedo','posed'],4265:['hrma','harm'],4266:['uylnfce','fluency'],4267:['ltesdra','dartles'],4268:['sedoka','soaked'],4269:['lmptera','templar'],4270:['uncteor','cornute'],4271:['ilnse','liens'],4272:['uilnha','inhaul'],
4273:['ulmhora','humoral'],4274:['ytre','tyre'],4275:['vinsex','vixens'],4276:['uingtor','outring'],4277:['lseka','slake'],4278:['nhcsora','archons'],4279:['linhgea','healing'],4280:['usma','amus'],4281:['onlw','lown'],4282:['ipstor','ripost'],4283:['ilncekr','crinkle'],4284:['lngcesoa','congeals'],
4285:['ulscek','suckle'],4286:['inteda','detain'],4287:['uscora','soucar'],4288:['oblw','bowl'],4289:['lteobr','bolter'],4290:['yimpseo','myopies'],4291:['ilfpeor','profile'],4292:['ygsetra','grayest'],4293:['uyltce','cutely'],4294:['cedox','codex'],4295:['limfs','films'],4296:['nwtser','strewn'],
4297:['vintedoa','donative'],4298:['vuilger','virgule'],4299:['linmgbra','marbling'],4300:['ilnmsea','menials'],4301:['inseax','xenias'],4302:['ilhser','hirsel'],4303:['stdra','drats'],4304:['ylser','lyres'],4305:['lifhska','khalifs'],4306:['iwser','weirs'],4307:['lmdoa','modal'],4308:['hsceokr','shocker'],
4309:['iwser','wiser'],4310:['ingcsbra','bracings'],4311:['iltekra','ratlike'],4312:['vulinger','veluring'],4313:['duel','duel'],4314:['inhsetda','handiest'],4315:['vyugeora','voyageur'],4316:['uintesr','uniters'],4317:['inhge','hinge'],4318:['uinksb','buskin'],4319:['lingtsoa','solating'],4320:['nmftora','formant'],
4321:['ingwsed','swinged'],4322:['tskra','karst'],4323:['ytseda','steady'],4324:['lngceoa','congeal'],4325:['yltcsra','crystal'],4326:['ntesb','bents'],4327:['ipedra','pardie'],4328:['inhteb','henbit'],4329:['uimtsbr','brutism'],4330:['ilnsk','links'],4331:['ltsba','blats'],4332:['inmwgsra','swarming'],
4333:['lpceoba','placebo'],4334:['lwea','wale'],4335:['mptso','stomp'],4336:['pcedra','redcap'],4337:['uinax','auxin'],4338:['jcetob','object'],4339:['ulmtesb','tumbles'],4340:['yinsetd','density'],4341:['vlinsea','alevins'],4342:['litceo','citole'],4343:['hsera','rheas'],4344:['ysdobra','byroads'],
4345:['bsea','base'],4346:['htedra','dearth'],4347:['ulpstea','pulsate'],4348:['ynmsdoa','dynamos'],4349:['lmsedor','remolds'],4350:['iwsebr','brewis'],4351:['injcetor','injector'],4352:['ilmcedax','climaxed'],4353:['ylimgca','myalgic'],4354:['inptesa','patines'],4355:['ulnfekr','flunker'],4356:['uingctd','ducting'],
4357:['ifpteor','piefort'],4358:['limpsera','impalers'],4359:['iftseo','softie'],4360:['vifer','fiver'],4361:['vintser','striven'],4362:['ypsta','patsy'],4363:['dnri','rind'],4364:['ulncda','unclad'],4365:['nmsedora','ransomed'],4366:['yintcor','tyronic'],4367:['lyra','aryl'],4368:['undob','bound'],
4369:['psera','reaps'],4370:['nhsor','horns'],4371:['lnmsdoa','dolmans'],4372:['hwsca','chaws'],4373:['nmgsea','gasmen'],4374:['dhsa','dahs'],4375:['tcesra','cartes'],4376:['ulmpghsa','galumphs'],4377:['lweob','bowel'],4378:['ywtdra','tawdry'],4379:['fsobr','forbs'],4380:['vylin','vinyl'],
4381:['inhgseda','headings'],4382:['lpedra','parled'],4383:['lebra','abler'],4384:['ilncora','clarion'],4385:['iltcra','citral'],4386:['ulnctsok','locknuts'],4387:['nmsedra','remands'],4388:['ylfcedor','forcedly'],4389:['wkoe','woke'],4390:['ilnpgso','sloping'],4391:['uilger','gluier'],4392:['ulneda','unlead'],
4393:['uyilhsk','huskily'],4394:['ylheo','holey'],4395:['liped','piled'],4396:['uqcska','quacks'],4397:['inhwscda','sandwich'],4398:['intco','ontic'],4399:['hwtcekra','thwacker'],4400:['ypherz','zephyr'],4401:['uingtba','tabuing'],4402:['igebr','giber'],4403:['ulmsctea','muscatel'],4404:['ulinmge','legumin'],
4405:['phteo','tophe'],4406:['ilnhgok','holking'],4407:['ngsba','bangs'],4408:['vinhsra','varnish'],4409:['uilnso','insoul'],4410:['vilpedra','deprival'],4411:['uhjpdor','jodhpur'],4412:['uigtra','guitar'],4413:['incesdk','dickens'],4414:['lijter','jilter'],4415:['ingseo','soigne'],4416:['ilcsdoba','cabildos'],
4417:['iznteora','notarize'],4418:['tors','orts'],4419:['lihptea','haplite'],4420:['uinhcso','cushion'],4421:['untcedka','untacked'],4422:['inmhpse','shipmen'],4423:['ykci','icky'],4424:['ilngser','slinger'],4425:['vihces','chives'],4426:['uimera','uremia'],4427:['uptcera','capture'],4428:['obny','bony'],
4429:['linsea','silane'],4430:['ngceto','cogent'],4431:['ilntceso','lections'],4432:['unkscba','sunback'],4433:['ytscok','stocky'],4434:['uylincra','uranylic'],4435:['iphda','aphid'],4436:['ngseora','onagers'],4437:['lpcetsa','placets'],4438:['uypor','roupy'],4439:['nrfe','fern'],4440:['hwtra','thraw'],
4441:['ynsek','ensky'],4442:['uylhgcea','gauchely'],4443:['insor','rosin'],4444:['ngtsa','gnats'],4445:['ntes','tens'],4446:['iwna','wain'],4447:['utebr','rebut'],4448:['nwtedoka','takedown'],4449:['vlier','viler'],4450:['nmedo','demon'],4451:['inhgsba','bashing'],4452:['uinmpgd','dumping'],
4453:['mscea','maces'],4454:['ljsdo','slojd'],4455:['ynwta','tawny'],4456:['uyfsb','fubsy'],4457:['unmtora','romaunt'],4458:['ihwsed','wished'],4459:['umtsda','datums'],4460:['uipcd','cupid'],4461:['uligsedr','sludgier'],4462:['nhcek','kench'],4463:['lyba','ably'],4464:['dofa','fado'],
4465:['uihgka','kiaugh'],4466:['iwste','wites'],4467:['nhtscera','snatcher'],4468:['uinpsor','inpours'],4469:['uinhgsk','husking'],4470:['ingta','giant'],4471:['lnseora','reloans'],4472:['utskra','kurtas'],4473:['unsebra','unbears'],4474:['inmedor','minored'],4475:['unmgeda','agendum'],4476:['otma','moat'],
4477:['hpci','chip'],4478:['infgekr','kerfing'],4479:['lnfmseok','menfolks'],4480:['absi','bias'],4481:['ulidb','build'],4482:['uimdo','odium'],4483:['ihcesdra','rachides'],4484:['hpcesa','cheaps'],4485:['yinfgsra','frayings'],4486:['izwdra','wizard'],4487:['ulzhcta','chalutz'],4488:['yntsora','aroynts'],
4489:['intedora','rationed'],4490:['yikweba','bikeway'],4491:['ybceokra','rockabye'],4492:['ulfpedr','purfled'],4493:['ulnsea','unseal'],4494:['ubsy','busy'],4495:['linpsea','alpines'],4496:['intca','antic'],4497:['nmpheo','phenom'],4498:['yilfekra','freakily'],4499:['tsra','rats'],4500:['ulingsck','suckling'],
4501:['ntcoa','canto'],4502:['lnmtesa','mantles'],4503:['ynmez','enzym'],4504:['vuigsor','vigours'],4505:['unti','unit'],4506:['lnmgsdoa','mangolds'],4507:['inhgtecr','retching'],4508:['lipha','phial'],4509:['ulhgso','slough'],4510:['uilfgra','figural'],4511:['linmpceo','compline'],4512:['nhteso','ethnos'],
4513:['uilmpcsb','upclimbs'],4514:['htcesa','cheats'],4515:['uhsebr','busher'],4516:['prex','prex'],4517:['impsteda','impasted'],4518:['ynhsea','hyenas'],4519:['ylnseka','alkynes'],4520:['scma','cams'],4521:['nmgtera','garment'],4522:['uynmsera','aneurysm'],4523:['uphtso','tophus'],4524:['iltscekr','stickler'],
4525:['instebra','banister'],4526:['linmkba','lambkin'],4527:['lseka','lakes'],4528:['ungcedra','ungraced'],4529:['ilsor','loris'],4530:['uyqcekra','quackery'],4531:['linmgse','mingles'],4532:['lwcesdor','clowders'],4533:['vimpsera','vampires'],4534:['iona','naoi'],4535:['yinwga','yawing'],4536:['ugedor','rogued'],
4537:['mseok','smoke'],4538:['isedor','dories'],4539:['pyta','paty'],4540:['nhseto','honest'],4541:['isedra','deairs'],4542:['utsedor','rousted'],4543:['limcea','malice'],4544:['ipsecr','spicer'],4545:['hwdokra','dorhawk'],4546:['uqtseor','questor'],4547:['ylnpgsa','spangly'],4548:['ilsdra','lairds'],
4549:['yingbra','braying'],4550:['uhtcesbr','butchers'],4551:['hcetsor','rochets'],4552:['ipcesdra','peracids'],4553:['ulmfsora','formulas'],4554:['wtsra','straw'],4555:['inmsea','inseam'],4556:['uywteora','routeway'],4557:['obrs','robs'],4558:['lfcesk','flecks'],4559:['ilmgse','glimes'],4560:['icetskr','rickets'],
4561:['vctora','cavort'],4562:['infgo','gonif'],4563:['nteob','beton'],4564:['tksi','skit'],4565:['viseora','ovaries'],4566:['unme','menu'],4567:['vmedo','moved'],4568:['sebra','saber'],4569:['ultbr','blurt'],4570:['unhgtsoa','hangouts'],4571:['lmgsoba','gambols'],4572:['hcska','hacks'],
4573:['lincka','calkin'],4574:['ifebr','fiber'],4575:['secdok','socked'],4576:['infhgter','frighten'],4577:['uitsor','suitor'],4578:['iftesax','fixates'],4579:['vuiqera','aquiver'],4580:['mscea','cames'],4581:['unkcsbra','runbacks'],4582:['ylimf','filmy'],4583:['uintcsdo','noctuids'],4584:['yledr','redly'],
4585:['lnseoa','anoles'],4586:['ifteobra','biforate'],4587:['yhebr','herby'],4588:['ulnmse','lumens'],4589:['ifmtsra','maftirs'],4590:['inpsedor','prisoned'],4591:['ilftsoax','foxtails'],4592:['yhpsra','sharpy'],4593:['ulngs','lungs'],4594:['ulncesra','lucarnes'],4595:['uilctdka','ducktail'],4596:['lncea','lance'],
4597:['hseor','shore'],4598:['ifhcte','fetich'],4599:['nmgtesoa','megatons'],4600:['ylhsa','shaly'],4601:['uymcbr','crumby'],4602:['uintesdr','intrudes'],4603:['ilnmteba','bailment'],4604:['imceskra','keramics'],4605:['tsra','star'],4606:['tesobrz','bortzes'],4607:['ulnhceoa','eulachon'],4608:['vuincedr','incurved'],
4609:['linfmea','inflame'],4610:['setdr','drest'],4611:['linmtera','tramline'],4612:['ulfhsta','hatsful'],4613:['dnte','tend'],4614:['dnte','dent'],4615:['yilcesta','clayiest'],4616:['pots','opts'],4617:['vyistra','varsity'],4618:['ptedora','readopt'],4619:['uintedr','turdine'],4620:['ukce','cuke'],
4621:['gush','sugh'],4622:['uncedka','uncaked'],4623:['tcesax','exacts'],4624:['imphsdor','dimorphs'],4625:['uymfpr','frumpy'],4626:['ulnedor','roundel'],4627:['linwga','waling'],4628:['wedora','redowa'],4629:['ipcetd','depict'],4630:['nwska','swank'],4631:['yzntsba','byzants'],4632:['wsora','sowar'],
4633:['pwsa','waps'],4634:['ultesob','boletus'],4635:['lmsebra','amblers'],4636:['uytcser','curtsey'],4637:['uiteda','dautie'],4638:['vulngedo','ungloved'],4639:['itsecr','steric'],4640:['pocs','cops'],4641:['wura','waur'],4642:['vinedokr','overkind'],4643:['lnmseo','solemn'],4644:['uylnteba','tuneably'],
4645:['unhgcera','uncharge'],4646:['ycesdo','decoys'],4647:['wnea','anew'],4648:['ulcedr','curdle'],4649:['linmsetb','nimblest'],4650:['vidoa','avoid'],4651:['nsedoa','anodes'],4652:['dnti','dint'],4653:['psetdob','bedpost'],4654:['uitsc','ictus'],4655:['lnmhteo','menthol'],4656:['limedo','moiled'],
4657:['uylhts','thusly'],4658:['ufhgtsra','fraughts'],4659:['nmhceta','manchet'],4660:['ulptesoa','outleaps'],4661:['zstra','tzars'],4662:['lmseda','medals'],4663:['lrea','real'],4664:['ylntsokr','klystron'],4665:['uilhtsob','holibuts'],4666:['yhtscra','starchy'],4667:['imger','grime'],4668:['uncsor','cornus'],
4669:['uylmhb','humbly'],4670:['uilfpted','uplifted'],4671:['upcsra','carpus'],4672:['uhtces','chutes'],4673:['ihpsera','harpies'],4674:['hoti','thio'],4675:['ulinmpgc','clumping'],4676:['unedbr','burden'],4677:['yilfhgt','flighty'],4678:['hwye','whey'],4679:['uymhtsc','smutchy'],4680:['ilhsta','latish'],
4681:['inhedo','hoiden'],4682:['cesdo','codes'],4683:['ulfsera','refusal'],4684:['ingsra','grains'],4685:['ucesbr','cubers'],4686:['uinmedra','muraenid'],4687:['dlea','deal'],4688:['umkgsecb','gemsbuck'],4689:['vlineora','overlain'],4690:['ipcetdr','predict'],4691:['uinpsdo','unipods'],4692:['iledok','keloid'],
4693:['ihgtor','righto'],4694:['ynpteco','potency'],4695:['uinfgsed','defusing'],4696:['linserax','relaxins'],4697:['vitcseo','costive'],4698:['nwtedora','danewort'],4699:['imhskra','kashmir'],4700:['wsera','wares'],4701:['ulhgco','clough'],4702:['uilngs','lungis'],4703:['lbmceoka','mockable'],4704:['uiqncesk','quickens'],
4705:['ifsetkr','frisket'],4706:['ipgsr','sprig'],4707:['ilptcera','particle'],4708:['yimsedok','misyoked'],4709:['vylnsa','sylvan'],4710:['lgtesora','gloaters'],4711:['liedob','boiled'],4712:['hsedax','hexads'],4713:['tesdb','debts'],4714:['lftesra','falters'],4715:['lipcesra','calipers'],4716:['hgtseoa','hostage'],
4717:['ingsoba','gabions'],4718:['ihtebz','zibeth'],4719:['inpgscra','scarping'],4720:['unpeobr','upborne'],4721:['yilnpcer','princely'],4722:['doea','odea'],4723:['linmftea','filament'],4724:['iphted','pithed'],4725:['vbre','verb'],4726:['utkra','kraut'],4727:['usti','tuis'],4728:['ylfer','flyer'],
4729:['ilmedo','meloid'],4730:['inhtcek','thicken'],4731:['untkr','trunk'],4732:['hwteda','thawed'],4733:['ulsedob','bloused'],4734:['lpgoa','galop'],4735:['fsetdba','bedfast'],4736:['uilfpts','uplifts'],4737:['lpjoa','jalop'],4738:['otrc','torc'],4739:['unmseb','busmen'],4740:['iftra','afrit'],
4741:['dbsi','bids'],4742:['ltedor','retold'],4743:['igsedbra','abridges'],4744:['ylsecdra','sacredly'],4745:['lfwteora','fleawort'],4746:['lfgtedoa','gatefold'],4747:['ulnhgced','glunched'],4748:['inphcer','phrenic'],4749:['uiqcesa','caiques'],4750:['vnsa','vans'],4751:['vuyntesd','duvetyns'],4752:['lseda','lased'],
4753:['uintscob','subtonic'],4754:['visek','skive'],4755:['yilhsda','shadily'],4756:['ymphtea','empathy'],4757:['mpwso','womps'],4758:['yingtsor','storying'],4759:['gurm','grum'],4760:['ulkwbra','bulwark'],4761:['hsebr','herbs'],4762:['uhtso','shout'],4763:['mhsea','hames'],4764:['lcesokr','lockers'],
4765:['nphteoa','phaeton'],4766:['umhbr','rhumb'],4767:['lwtsra','trawls'],4768:['imgsetob','misbegot'],4769:['lztesoa','zealots'],4770:['useca','sauce'],4771:['nbse','bens'],4772:['yhdra','hydra'],4773:['yulmgeda','amygdule'],4774:['yiltsbr','bristly'],4775:['ypjedora','jeopardy'],4776:['uiqer','quire'],
4777:['ltsea','least'],4778:['vuipsed','updives'],4779:['lwsbra','brawls'],4780:['ingeor','region'],4781:['ingtser','stinger'],4782:['ilfebax','fixable'],4783:['ubns','buns'],4784:['ulmsce','muscle'],4785:['yhwse','wheys'],4786:['uylneb','nebuly'],4787:['vinwga','waving'],4788:['dhna','hand'],
4789:['ipsoa','psoai'],4790:['lceoz','cloze'],4791:['itora','ratio'],4792:['pseka','speak'],4793:['ulsck','sculk'],4794:['ingcox','coxing'],4795:['vsebra','braves'],4796:['uincetdr','reinduct'],4797:['uihtceo','couthie'],4798:['gsdra','drags'],4799:['uitcer','curite'],4800:['imgcsa','magics'],
4801:['afel','leaf'],4802:['husl','shul'],4803:['ujtes','jutes'],4804:['inhcsa','chinas'],4805:['inwtesr','twiners'],4806:['ymsera','smeary'],4807:['imhcest','chemist'],4808:['ylisra','riyals'],4809:['ylnptora','patronly'],4810:['puse','spue'],4811:['ylfhse','fleshy'],4812:['lnpscea','spancel'],
4813:['inseba','sabine'],4814:['uintesda','audients'],4815:['ilpse','plies'],4816:['litedbr','driblet'],4817:['limcera','reclaim'],4818:['ulngtesa','languets'],4819:['uistra','aurist'],4820:['lsdba','balds'],4821:['ulwtedoa','outlawed'],4822:['lpsora','sporal'],4823:['uiqcsdra','quadrics'],4824:['ilhpseda','helipads'],
4825:['hpsedoax','hexapods'],4826:['ilnted','dentil'],4827:['inpseoa','senopia'],4828:['uyhgcor','grouchy'],4829:['ulngera','granule'],4830:['vyilhea','heavily'],4831:['ymher','rhyme'],4832:['mpscera','scamper'],4833:['inmhska','khamsin'],4834:['intcska','catkins'],4835:['fseox','foxes'],4836:['ilnhteso','neoliths'],
4837:['ufera','feuar'],4838:['mgebra','bregma'],4839:['ingsdbra','brigands'],4840:['gtedora','garoted'],4841:['ylnseoka','ankylose'],4842:['uilseor','lousier'],4843:['okcm','mock'],4844:['wseor','swore'],4845:['vinpgora','vaporing'],4846:['ailhtsoz','thiazols'],4847:['tsora','roast'],4848:['yihtsor','history'],
4849:['ftseor','foster'],4850:['ilmps','limps'],4851:['mhtceoba','hecatomb'],4852:['inmwgra','warming'],4853:['unmtedo','demount'],4854:['iphtcera','patchier'],4855:['uilmsedr','misruled'],4856:['izngedoa','agonized'],4857:['unsk','sunk'],4858:['uinjceor','jouncier'],4859:['gtseora','storage'],4860:['iltecsra','recitals'],
4861:['pyla','play'],4862:['vnedo','doven'],4863:['iwceor','cowrie'],4864:['uimhstb','bismuth'],4865:['htseo','shote'],4866:['obrs','orbs'],4867:['uhtec','teuch'],4868:['uyltsb','butyls'],4869:['ulimphcs','clumpish'],4870:['dres','reds'],4871:['lihcdor','chlorid'],4872:['mfeora','foamer'],
4873:['ingcekr','recking'],4874:['vilgeda','glaived'],4875:['nmgsdora','gormands'],4876:['unctsob','cobnuts'],4877:['rmie','rime'],4878:['unwtcsdo','cutdowns'],4879:['tsobra','aborts'],4880:['mpoe','poem'],4881:['nmsoa','mason'],4882:['uinfmor','uniform'],4883:['vilpce','pelvic'],4884:['htec','etch'],
4885:['fpsebra','prefabs'],4886:['hwpsa','whaps'],4887:['lheor','holer'],4888:['ngsedra','ganders'],4889:['vulngeo','unglove'],4890:['nmedra','remand'],4891:['hwedok','howked'],4892:['awbl','blaw'],4893:['ingeb','binge'],4894:['ungsdo','sundog'],4895:['vhsea','haves'],4896:['imphsera','seraphim'],
4897:['lpsea','lapse'],4898:['dutr','turd'],4899:['phcesra','eparchs'],4900:['aoel','olea'],4901:['lfeora','florae'],4902:['ilhgsa','laighs'],4903:['lhtcera','trachle'],4904:['gsorz','grosz'],4905:['ylmsetdo','modestly'],4906:['ifdobr','forbid'],4907:['limpgse','megilps'],4908:['ylfhtoa','hayloft'],
4909:['inba','bani'],4910:['ilfpceoa','epifocal'],4911:['uyntseda','unsteady'],4912:['uhgcedor','grouched'],4913:['inmpgtsa','stamping'],4914:['inteor','tonier'],4915:['yngseob','bygones'],4916:['setbra','breast'],4917:['inmceso','incomes'],4918:['grmi','grim'],4919:['lbheka','keblah'],4920:['mpgweora','gapeworm'],
4921:['lphteora','plethora'],4922:['ksab','kabs'],4923:['ulntesb','unbelts'],4924:['ipsedo','poised'],4925:['ipcekax','pickaxe'],4926:['untsedor','tonsured'],4927:['uiqhcska','quackish'],4928:['ilnpsekr','sprinkle'],4929:['uhsedo','housed'],4930:['nfeka','kenaf'],4931:['inpgeka','peaking'],4932:['usctba','sacbut'],
4933:['yrfa','fray'],4934:['lifhka','khalif'],4935:['ihcsk','hicks'],4936:['linhwgsa','shawling'],4937:['liobr','broil'],4938:['lmseda','damsel'],4939:['ulifeba','fibulae'],4940:['tusc','scut'],4941:['ineax','xenia'],4942:['utseob','obtuse'],4943:['geobrax','gearbox'],4944:['pcei','epic'],
4945:['jole','jole'],4946:['inwgdra','drawing'],4947:['ynak','yank'],4948:['vimtebra','ambivert'],4949:['iqntsra','qintars'],4950:['uylmgs','smugly'],4951:['edobr','bored'],4952:['dosa','soda'],4953:['ilngseba','singable'],4954:['dpuo','updo'],4955:['lhwseo','wholes'],4956:['yifgsa','gasify'],
4957:['uilnma','lumina'],4958:['incetba','cabinet'],4959:['uinsed','nudies'],4960:['vylier','verily'],4961:['ilncedk','clinked'],4962:['ulftser','fluster'],4963:['ulfwa','awful'],4964:['ihcesdr','herdics'],4965:['mgue','geum'],4966:['ulnmpcsa','unclamps'],4967:['ilmeda','medial'],4968:['ukctsoba','backouts'],
4969:['ylnrax','larynx'],4970:['ngedora','groaned'],4971:['ptsea','paste'],4972:['upedor','rouped'],4973:['umhsobr','rhombus'],4974:['ulnmcba','clubman'],4975:['ylinha','hyalin'],4976:['ihgsekr','skreigh'],4977:['ilnmfgoa','flamingo'],4978:['istex','exits'],4979:['upsedkr','predusk'],4980:['inhgceor','ochering'],
4981:['uhpcsba','hubcaps'],4982:['seax','axes'],4983:['yhtsced','scythed'],4984:['vlgeor','glover'],4985:['impsecra','sapremic'],4986:['lingteax','exalting'],4987:['gtesora','orgeats'],4988:['gcay','cagy'],4989:['ynstda','dynast'],4990:['upsetr','purest'],4991:['uimpsetd','dumpiest'],4992:['uinpgor','rouping'],
4993:['imtsea','misate'],4994:['nwedra','wander'],4995:['ngseora','oranges'],4996:['ylnob','nobly'],4997:['limkteob','tomblike'],4998:['lihseda','halides'],4999:['lfteoa','foetal'],5000:['uimhsdor','humidors']}
    canvas=Canvas(root,height=600,width=600,bg="AntiqueWhite1")
    canvas.pack()
    my_font = Font(family="Bauhaus 93", size=28,weight="bold",underline=1)
    myfont = Font(family="Courier New CE", size=15)
    myfon = Font(family="Arial Black", size=18,weight="bold")
    def closerules():
        global rulesframe
        rulesframe.destroy()
        root.bind("<Key>",ruleskey)
    def submitt(event):
        global proceed
        global que
        global frame1
        global l1
        global ys
        global bs
        global bestscore
        global curscore
        global frame3
        if proceed==1:
            user=en.get()
            if user==d[que][1]:
                ys+=1
                if ys>bs:
                    bs=ys
                bestscore.place_forget()
                curscore.place_forget()
                bestscore=Label(canvas,text="Best Score: "+str(bs),bg="PaleTurquoise1",font="impact 16",fg="dark violet")
                bestscore.place(relx=0.02,rely=0.02,relwidth=0.31,relheight=0.05)

                curscore=Label(canvas,text="Your Score: "+str(ys),bg="PaleTurquoise1",font="impact 16",fg="dark violet")
                curscore.place(relx=0.67,rely=0.02,relwidth=0.31,relheight=0.05)
        
                que+=1
                correct=Label(frame3,text="YAYY!!\nCORRECT!!!",font="impact 28 bold",bg="cornflower blue",fg="green")
                correct.place(relx=0.24,rely=0.6)
                correct.after(3000,lambda: correct.destroy())
                l1.place_forget()
                displaytext=d[que][0]
                l1=Label(frame1,text=displaytext,font="Courier 26 bold",bg="white",fg="red")
                l1.place(relheight=1,relwidth=0.65)
                en.delete(0,END)
                conn=sqlite3.connect(".img\\Guesstheword.db")
                c=conn.cursor()
                c.execute("""UPDATE Player_Info SET
                          question = :un
                          WHERE oid = :num""",
                          {"un":que,
                           "num":1
                           }
                              )
                conn.commit()
                conn.close()
            else:
                wrong=Label(frame3,text="OOPS!!\nWRONG ANSWER!",font="impact 25 bold",bg="cornflower blue",fg="firebrick1")
                wrong.place(relx=0.14,rely=0.55)
                wrong.after(3000,lambda: wrong.destroy())
                
                

                
                
    def nextt(event):
        global proceed
        global que
        global frame1
        global l1
        if proceed==1:
            if que==5000:
                que=1
            else:
                que+=1
            l1.place_forget()
            displaytext=d[que][0]
            l1=Label(frame1,text=displaytext,font="Courier 26 bold",bg="white",fg="red")
            l1.place(relheight=1,relwidth=0.65)
            conn=sqlite3.connect(".img\\Guesstheword.db")
            c=conn.cursor()
            c.execute("""UPDATE Player_Info SET
                          question = :un
                          WHERE oid = :num""",
                          {"un":que,
                           "num":1
                           }
                              )
            conn.commit()
            conn.close()
    def ruleskey(event):
        global proceed
        if proceed==1 and event.char=="5":
            root.unbind("<Key>")
            global rulesframe
            rulesframe=Frame(canvas,bg="deep pink",bd=5)
            rulesframe.place(x=0,y=0,relheight=1,relwidth=1)
            
            rulesframe2=Frame(rulesframe,bg="pink")
            rulesframe2.place(relwidth=1,relheight=1)
            
            heading=Label(rulesframe2,text="HOW TO PLAY?",font=my_font,bg="pink",fg="snow")
            heading.place(relx=0.25)
            st="""Hi!
1)The Game is simple,Once You enter username your
game will start.
2)You are Given with a jumbled text you need to
type the correct word by rearranging them and
      submit the answer.                     
3)If you dont know the answer you can press NEXT
button to get the next Jumbled word.
4)For Every Correct Answer you will be awarded
with 1 point.
5)You can end the Game whenever You want to by
pressing End Game button
6)After pressing END GAME your score will be reset
to 0.
7)You can see top 10 High scorers by clicking the
view points table button
8)For Offline players best score will always reset
to 0 when the application is started!
9)Be in the top 10 so that anyone in the world
playing this can see your name on the table!
***Words may have multiple answer but only one
of them will be correct..keep trying for that
tough one***"""
            description=Label(rulesframe2,text=st,font=myfont,bg="pink")
            description.place(relx=0.01,rely=0.1)
            closebutton=Button(rulesframe2,text="Back",font=myfon,bg="red",fg="white",command=closerules)
            closebutton.place(relx=0.8)

    def rulesbutton():
        if(1==1):
            root.unbind("<Key>")
            global rulesframe
            rulesframe=Frame(canvas,bg="deep pink",bd=5)
            rulesframe.place(x=0,y=0,relheight=1,relwidth=1)
            
            rulesframe2=Frame(rulesframe,bg="pink")
            rulesframe2.place(relwidth=1,relheight=1)
            
            heading=Label(rulesframe2,text="HOW TO PLAY?",font=my_font,bg="pink",fg="snow")
            heading.place(relx=0.25)
            st="""Hi!
1)The Game is simple,Once You enter username your
game will start.
2)You are Given with a jumbled text you need to
type the correct word by rearranging them and
      submit the answer.                     
3)If you dont know the answer you can press NEXT
button to get the next Jumbled word.
4)For Every Correct Answer you will be awarded
with 1 point.
5)You can end the Game whenever You want to by
pressing End Game button
6)After pressing END GAME your score will be reset
to 0.
7)You can see top 10 High scorers by clicking the
view points table button
8)For Offline players best score will always reset
to 0 when the application is started!
9)Be in the top 10 so that anyone in the world
playing this can see your name on the table!
***Words may have multiple answer but only one
of them will be correct..keep trying for that
tough one***"""
            description=Label(rulesframe2,text=st,font=myfont,bg="pink")
            description.place(relx=0.01,rely=0.1)
            closebutton=Button(rulesframe2,text="Back",font=myfon,bg="red",fg="white",command=closerules)
            closebutton.place(relx=0.8)

    def endgamee():
        global ys
        global l1
        global curscore
        global que
        ys=0
        curscore.place_forget()
        curscore=Label(canvas,text="Your Score: "+str(ys),bg="PaleTurquoise1",font="impact 16",fg="dark violet")
        curscore.place(relx=0.67,rely=0.02,relwidth=0.31,relheight=0.05)
        que=1
        l1.place_forget()
        displaytext=d[que][0]
        l1=Label(frame1,text=displaytext,font="Courier 26 bold",bg="white",fg="red")
        l1.place(relheight=1,relwidth=0.65)
        conn=sqlite3.connect(".img\\Guesstheword.db")
        c=conn.cursor()
        c.execute("""UPDATE Player_Info SET
                          question = :un
                          WHERE oid = :num""",
                          {"un":que,
                           "num":1
                           }
                              )
        conn.commit()
        conn.close()        
        en.delete(0,END)
    def startt(event):
        global startpage
        global proceed
        global Log
        if proceed==0:
                proceed=1
                root.bind("<Return>",submitt)
                startpage.place_forget()

    try:
        i1=ImageTk.PhotoImage(Image.open(".img\\GTW.jpg"))
        backg=Label(canvas,image=i1)
        backg.pack()
    except Exception:
        doc=0
        messagebox.showerror("File Missing!","One of our files are Missing!\nPlease Download again!")
        root.destroy()
    if doc==1:                   
        bestscore=Label(canvas,text="Best Score: 00000",bg="PaleTurquoise1",font="impact 16",fg="dark violet")
        bestscore.place(relx=0.02,rely=0.02,relwidth=0.31,relheight=0.05)

        curscore=Label(canvas,text="Your Score: 00000",bg="PaleTurquoise1",font="impact 16",fg="dark violet")
        curscore.place(relx=0.67,rely=0.02,relwidth=0.31,relheight=0.05)

        frame1=Frame(canvas,bg="cadet blue",bd=5)
        frame1.place(relx=0.23,rely=0.1,relwidth=0.6,relheight=0.1)
        
        displaytext=d[que][0]
        l1=Label(frame1,text=displaytext,font="Courier 26 bold",bg="white",fg="red")
        l1.place(relheight=1,relwidth=0.65)

        nex=Button(frame1,text="NEXT",bg="steelblue1",font="Helvetica 16 bold",fg="red3",command=lambda: nextt(1))
        nex.place(relx=0.67,relwidth=0.33,relheight=1)
        root.bind("<Right>",nextt)

        frame2=Frame(canvas,bg="cyan3")
        frame2.place(relx=0.23,rely=0.25,relwidth=0.6,relheight=0.05)

        l2=Label(frame2,text="Type Your Answer",font="verdana 16 bold",bg="cyan3",fg="maroon4")
        l2.place(relheight=1,relwidth=1)

        frame3=Frame(canvas,bg="cornflower blue",bd=5)
        frame3.place(relx=0.23,rely=0.32,relwidth=0.6,relheight=0.5)

        en=Entry(frame3,font="Helvetica 16")
        en.insert(0,"Type Here...")
        en.place(x=0,y=0,relwidth=1,relheight=0.3)

        submit=Button(frame3,text="Submit Answer",bg="wheat1",font="Helvetica 16 bold",fg="red3",command=lambda: submitt(1))
        submit.place(relx=0.5,rely=0.35)
        root.bind("<Return>",submitt)

        endgame=Button(canvas,bg="LightSkyBlue3",text="E N D   G A M E",font="impact 22",fg="red3",command=endgamee)
        endgame.place(relx=0.23,rely=0.85,relheight=0.1,relwidth=0.6)

        rules=Button(canvas,text="HOW \nTO \nPLAY\n?",bg="black",fg="white",font="verdana 12 bold",command=rulesbutton)
        rules.place(relx=0.85,rely=0.65,relheight=0.25,relwidth=0.14)
        root.bind("<Key>",ruleskey)

        keynote=Label(canvas,text="Press \n'5'\n for \nhelp",font="impact 16 ",fg="white",bg="gold")
        keynote.place(relx=0.85,rely=0.45,relwidth=0.135)

        offline=Label(canvas,text="You are\nPlaying\nOffline..",font="Helvetica 16 bold",bg="red",fg="snow",relief=RAISED)
        offline.place(relx=0.01,rely=0.55,relwidth=0.2)
        
        if proceed==0:
            startpage=Frame(canvas)
            startpage.place(relheight=1,relwidth=1)
            try:
                frames=[PhotoImage(file=".img\\Login.gif",format = 'gif -index %i' %(i)) for i in range(100)]
                def update(ind):
                    frame = frames[ind]
                    ind += 1
                    ind=ind%100
                    label.configure(image=frame)
                    startpage.after(100, update, ind)
                label = Label(startpage)
                label.pack()
                startpage.after(0, update, 0)

                descc=Label(startpage,text="This is one time Process \nif you have \nInternet Connection",fg="snow",font="verdana 16",bg="black")
                descc.place(relx=0.22,rely=0.2,relwidth=0.6)

                Log=Entry(startpage,fg="black",font="Courier 20 bold",bg="snow")
                Log.insert(0,"Username")
                Log.place(relx=0.3,rely=0.4,relwidth=0.4)

                startbut=Button(startpage,text="START",fg="white",bg="green",font="impact 14",command=lambda: startt(1))
                startbut.place(relx=0.3,rely=0.53,relwidth=0.4)
                root.bind("<Return>",startt)
            except Exception:
                doc=0
                messagebox.showerror("File Missing!","One of our files are Missing!\nPlease Download again!")
                root.destroy()
            root.mainloop()

conn.commit()
conn.close()
