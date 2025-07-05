FROM python:3.11

RUN apt-get update && apt-get install -y wget
RUN wget https://github.com/official-stockfish/Stockfish/releases/download/sf_16/stockfish-android-armv8.tar
RUN tar -xvf stockfish-android-armv8.tar
RUN mv /stockfish/stockfish-android-armv8 /usr/local/bin/stockfish
RUN rm -rf stockfish-android-armv8.tar /stockfish

ADD . /jetson-chess

RUN python3 -m pip install uv
RUN cd jetson-chess && python3 -m uv pip install -p .

CMD ["python3", "/jetson-chess/src/main.py"]
