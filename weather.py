from tkinter import *
import time
import requests as req
import speech_recognition as sr
import threading

def getCurrentWeather():
    global current_label2, current_label3

    city = textField.get()

    api = "https://api.openweathermap.org/data/2.5/weather?q=" + \
          city+"&appid=06c921750b9a82d8f5d1294e1586276f"
    json_data = req.get(api).json()

    description = str(json_data["weather"][0]["description"])
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = str(json_data['main']['pressure'])
    humidity = str(json_data['main']['humidity'])
    sunrise = str(time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600)))
    sunset = str(time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600)))
    visible = str(json_data["visibility"])
    lat = str(json_data["coord"]["lat"])
    lon = str(json_data["coord"]["lon"])
    w_speed = str(json_data["wind"]["speed"])

    final_description = "{desc}\n{temp}°C".format(
        desc=description,
        temp=temp
    )

    final_info = """
    Min Temp: {min_temp}°C
    Max Temp: {max_temp}°C
    Pressure: {pressure} milibars
    Humidity: {humidity}%
    Sunrise: {sunrise} a.m.
    Sunset: {sunset} p.m.
    Visibility: {visibility} meters
    Latitude: {lat}
    Longitude: {lon}
    Wind Speed: {wind_speed} miles per hour
    """.format(
        min_temp=min_temp,
        max_temp=max_temp,
        pressure=pressure,
        humidity=humidity,
        sunrise=sunrise,
        sunset=sunset,
        visibility=visible,
        lat=lat,
        lon=lon,
        wind_speed=w_speed
    )

    current_label2.config(text=final_description)
    current_label3.config(text=final_info)


def getFutureWeather():
    global future_label2
    global future_label3

    city = textField.get()
    api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=06c921750b9a82d8f5d1294e1586276f"
    json_data = req.get(api).json()
    try:
        population = str(json_data["city"]["population"])
    except Exception:
        population = 'No information'
    lat = str(json_data["city"]["coord"]["lat"])
    lon = str(json_data["city"]["coord"]["lon"])
    sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['city']['sunrise'] - 21600))
    sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['city']['sunset'] - 21600))
    date = json_data["list"][0]["dt_txt"].split(" ")[0]
    t = json_data["list"][0]["dt_txt"].split(" ")[1]
    pressure = str(json_data["list"][0]["main"]["pressure"])
    humidity = str(json_data["list"][0]["main"]["humidity"])
    try:
        rain_in_3h = str(json_data["list"][0]["rain"]['3h']) + " mm"
    except Exception:
        rain_in_3h = 'No information available'
    description = json_data["list"][0]["weather"][0]["description"]
    w_speed = str(json_data["list"][0]["wind"]["speed"])

    final_info = "{desc}\n{temp}°C".format(
        desc=description,
        temp=int(json_data["list"][0]["main"]["temp"] - 273.15)
    )

    final_data = """
    Pressure: {pressure} milibars
    Humidity: {humidity}%
    Sunrise: {sunrise} a.m.
    Sunset: {sunset} p.m.
    Date: {date}
    Time: {time}
    Population: {population}
    Latitude: {lat}
    Longitude: {lon}
    Wind Speed: {wind_speed} miles per hour
    Forecast for Rain in Upcoming 3 hours: {rain}
    """.format(
        pressure=pressure,
        humidity=humidity,
        sunrise=sunrise,
        sunset=sunset,
        date=date,
        time=t,
        population=population,
        lat=lat,
        lon=lon,
        wind_speed=w_speed,
        rain=rain_in_3h
    )

    future_label2.config(text=final_info)
    future_label3.config(text=final_data)


def getHistoricalWeather():
    global textField_1
    global textField_2
    global hist_label2
    global hist_label3

    lat = textField_1.get()
    long = textField_2.get()
    api = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&appid=06c921750b9a82d8f5d1294e1586276f"
    json_data = req.get(api).json()

    sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data["daily"][0]["sunrise"] - 21600))
    sunset = time.strftime('%I:%M:%S', time.gmtime(json_data["daily"][0]["sunset"] - 21600))
    moonrise = time.strftime('%I:%M:%S', time.gmtime(json_data["daily"][0]["moonrise"] - 21600))
    moonset = time.strftime('%I:%M:%S', time.gmtime(json_data["daily"][0]["moonset"] - 21600))
    moon_phase = int(json_data["daily"][0]['moon_phase'] * 100)
    try:
        rain = str(json_data["daily"][0]["rain"]) + " mm"
    except Exception:
        rain = 'No information available'
    uvi = json_data["daily"][0]["uvi"]
    pressure = json_data["daily"][0]["pressure"]
    humidity = json_data["daily"][0]["humidity"]
    description = json_data["daily"][0]["weather"][0]["description"]
    w_speed = json_data["daily"][0]["wind_speed"]

    avg_temp = float(
        (int(json_data["daily"][0]["temp"]["day"] - 273.15) +
         int(json_data["daily"][0]["temp"]["night"] - 273.15)) / 2
    )

    final_info = "\n{desc}\nAverage Temperature for the day: {avg_temp}°C".format(
        desc=description,
        avg_temp=avg_temp
    )

    final_data = """
    Pressure: {pressure} milibars
    Humidity: {humidity}%
    Sunrise: {sunrise} a.m.
    Sunset: {sunset} p.m.
    Moonrise: {moonrise} p.m.
    Moonset: {moonset} a.m.
    Moonphase: {moon_phase}%
    Wind Speed: {wind_speed} miles per hour
    Rain: {rain}
    UVI Index: {uvi}
    """.format(
        pressure=pressure,
        humidity=humidity,
        sunrise=sunrise,
        sunset=sunset,
        moonrise=moonrise,
        moonset=moonset,
        moon_phase=moon_phase,
        wind_speed=w_speed,
        rain=rain,
        uvi=uvi
    )

    hist_label2.config(text=final_info)
    hist_label3.config(text=final_data)


