# 🔐 Login com Face ID – Flask + OpenCV + face\_recognition

Este projeto implementa um sistema de **login seguro com reconhecimento facial**, substituindo senhas tradicionais por autenticação via câmera.

## 📸 Visão Geral

* Cadastro e login usando o rosto do usuário.
* Interface web com **Flask**.
* Banco de dados de rostos usando **imagens locais** (pasta `face_db/`).
* Verificação de duplicidade por nome e por rosto.

---

## ⚙️ Tecnologias Utilizadas

* [Python 3.x](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)
* [OpenCV](https://opencv.org/)
* [face\_recognition](https://github.com/ageitgey/face_recognition)
* [HTML/CSS/JS](https://developer.mozilla.org/pt-BR/docs/Web/HTML)

---

## 🧠 Como Funciona

### 1. Registro (`/register`)

* Usuário informa o nome.
* Câmera ativa e conta regressiva (3 segundos).
* O rosto é detectado e salvo como uma imagem em `face_db/`.
* O sistema verifica se:

  * O **nome já existe**.
  * O **rosto já está registrado** (mesmo com outro nome).

### 2. Login (`/login`)

* Câmera ativa e captura uma imagem.
* O rosto capturado é comparado com os rostos salvos.
* Se houver correspondência, o usuário é autenticado e redirecionado ao **Dashboard**.

### 3. Dashboard

* Mostra a imagem do usuário.
* Exibe uma mensagem de boas-vindas.
* Contém um mini-jogo interativo 🎮 (Clique na bolinha).

---

## ▶️ Como Executar

### 1. Instale as dependências:

```bash
pip install flask opencv-python face_recognition
```

> Obs: O `face_recognition` pode exigir bibliotecas adicionais como `dlib`. Recomenda-se usar um ambiente virtual.

### 2. Estrutura de Diretórios

```
faceid-flask/
│
├── app.py
├── face_db/             # Imagens registradas
├── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── script.js
│   │   └── game.js
```

### 3. Execute o projeto

```bash
python app.py
```

Acesse via navegador: [http://localhost:5000](http://localhost:5000)

---

## 📌 Melhorias Futuras

* 🔒 Integração com Firebase ou SQLite para persistência.
* 📱 Suporte a dispositivos móveis.
* 🧠 Treinamento com múltiplas imagens por usuário.
* 🌐 API REST para integração com apps externos.

---

## 🧑‍💻 Autores

- Feito com 💻 por [Cleiton Fratoni](https://github.com/cleitonfratoni)
- Feito com 💻 por [Matheus Gomes](https://github.com/mathgoms02)

---

