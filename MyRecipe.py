from flask import Flask,render_template,request,session
from flask import redirect,url_for
from DatabaseHelper import dataBase
# nm = ""
# tl = ""
error = ""
email = ""
app = Flask(__name__)
# session['name'] = " "
app.secret_key = 'YouWillNeverGetIt'

app.config['dbconfig'] = {'host':'127.0.0.1',
                'user':'root',
                'password':'Hemant@3726',
                'database':'MyRecipe',}

def log_user(req:'MyRecipe') -> None:
    with dataBase(app.config['dbconfig']) as cursor:
      str = """insert into userInfo(Fname,Lname,passwd,email_id) values (%s,%s,%s,%s) """
      cursor.execute(str,(req.form['Fname'],req.form['Lname'],req.form['password'],req.form['email'],))

def log_recipe(email:'String',rname:'String',loc:'String') -> bool:
    with dataBase(app.config['dbconfig']) as cursor:
        try:
         str = """insert into rcp_file(email,RCname,RCloc) values (%s,%s,%s)"""
         cursor.execute(str,(email,rname,loc,))
        except:
            return False
    return True

def my_recipe(email:'String') -> list:
    with dataBase(app.config['dbconfig']) as cursor:
        str = """select RCname,RCloc from rcp_file where email = %s"""
        cursor.execute(str,(email,))
        data = cursor.fetchall()
    return data


def valid_user(req:'MyRecipe')->int:
    with dataBase(app.config['dbconfig']) as cursor:
       str = """select count(*),Fname from userInfo where passwd = %s and email_id = %s """
       cursor.execute(str,(req.form['password'],req.form['email'],))
       a = cursor.fetchall()
    return a



@app.route('/')
def home():
    title = "Welcome, To My Cook Book"
    phrase = "What would you like to make Today ?"
    item = ("Breakfast","Dinner","Diet Food","Dessert","Fast Food")
    if 'pswd' in session:
        session['pswd'] = " "
    if 'name' in session:
       name = session['name']
    else:
        name = " "
    return render_template('home.html',title="My Cook Book",header = title,phrase=phrase,item_list=item,name=name)

@app.route('/Breakfast.html')
def breakfast():
    header = "Breakfast Food Recipe's"
    food_item = ('Scrambled Eggs','Oatmeal','Bagels','Hash Brown','Bacon','Omellete','Fried Patatoes')
    return render_template('Breakfast.html',title="Breakfast Recipe",header=header)

@app.route('/Dinner.html')
def dinner():
    header = "Dinner Food Recipe's"
    food_item = ()
    return render_template('Dinner.html',title="Dinner Recipe",header=header)

@app.route('/Diet')
def diet():
    header = "Diet Food Recipe's"
    food_item = ()
    return render_template('Diet.html',title="Diet Food Recipe",header=header)

@app.route('/Dessert.html')
def dessert():
    header = "Dessert Recipe's"
    food_item = ()
    return render_template('Dessert.html',title = "Dessert Recipe",header=header)

@app.route('/Fast')
def fast():
    header = "Fast Food Recipe"
    food_item = ()
    return render_template('Fast.html',title="Fast Food Recipe",header=header)

# @app.route('/MyRecipe')
# def Recipe():
#     if 'logged_in' not in session:
#      return details()
#     else:
#       global nm
#       name = nm
#       return render_template('MyBook.html',name=name)

@app.route('/register',methods=['POST'])
def register():
    # global tl
    if (request.form['password'] == request.form['cnfrm']):
     session['pswd'] = " "
     log_user(request)
     # global email
     # session['email'] = request.form['email']
     # print(email)
     return redirect(url_for('login'))
    else:
     session['pswd'] = "Your password doesn't match"
     return redirect(url_for('details'))

@app.route('/details')
def details():
    # global tl
    if 'pswd' in session:
     title = session['pswd']
    else:
     title = " "
    if 'logged_in' in session:
     session.pop('logged_in')
    return render_template('Register.html',title=title)


@app.route('/login')
def login():
    if 'logged_in' in session:
        # global nm
        # name = nm
        return redirect(url_for('recipe'))
    else:
     global error
     er = error
     return render_template('login.html',error=er)

@app.route('/MyBook',methods=['POST'])
def mybook():
    val = valid_user(request)
    # global email
    session['email'] = request.form['email']
   # pdb.set_trace()
    if 1 in val[0]:
        session['logged_in'] = True
        name = val[0][1]
        # global nm
        # nm = name.title()
        session['name']=name.title()
        return redirect(url_for('recipe'))
    else:
        global error
        error = "your email id and password don't match"
        return redirect(url_for('login'))

@app.route('/MyRecipe')
def recipe():
   if 'logged_in' in session:
    name = session['name']
    return render_template('MyBook.html',name=name)
   else:
     return redirect(url_for('login'))



@app.route('/SaveRcp',methods=['POST'])
def saveRcp():
    # global email
    em = session['email']
    rname = request.form['rname']
    rcp = request.form['recipe']
    loc = "Recipe/"+em + "_"+rname+".txt"
    flag = log_recipe(em, rname, loc)
    if flag:
     with open(loc,'w') as entry:
        entry.write(rcp)
     str = "Done Successfully !"
    else:
      str = "Recipe for this food is allready exist"
    return str

@app.route('/logout')
def logout():
  session['name'] = " "
  session['pwsd'] = " "
  session['email'] = " "
  if 'logged_in' in session:
    session.pop('logged_in')
    #global nm
    # session['name']=" "
    # global tl
    # session['pswd']= " "
    global error
    #nm = ""
    # tl = ""
    error = ""
    return redirect(url_for('home'))
  else:
      return redirect(url_for('home'))

@app.route('/Recipelist')
def mylist():
    email = session['email']
    rcp_list = []
    rcp_loc = []
    list_data = my_recipe(email)
    for data in list_data:
            rcp_list.append(data[0])
            rcp_loc.append(data[1])

    return render_template('Recipelist.html',name=session['name'],item_list=list_data)

@app.route('/FoodRecipe',methods=['GET','POST'])
def foodrcp():
    data_list = request.args.get('type')
    # print(data_list)
    with open(data_list,'r') as file:
     content = file.read()
    return render_template('foodrcp.html',content=content)


if __name__ == '__main__':
    app.run(debug=True)

