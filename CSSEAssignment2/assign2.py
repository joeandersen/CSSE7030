###################################################################
#
#   CSSE1001/7030 - Assignment 2
#
#   Student Number: 33422619
#
#   Student Name: Joseph Andersen
#
###################################################################

#
# Do not change the following import
#

from assign2_support import *

####################################################################
#
# Insert your code below
#
####################################################################

class PVData:
    """Class to hold the PV data for a given date."""

    def format_data(self,date_string):
        """reads in and loads data. Manipulates data into required format"""

        #Checking for bad date_strings
        
        

        data = load_data(date_string)
        self._times = []
        self._temperatures = []
        self._sunlights = []
        self._powers = dict()
        for array in ARRAYS:
            self._powers[array] = []
            
        for record in data:
            self._times.append(record[0])
            self._temperatures.append(record[1])
            self._sunlights.append(record[2])
            powers= record[3]
            for array,datum in enumerate(powers):
                self._powers[ARRAYS[array]].append(datum)
        return
                
          


    def __init__(self):
        """initializes the pv data with yesterday's data"""
        date_string = yesterday()
        self._date = date_string
        #data = load_data(date_string)
        #self._data = data
        self.format_data(date_string)
        return

    def change_date(self, date):
        """change the data to be for the given date. Must not
        reextract data if same date is used"""

        # Check if date change is actually required

        if self.get_date == date:
            return
        else:
            self._date = date
            try:
                self.format_data(date)
            except Exception as e:
                print e
                
            return
        

        

    def get_date(self):
        """return the date for the stored data"""
        return self._date

    def get_time(self,time_index):
        """return the time for the given index of the time data"""
        #return self._data[time_index][0]
        return self._times[time_index]
    
    def get_temperature(self):
        """return the list of temperature values for the current date"""
        """temperatures = []
        for record in self._data:
            temperatures.append(record[1])
        return temperatures"""
        return self._temperatures
 
    def get_sunlight(self):
        """return the list of sunlight values for the current date"""
        """sunlights = []
        for record in self._data:
            sunlights.append(record[2])
        return sunlights"""
        return self._sunlights

    def get_power(self,array):
        """returns power output for the current date and the given array"""
        return self._powers[array]
        
    def get_cumulative_energy(self,array):
        """computes and returns the list of cumulative energies for the
        current date and the given array"""

        powers = self._powers[array]

        cumulative_powers = []
        
        for count,power in enumerate(powers):
            accumulated_power = power
            for j in range(0,count):
                accumulated_power += powers[j]
            cumulative_powers.append(accumulated_power)

        return cumulative_powers
        
    
        
 
    

#Testing code for the data class functionality
    
"""
pvd = PVData()
pvd.change_date('13-09-2014')
print pvd.get_date()
print pvd.get_time(300)
print pvd.get_temperature()[300:304]
print pvd.get_sunlight()[300:304]
print pvd.get_power('UQ Centre, St Lucia')[300:304]
print pvd.get_power('All Arrays Combined')[300:304]
print pvd.get_cumulative_energy('All Arrays Combined')[300:304]
print pvd.get_power('All Arrays Combined')[0:4]
print pvd.get_cumulative_energy('All Arrays Combined')[0:4]

#get_data_for_date('')
#get_data_for_date('20-10-2050')
#get_data_for_date('20_10_2014')
#pvd.change_date('')
#pvd.change_date('20-10-2050')
#pvd.change_date('20_10_2014')
"""

