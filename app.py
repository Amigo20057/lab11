from flask import Flask, render_template, request, redirect, url_for, session, flash
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Фіктивна база даних
albums = {}

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Сторінка "Про проект"
@app.route('/about')
def about():
    return render_template('about.html')

# Сторінка "Історія гурту"
@app.route('/history')
def history():
    return render_template('history.html')

# Сторінка зі списком альбомів
@app.route('/albums')
def albums_page():
    return render_template('albums.html', albums=albums)

# Додавання нового альбому
@app.route('/album/new', methods=['GET', 'POST'])
def new_album():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        album_id = str(uuid.uuid4())
        albums[album_id] = {
            'title': request.form['title'],
            'description': request.form['description']
        }
        flash('Альбом додано!')
        return redirect(url_for('albums_page'))
    return render_template('album_form.html', action="Додати альбом")

# Редагування альбому
@app.route('/album/edit/<album_id>', methods=['GET', 'POST'])
def edit_album(album_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        albums[album_id]['title'] = request.form['title']
        albums[album_id]['description'] = request.form['description']
        flash('Альбом оновлено!')
        return redirect(url_for('albums_page'))
    return render_template('album_form.html', action="Редагувати альбом", album=albums[album_id])

# Видалення альбому
@app.route('/album/delete/<album_id>')
def delete_album(album_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    albums.pop(album_id, None)
    flash('Альбом видалено!')
    return redirect(url_for('albums_page'))

# Авторизація
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            flash('Ви увійшли!')
            return redirect(url_for('albums_page'))
        else:
            flash('Неправильний логін або пароль.')
    return render_template('login.html')

# Вихід з системи
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Ви вийшли з системи.')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()