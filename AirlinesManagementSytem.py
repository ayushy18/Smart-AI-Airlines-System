import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pymysql
import re

# Try importing fpdf for receipt generation
try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

# Try importing qrcode and PIL for QR generation
try:
    import qrcode
    from PIL import Image, ImageTk
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

class Airline:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart AI Airlines System")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.configure(bg="#ecf0f1")

        # Database Configuration 
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_pass = "@#A1y2u3s4h5#@1943"
        self.db_name = "rec"

        # ==========================================
        # STYLING
        # ==========================================
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook.Tab', font=('Arial', 14, 'bold'), padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', '#3498db')], foreground=[('selected', 'white')])
        style.configure('TFrame', background='#ecf0f1')
        style.configure('Card.TFrame', background='white', borderwidth=2, relief='groove')
        style.configure('Header.TLabel', background='white', font=('Arial', 18, 'bold'), foreground='#2c3e50')
        style.configure('Body.TLabel', background='white', font=('Arial', 14))

        # ==========================================
        # MAIN HEADER
        # ==========================================
        header_frame = tk.Frame(self.root, bg="#2c3e50", pady=20)
        header_frame.pack(fill="x", side="top")
        
        titleLabel = tk.Label(
            header_frame, text="Smart AI Airlines System", bg="#2c3e50", fg="white", font=("Arial", 35, "bold")
        )
        titleLabel.pack()

        # ==========================================
        # TABBED INTERFACE (Notebook)
        # ==========================================
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=30, pady=20)

        self.tab_booking = ttk.Frame(self.notebook, style='TFrame')
        self.tab_chat = ttk.Frame(self.notebook, style='TFrame')

        self.notebook.add(self.tab_booking, text="  ✈️ Flight Booking  ")
        self.notebook.add(self.tab_chat, text="  🤖 AI Assistant  ")

        self.setup_booking_tab()
        self.setup_chat_tab()
        self.showFlight()

    # ==========================================
    # TAB 1: BOOKING & FLIGHT LIST
    # ==========================================
    def setup_booking_tab(self):
        form_frame = ttk.Frame(self.tab_booking, style='Card.TFrame')
        form_frame.place(relx=0.02, rely=0.05, relwidth=0.35, relheight=0.85)

        ttk.Label(form_frame, text="Reserve a Seat", style='Header.TLabel').pack(pady=(30, 20))

        input_container = tk.Frame(form_frame, bg="white")
        input_container.pack(pady=20, padx=30, fill="x")

        ttk.Label(input_container, text="Flight No:", style='Body.TLabel').grid(row=0, column=0, pady=20, sticky="w")
        self.fNoIn = ttk.Entry(input_container, font=("Arial", 14), width=15)
        self.fNoIn.grid(row=0, column=1, pady=20, padx=10)

        ttk.Label(input_container, text="Your Name:", style='Body.TLabel').grid(row=1, column=0, pady=20, sticky="w")
        self.nameIn = ttk.Entry(input_container, font=("Arial", 14), width=15)
        self.nameIn.grid(row=1, column=1, pady=20, padx=10)

        ttk.Label(input_container, text="Passport No:", style='Body.TLabel').grid(row=2, column=0, pady=20, sticky="w")
        self.idIn = ttk.Entry(input_container, font=("Arial", 14), width=15)
        self.idIn.grid(row=2, column=1, pady=20, padx=10)

        tk.Button(
            form_frame, text="Confirm Booking", command=self.reserve, bg="#27ae60", fg="white", 
            activebackground="#2ecc71", activeforeground="white", bd=0, font=("Arial", 16, "bold"), pady=10, cursor="hand2"
        ).pack(fill="x", padx=40, pady=30)

        list_frame = ttk.Frame(self.tab_booking, style='Card.TFrame')
        list_frame.place(relx=0.4, rely=0.05, relwidth=0.58, relheight=0.85)

        ttk.Label(list_frame, text="Available Flights (Click to select)", style='Header.TLabel').pack(pady=(30, 10))

        header_text = f"{'Flight':<8} {'Price':<8} {'Seats':<6} {'Origin':<12} {'Destination':<12} {'Type'}"
        header_lbl = tk.Label(list_frame, text=header_text, font=("Consolas", 14, "bold"), bg="#dfe6e9", fg="#2d3436", anchor="w", padx=10)
        header_lbl.pack(fill="x", padx=30)

        scroll_frame = tk.Frame(list_frame, bg="white")
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side="right", fill="y")

        self.list = tk.Listbox(
            scroll_frame, font=("Consolas", 14), bg="#34495e", fg="white", selectbackground="#e74c3c",
            yscrollcommand=scrollbar.set, bd=0, highlightthickness=0
        )
        self.list.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.list.yview)
        self.list.bind("<<ListboxSelect>>", self.on_flight_select)

    def on_flight_select(self, event):
        try:
            selected_item = self.list.get(self.list.curselection()[0])
            flight_no = selected_item.split()[0] 
            self.fNoIn.delete(0, tk.END)
            self.fNoIn.insert(0, flight_no)
        except IndexError:
            pass 

    # ==========================================
    # TAB 2: ADVANCED CHAT UI & NLP 
    # ==========================================
    def setup_chat_tab(self):
        chat_container = tk.Frame(self.tab_chat, bg="#ffffff", bd=2, relief="groove")
        chat_container.pack(fill="both", expand=True, padx=50, pady=30) 

        header = tk.Frame(chat_container, bg="#3498db", pady=15)
        header.pack(fill="x", side="top")
        tk.Label(header, text="🤖 Advanced AI Booking Assistant", bg="#3498db", fg="white", font=("Arial", 18, "bold")).pack()

        input_frame = tk.Frame(chat_container, bg="#bdc3c7", pady=20, padx=20)
        input_frame.pack(fill="x", side="bottom")

        type_lbl = tk.Label(input_frame, text="TYPE HERE:", bg="#bdc3c7", fg="#2c3e50", font=("Arial", 14, "bold"))
        type_lbl.pack(side="left", padx=(0, 15))

        self.chat_entry = tk.Entry(input_frame, font=("Arial", 18), bd=3, relief="sunken", bg="white", fg="black")
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.chat_entry.bind("<Return>", self.handle_chat) 
        self.chat_entry.focus_set()

        send_btn = tk.Button(
            input_frame, text="SEND ➔", font=("Arial", 14, "bold"), bg="#2ecc71", fg="white", 
            bd=0, padx=20, pady=10, cursor="hand2", command=self.handle_chat
        )
        send_btn.pack(side="right")

        self.chat_history = tk.Text(
            chat_container, font=("Helvetica", 14), bg="#f5f6fa", bd=0, wrap=tk.WORD, state=tk.DISABLED, padx=20, pady=20
        )
        self.chat_history.pack(fill="both", expand=True)

        self.chat_history.tag_configure("user", foreground="#2980b9", justify="right", font=("Helvetica", 14, "bold"), spacing1=10, spacing3=10)
        self.chat_history.tag_configure("bot", foreground="#2c3e50", justify="left", font=("Helvetica", 14), spacing1=10, spacing3=10)

        self.chat_state = "idle"
        self.chat_data = {"fNo": "", "name": "", "id": "", "amount": 0}
        
        #  intro message 
        welcome_msg = (
            "👋 Welcome to Smart AI Airlines! Your seamless journey starts right here.\n"
            "Tell me what you're looking for! You can say things like:\n"
            "✈️ 'Show flights to Dubai'\n"
            "🎫 'Book flight 101'"
        )
        self.append_chat("bot", welcome_msg)

    def get_flight_details(self, flight_no):
        try:
            con = pymysql.connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, database=self.db_name)
            cur = con.cursor()
            cur.execute("SELECT amount, seats, origin, destination, flight_type FROM airline WHERE flightNo = %s", (flight_no,))
            row = cur.fetchone()
            cur.close()
            con.close()
            if row: return {"amount": row[0], "seats": row[1], "origin": row[2], "destination": row[3], "type": row[4]}
            return None
        except Exception as e: return "error"

    def analyze_db_query(self, query):
        try:
            con = pymysql.connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, database=self.db_name)
            cur = con.cursor()
            q_lower = query.lower()
            
            if "cheapest" in q_lower or "lowest" in q_lower:
                cur.execute("SELECT * FROM airline WHERE seats > 0 ORDER BY amount ASC LIMIT 1")
                row = cur.fetchone()
                if row: return f"The cheapest available flight is **Flight {row[0]}** from {row[3]} ➔ {row[4]} ({row[5]}). It costs **${row[1]}** with {row[2]} seats left."

            match = re.search(r'\b(to|from|for)\s+([a-zA-Z\s]+)', q_lower)
            if match:
                raw_city = match.group(2).replace("please", "").replace("today", "").replace("tomorrow", "").strip()
                city = raw_city.title()
                
                cur.execute("SELECT * FROM airline WHERE origin LIKE %s OR destination LIKE %s", (f"%{city}%", f"%{city}%"))
                data = cur.fetchall()
                
                if data:
                    response = f"Here are the flights I found for **{city}**:\n\n"
                    for row in data: 
                        response += f"✈️ **Flight {row[0]}**: {row[3]} ➔ {row[4]} ({row[5]}) | Price: ${row[1]} | Seats: {row[2]}\n"
                    response += "\nType 'book [flight number]' to reserve!"
                    return response
                else:
                    return f"Sorry, I couldn't find any currently available flights for '{city}'."

            words = [w.strip("?!.,") for w in query.split() if len(w) > 2]
            ignore_words = ["show", "me", "flights", "flight", "what", "is", "are", "book", "check", "available", "the", "for", "to", "from", "any", "all"]
            search_terms = [w.capitalize() for w in words if w.lower() not in ignore_words]
            
            if search_terms:
                for term in search_terms:
                    cur.execute("SELECT * FROM airline WHERE origin LIKE %s OR destination LIKE %s OR flight_type LIKE %s", (f"%{term}%", f"%{term}%", f"%{term}%"))
                    data = cur.fetchall()
                    if data:
                        response = f"Here are the flights I found for '{term}':\n\n"
                        for row in data: response += f"✈️ **Flight {row[0]}**: {row[3]} ➔ {row[4]} ({row[5]}) | Price: ${row[1]} | Seats: {row[2]}\n"
                        response += "\nType 'book [flight number]' to reserve!"
                        return response
            return None
            
        except Exception as e: 
            return f"Database error: {e}"
        finally:
            if 'con' in locals(): con.close()

    def get_all_flights_for_chat(self):
        try:
            con = pymysql.connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, database=self.db_name)
            cur = con.cursor()
            cur.execute("SELECT * FROM airline")
            data = cur.fetchall()
            cur.close()
            con.close()
            if not data: return "There are currently no flights available in the database."
            response = "Here are our currently available flights:\n\n"
            for row in data: response += f"✈️ **Flight {row[0]}**: {row[3]} ➔ {row[4]} ({row[5]}) | Price: ${row[1]} | Seats: {row[2]}\n"
            response += "\nType 'book [flight number]' to reserve a seat!"
            return response
        except Exception as e: return f"Sorry, I couldn't retrieve the flights due to an error: {e}"

    def process_flight_selection(self, f_no):
        self.append_chat("bot", f"Checking availability for Flight {f_no}...")
        details = self.get_flight_details(f_no)
        if details == "error":
            self.append_chat("bot", "Sorry, I am having trouble connecting to the database right now."); self.chat_state = "idle"
        elif details is None:
            self.append_chat("bot", f"Flight {f_no} does not exist in our system. Please check the available flights."); self.chat_state = "idle"
        else:
            if details["seats"] <= 0:
                self.append_chat("bot", f"Unfortunately, Flight {f_no} from {details['origin']} to {details['destination']} is fully booked."); self.chat_state = "idle"
            else:
                self.chat_data["fNo"] = f_no; self.chat_data["amount"] = details["amount"]; self.chat_state = "ask_name"
                self.append_chat("bot", f"Good news! **Flight {f_no}** from **{details['origin']}** ➔ **{details['destination']}** ({details['type']}) has {details['seats']} seats available. The ticket price is **${details['amount']}**. \n\nWhat is your **Full Name** for the reservation?")

    def handle_chat(self, event=None):
        user_msg = self.chat_entry.get().strip()
        if not user_msg: return
        self.chat_entry.delete(0, tk.END)
        self.append_chat("user", user_msg)
        msg_lower = user_msg.lower()

        if msg_lower == "cancel" and self.chat_state != "idle":
            self.chat_state = "idle"; self.chat_data = {"fNo": "", "name": "", "id": "", "amount": 0}
            self.append_chat("bot", "Booking process cancelled. Let me know if you need anything else."); return

        if self.chat_state == "idle":
            if "help" in msg_lower or "options" in msg_lower:
                help_text = ("Here is what I can do:\n• 'Show flights'\n• 'Flights to [City]'\n• 'Cheapest flight'\n• 'Book [Flight No]'\n• 'Check [Flight No]'\n• 'Cancel'")
                self.append_chat("bot", help_text)
            elif any(w in msg_lower for w in ["check", "status", "info"]):
                match = re.search(r'\d+', user_msg)
                if match:
                    f_no = match.group(); details = self.get_flight_details(f_no)
                    if details == "error": self.append_chat("bot", "Database error occurred.")
                    elif details is None: self.append_chat("bot", f"I couldn't find Flight {f_no} in our system.")
                    else: self.append_chat("bot", f"**Flight {f_no}** ({details['origin']} ➔ {details['destination']}, {details['type']}) has **{details['seats']} seats** left. The ticket price is **${details['amount']}**.")
                else: self.append_chat("bot", "Which flight would you like to check? (e.g., type 'check 101')")
            elif any(w in msg_lower for w in ["book", "reserve", "ticket", "new flight"]):
                match = re.search(r'\d+', user_msg)
                if match: self.process_flight_selection(match.group())
                else: self.chat_state = "ask_fno"; self.append_chat("bot", "Excellent! Please type the **Flight Number** you wish to book (e.g., 101).")
            elif any(w in msg_lower for w in ["hi", "hello", "hey"]):
                self.append_chat("bot", "Hi there! I can help you search for flights or book a ticket. Try asking 'What is the cheapest flight?' or type 'help'.")
            elif any(phrase in msg_lower for phrase in ["show all flights", "show me all the flights", "show me all flights", "show flights", "list all flights"]):
                flights_text = self.get_all_flights_for_chat()
                self.append_chat("bot", flights_text)
                self.showFlight()
            else:
                analysis_result = self.analyze_db_query(user_msg)
                if analysis_result: self.append_chat("bot", analysis_result)
                elif any(w in msg_lower for w in ["show", "available", "flight", "list", "all"]):
                    flights_text = self.get_all_flights_for_chat(); self.append_chat("bot", flights_text); self.showFlight() 
                else: self.append_chat("bot", "I didn't quite catch that. Try saying 'flights to Mumbai', 'cheapest flight', or 'show all flights'.")

        elif self.chat_state == "ask_fno":
            match = re.search(r'\d+', user_msg)
            if not match: self.append_chat("bot", "I didn't catch a valid flight number. Please type just the flight number, or type 'cancel'."); return
            self.process_flight_selection(match.group())
        elif self.chat_state == "ask_name":
            self.chat_data["name"] = user_msg.title(); self.chat_state = "ask_id"
            self.append_chat("bot", f"Thank you, {self.chat_data['name']}. Finally, please provide your **Passport Number**.")
        elif self.chat_state == "ask_id":
            self.chat_data["id"] = user_msg.upper(); self.chat_state = "confirm_booking"
            summary = (f"Please review your booking details:\n- Flight No: {self.chat_data['fNo']}\n- Passenger Name: {self.chat_data['name']}\n- Passport: {self.chat_data['id']}\n- Total Cost: ${self.chat_data['amount']}\n\nType **'yes'** to confirm and proceed to payment, or **'no'** to cancel.")
            self.append_chat("bot", summary)
        elif self.chat_state == "confirm_booking":
            if "yes" in msg_lower or "y" in msg_lower:
                self.append_chat("bot", "Redirecting to Secure Payment Gateway...")
                self.open_payment_gateway(self.chat_data["fNo"], self.chat_data["name"], self.chat_data["id"], self.chat_data["amount"], is_chat=True)
            else:
                self.append_chat("bot", "Booking cancelled. Let me know when you are ready to try again.")
                self.chat_state = "idle"; self.chat_data = {"fNo": "", "name": "", "id": "", "amount": 0}

    def append_chat(self, sender, text):
        self.chat_history.config(state=tk.NORMAL)
        if sender == "user": self.chat_history.insert(tk.END, f"{text}  \n", "user")
        else: self.chat_history.insert(tk.END, f"🤖  {text}\n\n", "bot")
        self.chat_history.see(tk.END); self.chat_history.config(state=tk.DISABLED)

    # ==========================================
    # PDF RECEIPT GENERATOR
    # ==========================================
    def generate_pdf_receipt(self, f_no, name, p_no, amount, method):
        if not FPDF_AVAILABLE:
            messagebox.showwarning("Feature Unavailable", "PDF generation requires the 'fpdf' library.\nPlease run: pip install fpdf")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"Flight_Ticket_{f_no}_{name.replace(' ', '_')}.pdf",
            title="Save Your E-Ticket & Receipt",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not filepath:
            return 
            
        try:
            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_fill_color(15, 23, 42)
            pdf.rect(0, 0, 210, 40, 'F')
            
            pdf.set_font("Arial", 'B', 24)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 15, "SMART AI AIRLINES", ln=True, align='C')
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, "Official E-Ticket & Payment Receipt", ln=True, align='C')
            
            pdf.ln(20)
            pdf.set_text_color(0, 0, 0)
            
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Passenger Details", border="B", ln=True)
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, "Passenger Name:")
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, name, ln=True)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, "Passport Number:")
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, p_no, ln=True)
            
            pdf.ln(10)
            
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Flight Information", border="B", ln=True)
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, "Flight Number:")
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, str(f_no), ln=True)
            
            pdf.ln(10)
            
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Payment Summary", border="B", ln=True)
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, "Total Amount Paid:")
            pdf.set_text_color(16, 185, 129)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, f"${amount} USD", ln=True)
            pdf.set_text_color(0, 0, 0)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, "Payment Method:")
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, method, ln=True)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(50, 10, "Booking Status:")
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(16, 185, 129)
            pdf.cell(0, 10, "CONFIRMED & SECURED", ln=True)
            
            pdf.set_y(-30)
            pdf.set_text_color(128, 128, 128)
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 10, "Thank you for flying with Smart AI Airlines. Have a safe journey!", align='C')

            pdf.output(filepath)
            messagebox.showinfo("Success", f"Your E-Ticket has been successfully downloaded!")
            
        except Exception as e:
            messagebox.showerror("PDF Error", f"Failed to generate receipt: {e}")

    # ==========================================
    # HORIZONTAL PAYMENT GATEWAY UI
    # ==========================================
    def open_payment_gateway(self, f_no, name, p_no, amount, is_chat=False):
        self.pay_win = tk.Toplevel(self.root)
        self.pay_win.title("Secure Checkout - Smart AI Airlines")
        
        self.pay_win.geometry("900x580") 
        self.pay_win.configure(bg="#f4f6f9") 
        self.pay_win.grab_set() 
        self.pay_win.resizable(False, False)

        header_frame = tk.Frame(self.pay_win, bg="#0f172a", pady=15)
        header_frame.pack(side="top", fill="x")
        tk.Label(header_frame, text="🔒 Secure Checkout", font=("Helvetica", 20, "bold"), bg="#0f172a", fg="white").pack()
        tk.Label(header_frame, text="Smart AI Airlines Payment Portal", font=("Helvetica", 11), bg="#0f172a", fg="#94a3b8").pack(pady=(2,0))

        summary_frame = tk.Frame(self.pay_win, bg="white", bd=1, relief="solid")
        summary_frame.pack(side="top", fill="x", padx=30, pady=15)
        
        sf_inner = tk.Frame(summary_frame, bg="white", padx=20, pady=10)
        sf_inner.pack(fill="both")
        
        tk.Label(sf_inner, text=f"Flight: {f_no}", font=("Helvetica", 12, "bold"), bg="white", fg="#1e293b").pack(side="left", padx=20)
        tk.Label(sf_inner, text=f"Passenger: {name}", font=("Helvetica", 12, "bold"), bg="white", fg="#1e293b").pack(side="left", padx=20)
        
        amount_frame = tk.Frame(sf_inner, bg="white")
        amount_frame.pack(side="right", padx=20)
        tk.Label(amount_frame, text="Total Due: ", font=("Helvetica", 12), bg="white", fg="#64748b").pack(side="left")
        tk.Label(amount_frame, text=f"${amount}", font=("Helvetica", 16, "bold"), bg="white", fg="#10b981").pack(side="left")

        content_frame = tk.Frame(self.pay_win, bg="#f4f6f9")
        content_frame.pack(fill="both", expand=True, padx=30, pady=5)

        # --- LEFT COLUMN: CARD PAYMENT ---
        card_col = tk.Frame(content_frame, bg="white", bd=1, relief="solid")
        card_col.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        tk.Label(card_col, text="💳 Credit / Debit Card", bg="#f8fafc", font=("Helvetica", 14, "bold"), fg="#0f172a", pady=10).pack(fill="x")
        
        card_inner = tk.Frame(card_col, bg="white", padx=20, pady=10)
        card_inner.pack(fill="both", expand=True)

        tk.Label(card_inner, text="Card Number", bg="white", font=("Helvetica", 10, "bold"), fg="#334155").pack(anchor="w", pady=(10, 5))
        card_entry = ttk.Entry(card_inner, font=("Helvetica", 13))
        card_entry.pack(fill="x", ipady=4)

        tk.Label(card_inner, text="Cardholder Name", bg="white", font=("Helvetica", 10, "bold"), fg="#334155").pack(anchor="w", pady=(10, 5))
        name_entry = ttk.Entry(card_inner, font=("Helvetica", 13))
        name_entry.insert(0, name) 
        name_entry.pack(fill="x", ipady=4)

        split_frame = tk.Frame(card_inner, bg="white")
        split_frame.pack(fill="x", pady=(10, 5))
        
        exp_frame = tk.Frame(split_frame, bg="white")
        exp_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Label(exp_frame, text="Expiry", bg="white", font=("Helvetica", 10, "bold"), fg="#334155").pack(anchor="w", pady=(0, 5))
        
        cb_frame = tk.Frame(exp_frame, bg="white")
        cb_frame.pack(fill="x")
        month_cb = ttk.Combobox(cb_frame, values=[f"{i:02d}" for i in range(1, 13)], width=3, font=("Helvetica", 12), state="readonly")
        month_cb.set("MM")
        month_cb.pack(side="left")
        tk.Label(cb_frame, text="/", bg="white", font=("Helvetica", 12)).pack(side="left")
        year_cb = ttk.Combobox(cb_frame, values=[str(i) for i in range(24, 35)], width=3, font=("Helvetica", 12), state="readonly")
        year_cb.set("YY")
        year_cb.pack(side="left")

        cvv_frame = tk.Frame(split_frame, bg="white")
        cvv_frame.pack(side="right", fill="x", expand=True, padx=(5, 0))
        tk.Label(cvv_frame, text="CVV", bg="white", font=("Helvetica", 10, "bold"), fg="#334155").pack(anchor="w", pady=(0, 5))
        cvv_entry = ttk.Entry(cvv_frame, font=("Helvetica", 13), show="•")
        cvv_entry.pack(fill="x", ipady=4)

        tk.Button(
            card_inner, text=f"Pay ${amount} via Card ➔", 
            command=lambda: self.process_card_payment(f_no, name, p_no, amount, is_chat, card_entry.get(), f"{month_cb.get()}/{year_cb.get()}", cvv_entry.get()),
            bg="#10b981", fg="white", activebackground="#059669", activeforeground="white", 
            font=("Helvetica", 12, "bold"), bd=0, pady=8, cursor="hand2"
        ).pack(fill="x", side="bottom", pady=15)


        # --- RIGHT COLUMN: UPI PAYMENT (TABBED) ---
        upi_col = tk.Frame(content_frame, bg="white", bd=1, relief="solid")
        upi_col.pack(side="right", fill="both", expand=True, padx=(15, 0))

        tk.Label(upi_col, text="📱 UPI / QR Payment", bg="#f8fafc", font=("Helvetica", 14, "bold"), fg="#0f172a", pady=10).pack(fill="x")

        # Create Notebook for UPI tabs
        upi_notebook = ttk.Notebook(upi_col)
        upi_notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # ---- Tab 1: Manual UPI ID ----
        tab_upi_id = tk.Frame(upi_notebook, bg="white", padx=15, pady=20)
        upi_notebook.add(tab_upi_id, text=" Enter UPI ID ")

        tk.Label(tab_upi_id, text="Virtual Payment Address (VPA)", bg="white", font=("Helvetica", 10, "bold"), fg="#334155").pack(anchor="w", pady=(15, 5))
        upi_entry = ttk.Entry(tab_upi_id, font=("Helvetica", 13))
        upi_entry.insert(0, "username@bank")
        upi_entry.pack(fill="x", ipady=4, pady=(0, 20))

        tk.Button(
            tab_upi_id, text=f"Pay ${amount} via UPI ➔", 
            command=lambda: self.process_upi_payment(f_no, name, p_no, amount, is_chat, upi_entry.get()),
            bg="#3b82f6", fg="white", activebackground="#2563eb", activeforeground="white", 
            font=("Helvetica", 12, "bold"), bd=0, pady=8, cursor="hand2"
        ).pack(fill="x", side="bottom", pady=15)

        # ---- Tab 2: Scan QR Code ----
        tab_qr = tk.Frame(upi_notebook, bg="white", padx=10, pady=10)
        upi_notebook.add(tab_qr, text=" Scan QR Code ")

        qr_frame = tk.Frame(tab_qr, bg="#f8fafc", bd=1, relief="solid")
        qr_frame.pack(pady=10, expand=True)

        if QR_AVAILABLE:
            # Generate a UPI deep-link string dynamically
            upi_link = f"upi://pay?pa=airlines@bank&pn=Smart%20AI%20Airlines&am={amount}&cu=USD"
            
            # Use smaller box_size and border for a compact QR
            qr = qrcode.QRCode(version=1, box_size=3, border=1)
            qr.add_data(upi_link)
            qr.make(fit=True)
            
            # Create PIL image
            qr_img = qr.make_image(fill_color="black", back_color="#f8fafc")
            
            # Resize image explicitly to ensure it stays small (140x140 pixels)
            try:
                qr_img = qr_img.resize((140, 140), Image.Resampling.LANCZOS)
            except AttributeError:
                # Fallback for older Pillow versions
                qr_img = qr_img.resize((140, 140), Image.ANTIALIAS)

            self.qr_photo = ImageTk.PhotoImage(qr_img)
            
            tk.Label(qr_frame, image=self.qr_photo, bg="#f8fafc").pack(padx=15, pady=(15, 5))
            tk.Label(qr_frame, text="Scan with GPay / PhonePe / Paytm", bg="#f8fafc", fg="#475569", font=("Helvetica", 9)).pack(pady=(0, 15))
        else:
            tk.Label(qr_frame, text="[ 🔲 ]\nScan with GPay/PhonePe\n(Please pip install qrcode pillow)", bg="#f8fafc", fg="#475569", font=("Helvetica", 10), width=25, height=3).pack(padx=10, pady=10)

        # Footer
        footer_frame = tk.Frame(self.pay_win, bg="#f4f6f9")
        footer_frame.pack(side="bottom", fill="x", pady=10)
        tk.Label(footer_frame, text="🔒 256-bit SSL Encryption | 100% Secure Payment", font=("Helvetica", 9), fg="#94a3b8", bg="#f4f6f9").pack()

    def process_card_payment(self, f_no, name, p_no, amount, is_chat, card, exp, cvv):
        if not card or "MM" in exp or "YY" in exp or not cvv:
            messagebox.showerror("Payment Error", "All card payment fields are required.", parent=self.pay_win)
            return
        if len(card.replace(" ", "")) < 16:
            messagebox.showerror("Payment Error", "Invalid Card Number. Must be at least 16 digits.", parent=self.pay_win)
            return

        messagebox.showinfo("Processing", "Card Payment Approved! Processing your booking...", parent=self.pay_win)
        self.pay_win.destroy()
        self.finalize_booking(f_no, name, p_no, amount, is_chat, method="Credit/Debit Card")

    def process_upi_payment(self, f_no, name, p_no, amount, is_chat, upi_id):
        if not upi_id or upi_id == "username@bank":
            messagebox.showerror("Payment Error", "Please enter a valid UPI ID to proceed.", parent=self.pay_win)
            return
        if "@" not in upi_id:
            messagebox.showerror("Payment Error", "Invalid UPI ID format. It should contain an '@' symbol.", parent=self.pay_win)
            return

        messagebox.showinfo("Processing", "UPI Request sent to your app.\nPayment Approved! Processing your booking...", parent=self.pay_win)
        self.pay_win.destroy()
        self.finalize_booking(f_no, name, p_no, amount, is_chat, method="UPI")

    def finalize_booking(self, f_no, name, p_no, amount, is_chat, method):
        try:
            con = pymysql.connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, database=self.db_name)
            cur = con.cursor()

            cur.execute("SELECT seats FROM airline WHERE flightNo = %s", (f_no,))
            row = cur.fetchone()
            
            if row and row[0] > 0:
                update = row[0] - 1
                cur.execute("UPDATE airline SET seats=%s WHERE flightNo=%s", (update, f_no))
                con.commit()
                self.showFlight()

                if is_chat:
                    self.append_chat("bot", f"✅ Payment of ${amount} via {method} received! Booking Successful. Please save your receipt.")
                    self.chat_state = "idle"
                    self.chat_data = {"fNo": "", "name": "", "id": "", "amount": 0}
                else:
                    messagebox.showinfo("Booking Confirmed", f"Payment Successful via {method}!\n\nSeat Reserved in Flight No: {f_no}\nFor {name}")
                    self.fNoIn.delete(0, tk.END)
                    self.nameIn.delete(0, tk.END)
                    self.idIn.delete(0, tk.END)
                
                self.generate_pdf_receipt(f_no, name, p_no, amount, method)

            else:
                msg = "Sorry, the flight sold out while processing your payment."
                if is_chat: self.append_chat("bot", msg)
                else: messagebox.showerror("Booking Failed", msg)

            cur.close()
            con.close()

        except Exception as e:
            if is_chat: self.append_chat("bot", f"Database Error during finalization: {e}")
            else: messagebox.showerror("Error", f"Error saving booking: {e}")

    # ==========================================
    # DATABASE LOGIC (Manual Booking Tab Update)
    # ==========================================
    def showFlight(self):
        try:
            con = pymysql.connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, database=self.db_name)
            cur = con.cursor()
            cur.execute("SELECT * FROM airline")
            data = cur.fetchall()
            self.list.delete(0, tk.END)

            for row in data:
                formatted_row = f"{row[0]:<8} {row[1]:<8} {row[2]:<6} {row[3]:<12} {row[4]:<12} {row[5]}"
                self.list.insert(tk.END, formatted_row)

            cur.close()
            con.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    def reserve(self):
        try: f = int(self.fNoIn.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid Flight Number."); return

        name = self.nameIn.get().strip(); pNo = self.idIn.get().strip()

        if not name or not pNo:
            messagebox.showerror("Input Error", "Name and Passport No cannot be empty."); return

        try:
            con = pymysql.connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, database=self.db_name)
            cur = con.cursor()
            cur.execute("SELECT amount, seats FROM airline WHERE flightNo = %s", (f,))
            row = cur.fetchone()

            if row is None:
                messagebox.showerror("Error", "No such flight found."); cur.close(); con.close(); return

            amount, seats = row[0], row[1]

            if seats > 0: self.open_payment_gateway(f, name, pNo, amount, is_chat=False)
            else: messagebox.showerror("Error", "All seats are reserved.")

            cur.close(); con.close()

        except Exception as e: messagebox.showerror("Error", f"Error accessing database: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    obj = Airline(root)
    root.mainloop()