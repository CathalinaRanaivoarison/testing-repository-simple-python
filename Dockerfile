#image de base avec Python
FROM python:3.11-slim

#le dossier de travail dans le conteneur
WORKDIR /app


COPY requirements.txt .

#installation des dépendances Python
RUN pip install --no-cache-dir --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

#Copie le reste du code
COPY  . .

# Variable d'environnement pour que le code fonctionne partout
ENV PYTHONPATH="${PYTHONPATH}:/app"

#Exposition du port 8888 (défini dans app.py)
EXPOSE 8888

# En local
#CMD [ "python", "app.py" ]

# En prod
CMD ["gunicorn", "-b", "0.0.0.0:8888", "src:application", "-w", "4", "--threads", "2"]