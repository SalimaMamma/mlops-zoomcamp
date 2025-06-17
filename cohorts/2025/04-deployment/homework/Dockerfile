FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

WORKDIR /app


COPY starter.py .

# Installer les dépendances requises (scikit-learn, pandas, pyarrow)
RUN pip install pandas pyarrow scikit-learn==1.6.1

# Commande par défaut : lancer le script avec des arguments
ENTRYPOINT ["python", "starter.py"]
