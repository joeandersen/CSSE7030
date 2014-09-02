def create_layout(frame):
    button1 = Button(frame,text = 'Button1',command=pressed)
    button2 = Button(frame,text = 'Button2',command=pressed)

    button1.pack(side=TOP, anchor = W, pady=20)
    button2.pack(side=TOP, anchor = W, ipadx=20)
    
