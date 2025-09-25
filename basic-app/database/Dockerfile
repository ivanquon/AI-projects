FROM pgvector/pgvector:pg16-trixie

RUN apt-get update && apt-get install -y postgresql-server-dev-15 build-essential git curl

# Install pgvector extension
RUN git clone https://github.com/pgvector/pgvector.git /pgvector && \
    cd /pgvector && \
    make && make install

# Clean up
RUN rm -rf /pgvector && apt-get clean && rm -rf /var/lib/apt/lists/*
