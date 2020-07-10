from tkinter import *
import mysql.connector
import matplotlib.pyplot as plt
import csv

root = Tk()
root.title('VINCI FarmDB')
root.geometry("400x700")
root.iconbitmap('Logo.ico')
# Connec to the MySQL Server
mydb = mysql.connector.connect(
	host="localhost",
	user = "",                                    #Enter Your Username
	passwd = "",                                   #Enter Your Password
	database = "warehouse"
	)

#FUNCTIONS

#Clear Filed
def clear_field():
	nbox.delete(0,END)
	abox.delete(0,END) 
	pbox.delete(0,END) 
	qbox.delete(0,END)  
	debox.delete(0,END)  
	p1box.delete(0,END)  
	p2box.delete(0,END)  
	dabox.delete(0,END)  
	tbox.delete(0,END)  
	arbox.delete(0,END)  

#Add Data to Database
def add_data():
	sql_command = "INSERT INTO master (name,aadno,ph,catg,quant,des,plts,plte,date,intt,area) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	values = (nbox.get(), abox.get(), pbox.get(), clicked.get(), qbox.get(), debox.get(), p1box.get(), p2box.get(), dabox.get(), tbox.get(), arbox.get())

	cursor.execute(sql_command, values)

	mydb.commit()
	clear_field()
	

#View Database
def view_db():
	view = Tk()
	view.title("List of All Stock In Warehouse")
	view.geometry("800x600")
	view.iconbitmap('Logo.ico')


	cursor.execute("SELECT * FROM master")

	result = cursor.fetchall()
	n1=0
	head = ['Name','AadharNo','PhNo','Type','Quantity','Description','PlotNo(Start)','PlotNo(End)','Date','InTime','Area']

	for i in head:
		hl = Label(view,text=i,fg="red")
		hl.grid(row=0,column=n1)
		n1+=1

	for index, x in enumerate(result):
		num = 0
		for y in x:
			ll = Label(view, text = y)
			ll.grid(row=index+1, column=num)
			num+=1
	csv_b = Button(view, text="Save as Excel", command=lambda: wtocsv(result))
	csv_b.grid(row=index+2, column=0)		



def wtocsv(result):
	with open('Warehouse.csv','a') as f:
		w = csv.writer(f, dialect='excel')

		for record in result:
			w.writerow(record)

#Search Warehouse Function
def search_db():
	search = Tk()
	search.title("List of All Stock In Warehouse")
	search.geometry("800x600")
	search.iconbitmap('Logo.ico')


	def search_now():
		ans = searchbox.get()
		sql = "SELECT * FROM master WHERE aadno = %s"

		ano = (ans, )

		result = cursor.execute(sql,ano)
		result = cursor.fetchall()
		if not result:
			result = "No Record Found"
		
		if result =="No Record Found":
			ansl = Label(search, text=result)
			ansl.grid(row=2,column=0,padx=10)
		else:
			n1=0
			head = ['Name','AadharNo','PhNo','Type','Quantity','Description','PlotNo(Start)','PlotNo(End)','Date','InTime','Area']
			for i in head:
				hl = Label(search,text=i,fg="red")
				hl.grid(row=3,column=n1)
				n1+=1
			for index, x in enumerate(result):
				num = 0
				for y in x:
					ll = Label(search, text = y)
					ll.grid(row=index+4, column=num)
					num+=1
						

	searchbox = Entry(search)
	searchbox.grid(row=0,column=1,padx=10,pady=10)

	slabel = Label(search, text="Enter Aadhar No:")
	slabel.grid(row=0,column=0, padx=10,pady=10)

	sb = Button(search, text="Search Warehouse", command=search_now)
	sb.grid(row=1,column=0,padx=10,pady=10)

