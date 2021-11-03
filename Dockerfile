# We're Using NaytSeyd's Special Docker
FROM naytseyd/sedenbot:j1xlte

# Working Directory
WORKDIR /Priceee/

# Clone Repo
RUN git clone https://github.com/thedeveloper12/PriceBot.git /Priceee/
RUN pip3 install -r requirements.txt

# Run bot
CMD ["python3", "price_tracker.py"]
