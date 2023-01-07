FROM python:3.8 as installer
SHELL ["/bin/bash", "-c"]

RUN useradd -ms /bin/bash runner

ENV HOME="/home/runner"

RUN mkdir -p $HOME/.ssh/
ADD id_rsa $HOME/.ssh/id_rsa
RUN chmod 777 -R $HOME/.ssh/

USER runner

# RUN touch $HOME/.ssh/known_hosts && \
#     ssh-keyscan -t rsa github.com > $HOME/.ssh/known_hosts

ENV GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no -i $HOME/.ssh/id_rsa"

RUN pip install --upgrade pip && \
    pip install virtualenv && \
    python -m virtualenv $HOME/venv && \
    chmod 777 -R $HOME/venv

ADD package package

RUN source $HOME/venv/bin/activate && \
    pip install package/*.whl
# kognita.azurecr.io/coleta-dimovel

FROM python:3.8
SHELL ["/bin/bash", "-c"]

WORKDIR /venv
COPY --from=installer /home/runner/venv /home/runner/venv

ENV PATH="/home/runner/venv/bin:$PATH"