#Updating the Database
def update_db():
	udate = Tk()
	udate.title("Update Warehouse")
	udate.geometry("800x600")
	udate.iconbitmap('Logo.ico')

	def update_now():
		ans = searchbox.get()
		sql = "SELECT * FROM master WHERE aadno = %s"

		ano = (ans, )

		result = cursor.execute(sql,ano)
		result = cursor.fetchall()
		name = Label(udate,text="Name").grid(row=2,column=0,sticky=W,padx=10)
		aadno = Label(udate,text="Aadhar Number").grid(row=2+1,column=0,sticky=W,padx=10)
		ph = Label(udate,text="Phone Number").grid(row=3+1,column=0,sticky=W,padx=10)
		catg = Label(udate,text="Type").grid(row=4+1,column=0,sticky=W,padx=10)
		quant = Label(udate,text="Quantity").grid(row=5+1,column=0,sticky=W,padx=10)
		des = Label(udate,text="Description").grid(row=6+1,column=0,sticky=W,padx=10)
		plts = Label(udate,text="Plot Number START").grid(row=7+1,column=0,sticky=W,padx=10)
		plte = Label(udate,text="Plot Number END").grid(row=8+1,column=0,sticky=W,padx=10)
		date = Label(udate,text="Date").grid(row=9+1,column=0,sticky=W,padx=10)
		Time = Label(udate,text="Time").grid(row=10+1,column=0,sticky=W,padx=10)
		area = Label(udate,text="Area Occupied").grid(row=11+1,column=0,sticky=W,padx=10)


		#Creating Input Boxes
		nbox = Entry(udate)
		nbox.grid(row=1+1,column=1)
		nbox.insert(0,result[0][0])

		abox = Entry(udate)
		abox.grid(row=2+1,column=1,pady = 5)
		abox.insert(0,result[0][1])

		pbox = Entry(udate)
		pbox.grid(row=3+1,column=1,pady = 5)
		pbox.insert(0,result[0][2])

		clicked = StringVar()
		clicked.set("Livestock")
		cbox = OptionMenu(udate, clicked, "Livestock", "Grains", "Fruits", "Vegetable", "Fertilizers", "Milk", "Tools")
		cbox.grid(row=4+1,column=1,pady = 5)

		qbox = Entry(udate)
		qbox.grid(row=5+1,column=1,pady = 5)
		qbox.insert(0,result[0][4])

		debox = Entry(udate)
		debox.grid(row=6+1,column=1,pady = 5)
		debox.insert(0,result[0][5])

		p1box = Entry(udate)
		p1box.grid(row=7+1,column=1,pady = 5)
		p1box.insert(0,result[0][6])

		p2box = Entry(udate)
		p2box.grid(row=8+1,column=1,pady = 5)
		p2box.insert(0,result[0][7])

		dabox = Entry(udate)
		dabox.grid(row=9+1,column=1,pady = 5)
		dabox.insert(0,result[0][8])

		tbox = Entry(udate)
		tbox.grid(row=10+1,column=1,pady = 5)
		tbox.insert(0,result[0][9])

		arbox = Entry(udate)
		arbox.grid(row=11+1,column=1,pady = 5)
		arbox.insert(0,result[0][10])



		def update_two():
			sql_command = """UPDATE master SET name = %s,ph = %s,catg = %s,quant = %s,des = %s,plts = %s,plte = %s,date = %s,intt = %s,area = %s WHERE aadno = %s"""
			values = (nbox.get(), pbox.get(), clicked.get(), qbox.get(), debox.get(), p1box.get(), p2box.get(), dabox.get(), tbox.get(), arbox.get(),abox.get())

			cursor.execute(sql_command, values)

			mydb.commit()

			udate.destroy()

		up = Button(udate,text="Update Record",command=update_two)
		up.grid(row=13,column=0)		



	searchbox = Entry(udate)
	searchbox.grid(row=0,column=1,padx=10,pady=10)

	slabel = Label(udate, text="Enter Aadhar No:")
	slabel.grid(row=0,column=0, padx=10,pady=10)

	sb = Button(udate, text="Update Person With AadharNo", command=update_now)
	sb.grid(row=1,column=0,padx=10,pady=10)

#Plotting Functions

def occupied_graph():
	cursor.execute("SELECT SUM(area) FROM master")
	val = cursor.fetchall()
	val1 = val[0][0]
	val2 = 100 - val1

	label = 'Occupied' , 'Unoccupied'

	sizes = [val1 , val2]

	explode = (0.1,0)

	fig1, ax1 = plt.subplots()

	ax1.pie(sizes, explode=explode, labels = label,autopct = '%1.1f%%',shadow=True, startangle = 90)

	ax1.axis('equal')

	plt.title("Occupancy Chart")
	plt.show()

def cateo_chart():
	cursor.execute("SELECT SUM(area) FROM master GROUP BY catg")
	val = cursor.fetchall()
	
	label = "Livestock", "Grains", "Fruits", "Vegetable", "Fertilizers", "Milk", "Tools"

	sizes = [val[0][0], val[1][0] , val[2][0] , val[3][0], val[4][0], val[5][0], val[6][0]]

	explode = (0.1,0,0,0,0,0,0)

	fig1, ax1 = plt.subplots()

	ax1.pie(sizes, explode=explode, labels = label,autopct = '%1.1f%%',shadow=True, startangle = 90)

	ax1.axis('equal')

	plt.title("Category Wise Occupancy Chart")
	plt.show()


