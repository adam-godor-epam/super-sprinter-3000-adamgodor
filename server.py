from flask import Flask, render_template, redirect, request, session
app = Flask(__name__)


def get_ID():
    table = read_from_csv("data.csv")
    ID_list = [i[0] for i in table]
    ID_list_int = [int(i) for i in ID_list]
    if sorted(ID_list_int) == list(range(1, len(ID_list)+1)):
        return str(len(ID_list_int)+1)
    else:
        for i in range(1, len(ID_list_int)+1):
            if i not in ID_list_int:
                return str(i)
            else:
                continue

def read_from_csv(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(";") for element in lines]
    return table


def write_to_csv(table, filename = "data.csv"):
    with open(filename, "w") as file:
        for data in table:
            line = ';'.join(data)
            file.write(line +'\n')


@app.route('/')
def route_index():
    header_list = ["ID", "Story name", "Story", "Acceptance Criteria", "Business Value", "Estiamtion", "Status", "Delete", "Edit"]
    table = read_from_csv("data.csv")
    return render_template('list.html', header_list = header_list, table = table)


@app.route('/story')
def route_story():
    return render_template('story.html', options=['Planning','TODO','Review','Done','In progress'])

@app.route('/save-story', methods = ["GET", "POST"])
def save_story():
    if request.method == "POST":
        ID = get_ID()
        storytitle = request.form['storytitle']
        story = request.form['story']
        criteria = request.form['criteria']
        business = request.form['business']
        estimation = request.form['estimation']
        status = request.form['options']
    new_story = [ID, storytitle, story, criteria, business, estimation, status]
    with open('data.csv', "a") as file:
        line = ';'.join(new_story)
        file.write(line +"\n")
    return redirect('/')


@app.route('/delete', methods = ['POST', 'GET'])
def delete_story():
    table = read_from_csv("data.csv")
    ID = request.form['delete']
    sID = str(ID)
    for item in table:
        if item[0] == sID:
            table.remove(item)
    write_to_csv(table)
    return redirect('/')


@app.route('/edit/<ID>', methods = ['POST', 'GET'])
def edit_story(ID):
    table = read_from_csv("data.csv")
    ID = request.form['edit']
    sID = str(ID)
    edit_list = []
    for item in table:
        if item[0] == sID:
            edit_list = item
    return render_template('story.html',ID = 'ID', options=['Planning','TODO','Review','Done','In progress'], edit_list = edit_list)


@app.route('/edit-story', methods = ['POST', 'GET'])
def edit():
    table = read_from_csv("data.csv")
    ID = request.form['edit']
    sID = str(ID)
    if request.method == "POST":
        storytitle = request.form['updatestorytitle']
        story = request.form['updatestory']
        criteria = request.form['updatecriteria']
        business = request.form['updatebusiness']
        estimation = request.form['updateestimation']
        status = request.form['options']
    update_story = [sID, storytitle, story, criteria, business, estimation, status]
    for item in table:
        if sID == item[0]:
            index_of_the_updated_row = table.index(item)
            table.remove(item)
            table.insert(index_of_the_updated_row, update_story)
    write_to_csv(table)
    return redirect ('/')


if __name__ == "__main__":
  app.secret_key = 'asdasd'
  app.run(
      debug=True,  # Allow verbose error reports
      port=5000  # Set custom port
  )