# ── Voice input ───────────────────────────────────────────────────────────────

def speakCity(text_field, button, predict_btn):
    """Listen for city name and fill the text field. Runs in a thread."""
    def listen():
        r = sr.Recognizer()
        button.config(text="🎤 Listening...", state=DISABLED, bg="#cc6600")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=4)
            city = r.recognize_google(audio)
            city = city.strip().title()
            text_field.delete(0, END)
            text_field.insert(0, city)
            button.config(text="🎤 Speak out City Name", state=NORMAL, bg="#FF8C00")
        except sr.WaitTimeoutError:
            button.config(text="🎤 Speak out City Name", state=NORMAL, bg="#FF8C00")
        except sr.UnknownValueError:
            button.config(text="🎤 Could not hear, try again", state=NORMAL, bg="#FF8C00")
        except Exception as e:
            button.config(text="🎤 Speak out City Name", state=NORMAL, bg="#FF8C00")

    threading.Thread(target=listen, daemon=True).start()


# ── GUI ───────────────────────────────────────────────────────────────────────

canvas = Tk()
canvas.geometry("850x600")
canvas.title("Megh-Suryam")
f = ("poppins", 15, "bold")
a = ("poppins", 17, "bold")
b = ("poppins", 20, "bold")
t = ("poppins", 35, "bold")

ttl = Label(canvas, text="Megh-Suryam", justify='center',
            font=("comic", 35, "bold"), foreground='white', background='#0000FF')
ttl.pack()

canvas["bg"] = "blue"


def current():
    global textField
    global current_label2
    global current_label3

    top = Toplevel()
    top.geometry("750x700")
    top["bg"] = "#A4DE02"

    current_label1 = Label(top, text='Please enter the City Name to get the Current Prediction',
                           justify='center', width=50, font=b, background="green", foreground="white",
                           wraplength=700)
    current_label1.pack()

    textField = Entry(top, justify='center', width=20, font=t)
    textField.pack(pady=10)

    voice_btn = Button(top, text="🎤 Speak out City Name", width=22, font=f,
                       bg="#FF8C00", fg="white",
                       command=lambda: speakCity(textField, voice_btn, predict_btn))
    voice_btn.pack(pady=5)

    predict_btn = Button(top, text="Click to Predict", width=16,
                         command=getCurrentWeather, font=f)
    predict_btn.pack(pady=5)

    current_label2 = Label(top, font=a, background="#A4DE02", foreground="blue")
    current_label2.pack()
    current_label3 = Label(top, font=f, background="#A4DE02", foreground="blue")
    current_label3.pack()

    top.resizable(True, True)
    top.mainloop()


def future():
    global textField
    global future_label2
    global future_label3

    top = Toplevel()
    top.geometry("750x700")
    top["bg"] = "#A4DE02"

    future_label1 = Label(top, text='Please enter the City Name to get the Future Prediction',
                          justify='center', width=50, font=b, background="green", foreground="white",
                          wraplength=700)
    future_label1.pack()

    textField = Entry(top, justify='center', width=20, font=t)
    textField.pack(pady=10)

    voice_btn = Button(top, text="🎤 Speak out City Name", width=22, font=f,
                       bg="#FF8C00", fg="white",
                       command=lambda: speakCity(textField, voice_btn, None))
    voice_btn.pack(pady=5)

    predict_btn = Button(top, text="Click to Predict", width=16,
                         command=getFutureWeather, font=f)
    predict_btn.pack(pady=5)

    future_label2 = Label(top, font=a, background="#A4DE02", foreground="blue")
    future_label2.pack()
    future_label3 = Label(top, font=f, background="#A4DE02", foreground="blue")
    future_label3.pack()

    top.resizable(True, True)
    top.mainloop()


def hist():
    global textField_1
    global textField_2
    global hist_label2
    global hist_label3

    top = Toplevel()
    top.geometry("1450x700")
    top["bg"] = "#A4DE02"

    hist_label1 = Label(top, text='Please enter the Latitude first then the Longitude to get the Historical Prediction',
                        justify='center', width=65, font=b, background="green", foreground="white",
                        wraplength=1400)
    hist_label1.pack()

    textField_1 = Entry(top, justify='center', width=20, font=t)
    textField_1.pack(pady=20)
    textField_2 = Entry(top, justify='center', width=20, font=t)
    textField_2.pack(pady=20)

    predict_btn = Button(top, text="Click to Predict", width=16,
                         command=getHistoricalWeather, font=f)
    predict_btn.pack()

    hist_label2 = Label(top, font=a, background="#A4DE02", foreground="blue")
    hist_label2.pack()
    hist_label3 = Label(top, font=f, background="#A4DE02", foreground="blue")
    hist_label3.pack()

    top.resizable(True, True)
    top.mainloop()


Btn_1 = Button(text="Click here to visit the Current Weather Prediction Page",
               command=current, font=b)
Btn_1["bg"] = "yellow"
Btn_1.pack()
Btn_1.place(x=40, y=100)

Btn_2 = Button(text="Click here to visit the Future Weather Prediction Page",
               command=future, font=b)
Btn_2["bg"] = "yellow"
Btn_2.pack()
Btn_2.place(x=40, y=250)

Btn_3 = Button(text="Click here to visit the Historical Weather Prediction Page",
               command=hist, font=b)
Btn_3["bg"] = "yellow"
Btn_3.pack()
Btn_3.place(x=40, y=400)

canvas.resizable(True, True)
canvas.mainloop()
