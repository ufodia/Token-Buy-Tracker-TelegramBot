# We're Using NaytSeyd's Special Docker
FROM naytseyd/sedenbot:j1xlte

# Working Directory
WORKDIR /Tracker_Bot/

# Clone Repo
RUN git clone -b seden https://github.com/thedeveloper12/Price_Tracker.git /Tracker_Bot/
RUN pip3 install -r requirements.txt

# Run bot
CMD ["python3", "price_tracker.py"]
