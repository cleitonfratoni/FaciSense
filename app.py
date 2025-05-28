from flask import Flask, render_template, request, redirect, url_for, flash
import face_recognition
import cv2
import os

app = Flask(__name__)
app.secret_key = "secret"

FACE_DB_PATH = "face_db"

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
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    video_capture.release()

    if not ret:
        flash("Erro ao acessar a câmera.")
        return redirect(url_for('index'))

    known_encodings, known_names = load_known_faces()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_encodings(rgb_frame)

    if not faces:
        flash("Nenhum rosto detectado.")
        return redirect(url_for('index'))

    match = face_recognition.compare_faces(known_encodings, faces[0])
    if True in match:
        name = known_names[match.index(True)]
        flash(f"Login bem-sucedido. Bem-vindo, {name}!")
    else:
        flash("Rosto não reconhecido.")

    return redirect(url_for('index'))

# NOVA ROTA: Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip().lower().replace(" ", "_")
        if not name:
            flash("Nome inválido.")
            return redirect(url_for('register'))

        # Captura imagem da webcam
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        video_capture.release()

        if not ret:
            flash("Erro ao acessar a câmera.")
            return redirect(url_for('register'))

        # Detecta rostos
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) != 1:
            flash("Por favor, certifique-se de que apenas UM rosto está visível.")
            return redirect(url_for('register'))

        # Salva imagem com o nome
        save_path = os.path.join(FACE_DB_PATH, f"{name}.jpg")
        cv2.imwrite(save_path, frame)
        flash(f"Usuário {name} registrado com sucesso.")
        return redirect(url_for('index'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
