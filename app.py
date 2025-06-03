from flask import Flask, render_template, request, redirect, url_for, flash
import face_recognition
import cv2
import os
import numpy as np
import time

app = Flask(__name__)
app.secret_key = "secret"

FACE_DB_PATH = "static/face_db"

if not os.path.exists(FACE_DB_PATH):
    os.makedirs(FACE_DB_PATH)

def capture_frame():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return ret, frame

def load_known_faces():
    known_encodings = []
    known_names = []

    for filename in os.listdir(FACE_DB_PATH):
        image_path = os.path.join(FACE_DB_PATH, filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(filename)[0])
    return known_encodings, known_names

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    ret, frame = capture_frame()
    if not ret:
        flash("Erro ao acessar a câmera.")
        return redirect(url_for('index'))

    known_encodings, known_names = load_known_faces()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_encodings(rgb_frame)

    if not faces:
        flash("Nenhum rosto detectado.")
        return redirect(url_for('index'))

    distances = face_recognition.face_distance(known_encodings, faces[0])
    if len(distances) == 0:
        flash("Nenhum rosto conhecido encontrado.")
        return redirect(url_for('index'))

    min_distance_index = np.argmin(distances)
    if distances[min_distance_index] < 0.5:
        name = known_names[min_distance_index]
        flash(f"Login bem-sucedido. Bem-vindo, {name}!")
        return redirect(url_for('dashboard', user=name))
    else:
        flash("Rosto não reconhecido.")
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    user = request.args.get('user', 'usuário')
    return render_template('dashboard.html', user=user)

# NOVA ROTA: Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip().lower().replace(" ", "_")
        if not name:
            flash("Nome inválido.")
            return redirect(url_for('register'))

        image_path = os.path.join(FACE_DB_PATH, f"{name}.jpg")

        # Evita duplicação por nome
        if os.path.exists(image_path):
            flash("Este nome já está registrado.")
            return redirect(url_for('register'))

        # Captura imagem com countdown
        ret, frame = capture_frame()
        if not ret:
            flash("Erro ao acessar a câmera.")
            return redirect(url_for('register'))

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        new_face_encodings = face_recognition.face_encodings(rgb_frame)

        if len(new_face_encodings) != 1:
            flash("Por favor, certifique-se de que apenas UM rosto está visível.")
            return redirect(url_for('register'))

        new_encoding = new_face_encodings[0]

        # Verifica duplicação por rosto
        for filename in os.listdir(FACE_DB_PATH):
            known_image_path = os.path.join(FACE_DB_PATH, filename)
            known_image = face_recognition.load_image_file(known_image_path)
            known_encodings = face_recognition.face_encodings(known_image)

            if known_encodings and face_recognition.compare_faces([known_encodings[0]], new_encoding, tolerance=0.5)[0]:
                flash("Este rosto já está registrado com outro nome.")
                return redirect(url_for('register'))

        # Salva a imagem se não houver duplicação
        cv2.imwrite(image_path, frame)
        flash(f"Usuário {name} registrado com sucesso.")
        return redirect(url_for('index'))

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
