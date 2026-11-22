FROM python:3.10-slim

# Buat user non-root dengan UID 1000 (standar Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

WORKDIR $HOME/app

COPY --chown=user requirements.txt $HOME/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . $HOME/app

# Port default Hugging Face Spaces
EXPOSE 7860

CMD ["python", "main.py"]
