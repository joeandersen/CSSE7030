def create_layout(frame):

    frame2 = Frame(frame,bg='red')
    
    button1 = Button(frame2,text = 'Button1',command=pressed)
    button2 = Button(frame2,text = 'Button2',command=pressed)
    button3 = Button(frame,text = 'Button3',command=pressed)
    button4 = Button(frame,text = 'Button4',command=pressed)

    button1.pack(side=TOP, expand=True)
    button2.pack(side=TOP, expand=True)
    frame2.pack(side=LEFT, fill = BOTH, expand=True)
    button3.pack(side=LEFT, expand=True)
    button4.pack(side=LEFT, expand=True)