#Calcuate Cost
def cal_cost():
	return



#Cursor for MySQL

cursor = mydb.cursor()

#Creating Database

# cursor.execute("CREATE DATABASE warehouse")

#Creating the Table

# cursor.execute("CREATE TABLE master(name VARCHAR(255),aadno INT(12) PRIMARY KEY,ph INT(10),catg VARCHAR(255),quant INT(10),des TEXT,plts INT(10),plte INT(10),date DATE,intt TIME,area INT(10))")


tlt_label = Label(root, text="VINCI FarmDB",font=("Times","24","bold"))
tlt_label.grid(row=0,column=0,columnspan=2,pady="10")


#Creating the Form

name = Label(root,text="Name").grid(row=1,column=0,sticky=W,padx=10)
aadno = Label(root,text="Aadhar Number").grid(row=2,column=0,sticky=W,padx=10)
ph = Label(root,text="Phone Number").grid(row=3,column=0,sticky=W,padx=10)
catg = Label(root,text="Type").grid(row=4,column=0,sticky=W,padx=10)
quant = Label(root,text="Quantity").grid(row=5,column=0,sticky=W,padx=10)
des = Label(root,text="Description").grid(row=6,column=0,sticky=W,padx=10)
plts = Label(root,text="Plot Number START").grid(row=7,column=0,sticky=W,padx=10)
plte = Label(root,text="Plot Number END").grid(row=8,column=0,sticky=W,padx=10)
date = Label(root,text="Date").grid(row=9,column=0,sticky=W,padx=10)
Time = Label(root,text="Time").grid(row=10,column=0,sticky=W,padx=10)
area = Label(root,text="Area Occupied").grid(row=11,column=0,sticky=W,padx=10)


#Creating Input Boxes
nbox = Entry(root)
nbox.grid(row=1,column=1)

abox = Entry(root)
abox.grid(row=2,column=1,pady = 5)

pbox = Entry(root)
pbox.grid(row=3,column=1,pady = 5)

clicked = StringVar()
clicked.set("Livestock")
cbox = OptionMenu(root, clicked, "Livestock", "Grains", "Fruits", "Vegetable", "Fertilizers", "Milk", "Tools")
cbox.grid(row=4,column=1,pady = 5)

qbox = Entry(root)
qbox.grid(row=5,column=1,pady = 5)

debox = Entry(root)
debox.grid(row=6,column=1,pady = 5)

p1box = Entry(root)
p1box.grid(row=7,column=1,pady = 5)

p2box = Entry(root)
p2box.grid(row=8,column=1,pady = 5)

dabox = Entry(root)
dabox.grid(row=9,column=1,pady = 5)

tbox = Entry(root)
tbox.grid(row=10,column=1,pady = 5)

arbox = Entry(root)
arbox.grid(row=11,column=1,pady = 5)

#Buttons
add_b = Button(root, text="Add to Warehouse", command=add_data)
add_b.grid(row=12,column=0,padx=10,pady=10)

clear_b = Button(root, text="Clear Data", command=clear_field)
clear_b.grid(row=12,column=1)

view_b = Button(root, text="View The Entire Warehouse", command=view_db)
view_b.grid(row=13,column=0,sticky=W,padx=10)

search_b = Button(root, text="Search Warehouse", command=search_db)
search_b.grid(row=13,column=1, sticky=W, padx=10)

update_b = Button(root,text="Warehouse Update", command=update_db)
update_b.grid(row=14,column=0,sticky=W,padx=10,pady=10)

plot1 = Label(root,text="Plotting Functions",fg="red")
plot1.grid(row=15,column=0)

occ = Button(root,text="Occupancy Chart",command=occupied_graph)
occ.grid(row=16,column=0,sticky=W,padx=10,pady=10)

cato = Button(root,text="Category Chart",command=cateo_chart)
cato.grid(row=16,column=1,sticky=W,padx=10,pady=10)

plot2 = Label(root,text="Cost Calculator",fg="red")
plot2.grid(row=17,column=0)

cost_b = Button(root,text="Calculate Cost",command=cal_cost)
cost_b.grid(row=18,column=0,sticky=W,padx=10,pady=10)

root.mainloop()


