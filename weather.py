import tkinter as tk
from tkinter import messagebox
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather Predictor")

        self.label = tk.Label(master, text="Enter date for weather prediction:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.predict_button = tk.Button(master, text="Predict Weather", command=self.predict_weather)
        self.predict_button.pack()

    def predict_weather(self):
        date = self.entry.get()

        try:
            if not date:
                messagebox.showerror("Error", "Please enter a date.")
            else:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You will be provided with a date. You are to predict the weather in Lagos, Nigeria for that date. You should tell the maximum and minimum temperatures for that day and if it will rain or not. Don't talk too much, just be straight to the point and say the predicted weather."
                        },
                        {
                            "role": "user",
                            "content": f"{date}"
                        }
                    ],
                    temperature=0.1,
                    max_tokens=100,
                    top_p=1
                )
                prediction = response.choices[0].message.content

                messagebox.showinfo("Prediction", f"Weather prediction for {date}: {prediction}")
        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Error", "An error occurred while generating prediction.")

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
