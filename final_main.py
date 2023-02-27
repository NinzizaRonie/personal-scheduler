from final_connect import my_conn
import tkinter as tk
from tkinter import *
from datetime import datetime,date
my_w = tk.Tk()
my_w.geometry("500x400") 
from tkcalendar import DateEntry
f_done=('Times',16,'overstrike') # font style for tasks completed
f_normal=('Times',16,'normal')  # for pending 
def my_upd(k):
    if(my_ref[k][1].get()==True):
        my_ref[k][0].config(font=f_done,fg='green')
        q='UPDATE my_tasks SET status=True WHERE id='+str(k)
    else:
        my_ref[k][0].config(font=f_normal,fg='blue')
        q='UPDATE my_tasks SET status=False WHERE id='+str(k)
    r_set=my_conn.execute(q)    
    msg="No. Updated:"+str(r_set.rowcount) # Number of rows updated
    my_msg(msg) # show message for 3 seconds 
    
l1=tk.Label(my_w,text='Task List with Date',font=('Times',22,('bold','underline')),fg='green')
l1.grid(row=0,column=0,padx=30,pady=10,columnspan=5,sticky='ew')    
e1=tk.Entry(my_w,width=12,bg='yellow',font=18)
e1.grid(row=1,column=0,padx=10)
cal=DateEntry(my_w,selectmode='day',font=18)
cal.grid(row=1,column=1)
b1=tk.Button(my_w,text='+',font=18,command=lambda:add_task())
b1.grid(row=1,column=2)
b2=tk.Button(my_w,text='-',font=18,bg='red',command=lambda:delete_task())
b2.grid(row=1,column=3,padx=3)
l2=tk.Label(my_w,text='Message here',bg='lightgreen',width=15)    
l2.grid(row=1,column=4,padx=2)

task_frame=Frame(my_w,width=390, height=390,background='lightyellow',
highlightbackground='lightblue',highlightthicknes=3)
task_frame.grid(row=2,column=0,columnspan=5,
    padx=15,pady=5,ipadx=5,ipady=5,sticky='w')
my_ref={} # to store references to checkboxes 
def my_show():
    for w in task_frame.grid_slaves(): #Loop through each row 
        w.grid_forget() # remove the row 
    q='SELECT *  FROM my_tasks '  # query to collect data from table
    my_cursor=my_conn.execute(q)
    r_set=my_cursor.fetchall()
    my_dict = {row[0]: [row[1],row[2],row[3]] for row in r_set}                

    i=2 # row number 
    for k in my_dict.keys(): # Number of checkbuttons 
        var=tk.BooleanVar() # variable 
        var.set(my_dict[k][1]) # set to value of status column
        if my_dict[k][1]==True: # set font based on status column
            font,fg=f_done,'green' # if True 
        else:
            font,fg=f_normal,'blue'
        ck = tk.Checkbutton(task_frame, text=my_dict[k][0], 
        variable=var,onvalue=True,offvalue=False,font=font,fg=fg,
        command=lambda k=k: my_upd(k))
        ck.grid(row=i,column=0,padx=20,pady=1,sticky='w')
        dt=datetime.strptime(my_dict[k][2],'%Y-%m-%d').strftime('%d-%b-%Y') # sqlite
        # dt=datetime.strftime(my_dict[k][2],'%d-%b-%Y')
        ld=tk.Label(task_frame,text=dt) # Label to display date
        ld.grid(row=i,column=1,padx=2)
        my_ref[k]=[ck,var] # to hold the references 
        i=i+1 # increase the row number 
def add_task():
    dt=cal.get_date() # Selected date from the calendar 
    #dt=date.today()  # Use today's date if required 
    my_data=(e1.get(),False,dt) # data to pass using query
    r_set=my_conn.execute("INSERT INTO my_tasks (tasks, status,dt) \
        VALUES(?,?,?)",my_data)
    ### for MySQL use the below line and remove the above line 
    # r_set=my_conn.execute("INSERT INTO my_tasks (tasks, status,dt) \
    #      VALUES(%s,%s,%s)",my_data)

    msg="Task ID:"+str(r_set.lastrowid) # id of the row added 
    e1.delete(0,'end') # remove the task from entry box
    my_msg(msg) # show message for 3 seconds 
    my_show() # refresh the view 
def delete_task(): # remove all completed tasks
    r_set=my_conn.execute("DELETE FROM my_tasks WHERE status=True")
    msg="No Deleted:"+str(r_set.rowcount) # Number of rows deleted
    my_msg(msg) # show message for 3 seconds 
    my_show()   # refresh the view   

def my_msg(msg):
    l2.config(text=msg) # show message 
    my_w.after(3000,lambda:l2.config(text='')) # remove after 3 seconds
    


my_show()
my_w.mainloop() # keep the window open   