class Plotter(Canvas):
    """class responsible for doing the plotting"""

    def __init__(self,parent,pvd,options_frame):

        self._width = 900
        self._height = 500
        
        self._canvas = Canvas(parent, bg="white", width=self._width,
                              height=self._height)
        self._canvas.pack(side=TOP, expand=True, fill=BOTH)
        self._coord_trans=CoordinateTranslator(self._width,
                                               self._height,
                                               len(pvd.get_temperature()))

        self._options_frame = options_frame
        self._pvd = pvd
        self.draw_plot()
        return

    def draw_plot(self):


        
        if self._options_frame._power_v.get() ==2:
            self.draw_power(self._pvd,self._options_frame._array_variable.get())
        
        elif self._options_frame._power_v.get() ==3:
            self.draw_cumulative_energy(self._pvd,self._options_frame._array_variable.get())


        if self._options_frame._plot_sun.get():
            self.draw_sunlight(self._pvd)
        if self._options_frame._plot_temp.get():
            self.draw_temperature(self._pvd)
        
        return
    
    def draw_power(self,pvd,array):
        
       
        powers = pvd.get_power(array)
    
    
        point_list = []
        for count,power in enumerate(powers):

            point_list.append(self._coord_trans.power_coords(count,power,array))
            
        self._canvas.create_polygon(point_list,
                                    outline=POWER_COLOUR,fill=POWER_COLOUR)

    def draw_cumulative_energy(self,pvd,array):
        

       
        accum_energies = pvd.get_cumulative_energy(array)
 
    
        point_list = []
        for count,accum_energy in enumerate(accum_energies):
            point_list.append(self._coord_trans.power_coords(count,
                                                             accum_energy/400,array))

        point_list.append(self._coord_trans.power_coords(count,
                                                             0,array))

        

        self._canvas.create_polygon(point_list,
                                    outline=POWER_COLOUR,fill=POWER_COLOUR)



    def draw_temperature(self,pvd):
        temperatures = pvd.get_temperature()
        point_list = []
        for count,temp in enumerate(temperatures):
            point_list.append(self._coord_trans.temperature_coords(count,temp))
        self._canvas.create_line(point_list, fill='yellow')
    
    def draw_sunlight(self,pvd):
        sunlights = pvd.get_sunlight()
        point_list = []
        for count,sunlight in enumerate(sunlights):
            point_list.append(self._coord_trans.sunlight_coords(count,sunlight))
        self._canvas.create_line(point_list, fill='yellow')


    def delete(self):
        self._canvas.delete(ALL)
    

class OptionsFrame(Frame):
    """The widget used for choosing options"""

    

    def __init__(self,parent,plotting_app,pvd):



        self._plotting_app = plotting_app
        Frame.__init__(self,parent)
    

        row1 = Frame(self)
        #A row of three radiobuttons to choose between
        #No power, Instantaeous power and Cumulative power
        power_v = IntVar()
        power_v.set(2)
        Radiobutton(row1, text='No Power', variable=power_v,
                    value=1).pack(side=LEFT)
        Radiobutton(row1, text='Instantaneous Power', variable=power_v,
                    value=2).pack(side=LEFT)
        Radiobutton(row1, text='Cumulative Energy', variable=power_v,
                    value=3).pack(side=LEFT)
        self._power_v = power_v
        row1.pack(side=TOP)

        row2 = Frame(self)
        #A row of two checkbuttons so the user can choose
        #what data, other than power is displayed
        plot_temp = IntVar()
        plot_sun = IntVar()
        Checkbutton(row2, text='Temperature', variable=plot_temp).pack(side=LEFT)
        Checkbutton(row2, text='Sunlight', variable=plot_sun).pack(side=LEFT)
        self._plot_temp = plot_temp
        self._plot_sun = plot_sun
        row2.pack(side=TOP, expand=TRUE)

   
        row3 = Frame(self)

        
      

        #an entry box where the user can enter a date
        Label(row3,text = 'Choose Date:').pack(side=LEFT)
        self.entry = Entry(row3, width=20)
        self.entry.insert(END,pvd.get_date())
        self.entry.pack(side=LEFT)
        #a button to apply the choice of date and array
        Button(row3,text ='Apply',command=self.apply_choices).pack(side=LEFT)


        
        #an OptionMenu allowing the user to choose which
        #which array to display. All combined is default
        array_variable = StringVar()
        array_variable.set(ARRAYS[-1])
        OptionMenu(row3,array_variable,*ARRAYS).pack(side=RIGHT)

        self._array_variable = array_variable
        row3.pack(side=TOP)
        return


    def apply_choices(self):

        print self._power_v.get()
        print self._plot_temp.get()
        print self._plot_sun.get()
        date_string = self.entry.get()
        self._date_string = date_string
        print self._date_string
        print self._array_variable.get()

        self._plotting_app.apply()
        return
       
       

class PVPlotApp:
    """top level class for the GUI. responsible for
    creating and managing instances of the above classes"""

    def __init__(self, master):

        master.title('PV Plotter')
        self._pvd = PVData()
        #pvd.change_date('08-12-2013')
        
        self._options_frame = OptionsFrame(master,self,self._pvd)
        self._options_frame.pack(side=BOTTOM)
        self._plotter = Plotter(master,self._pvd,self._options_frame)#.pack(side=TOP)
 

    def apply(self):
        self._plotter.delete()
        self._pvd.change_date(self._options_frame._date_string)
        self._plotter.draw_plot()
        


####################################################################
#
# WARNING: Leave the following code at the end of your code
#
# DO NOT CHANGE ANYTHING BELOW
#
####################################################################

def main():
    root = Tk()
    app = PVPlotApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()






