def create_layout(frame):
    """add two buttons to frame"""
    
    # add your code here
    button1 = Button(frame,text="Button1",command=pressed)
    button1.pack(side=LEFT)
    button2 = Button(frame,text="Button2",command=pressed)
    button2.pack(side=LEFT)
