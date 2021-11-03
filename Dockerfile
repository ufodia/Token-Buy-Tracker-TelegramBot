# We're Using NaytSeyd's Special Docker
FROM naytseyd/sedenbot:j1xlte

# Working Directory
WORKDIR /Price/

# Clone Repo
RUN git clone https://github.com/thedeveloper12/PriceBot.git /Price/
RUN pip3 install -r requirements.txt

# Run bot
CMD ["python3", "price_tracker.py"]
