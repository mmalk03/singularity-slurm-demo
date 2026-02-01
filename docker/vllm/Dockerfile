FROM vllm/vllm-openai:v0.15.0

RUN mkdir /app
COPY docker/vllm/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY demo /app/demo

WORKDIR /app
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:."
CMD ["/bin/bash"]
