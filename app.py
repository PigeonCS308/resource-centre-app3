from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "kunci_rahsia_pusat_sumber"

STUDENT_CODES = {
    #Hari Isnin
    "Z6G1": {"nama": "Mahirah", "kelas": "4 FIRDAUS 1", "hari": "Isnin"},
    "F17A": {"nama": "Nazihah", "kelas": "4 FRIDAUS 1", "hari": "Isnin"},
    "A43L": {"nama": "Aqilah Amiruddin", "kelas": "N/A", "hari": "Isnin"},
    "PQ22": {"nama": "Sapihie", "kelas": "1 FIRDAUS 2", "hari": "Isnin"},
    "U3F8": {"nama": "Adnan", "kelas": "5 FIRDAUS 1", "hari": "Isnin"},
    "MT70": {"nama": "Zuhaily", "kelas": "2 FIRDAUS 3", "hari": "Isnin"},
    "AJ33": {"nama": "Azan", "kelas": "2 FIRDAUS 1", "hari": "Isnin"},
    "G2N1": {"nama": "Hilmi", "kelas": "1 FIRDAUS 2", "hari": "Isnin"},
    "HI19": {"nama": "Izzati", "kelas": "3 FIRDAUS 1", "hari": "Isnin"},
    #Hari Selasa
    "C6V1": {"nama": "Daennisyah", "kelas": "4 FIRDAUS 1", "hari": "Selasa"},
    "VK09": {"nama": "Elliesyah", "kelas": "1 FIRDAUS 1", "hari": "Selasa"},
    "04YT": {"nama": "Faiz", "kelas": "1 FIRDAUS 4", "hari": "Selasa"},
    "O2PI": {"nama": "Anna Mary", "kelas": "1 FIRDAUS 3", "hari": "Selasa"},
    "34FD": {"nama": "Taufiq", "kelas": "2 FIRDAUS 2", "hari": "Selasa"},
    "MC78": {"nama": "Syed Asyraf", "kelas": "3 FIRDAUS 1", "hari": "Selasa"},
    "CR07": {"nama": "Alif Farhan", "kelas": "1 FIRDAUS 2", "hari": "Selasa"},
    "HA15": {"nama": "Kahar", "kelas": "2 FIRDAUS 1", "hari": "Selasa"},
    "NR12": {"nama": "Ryan", "kelas": "2 FIRDAUS 1", "hari": "Selasa"},
    #Hari Rabu
    "EG89": {"nama": "Ummu Umairah", "kelas": "5 FIRDAUS 2", "hari": "Rabu"},
    "EP09": {"nama": "Zahin", "kelas": "5 FIRDAUS 2", "hari": "Rabu"},
    "67YU": {"nama": "Aryan", "kelas": "3 FIRDAUS 1", "hari": "Rabu"},
    "IX89": {"nama": "Nurahman", "kelas": "3 FIRDAUS 2", "hari": "Rabu"},
    "1AI2": {"nama": "Azzry", "kelas": "3 FIRDAUS 1", "hari": "Rabu"},
    "RK83": {"nama": "Qayyum", "kelas": "2 FIRDAUS 1", "hari": "Rabu"},
    "80IQ": {"nama": "Putra", "kelas": "N/A", "hari": "Rabu"},
    "LD42": {"nama": "Zahazan", "kelas": "3 FIRDAUS 1", "hari": "Rabu"},
    #Hari Khamis
    "HG74": {"nama": "Norliyana", "kelas": "5 FIRDAUS 1", "hari": "Khamis"},
    "G7H8": {"nama": "Azlianah", "kelas": "5 FIRDAUS 1", "hari": "Khamis"},
    "AA70": {"nama": "Aeron", "kelas": "N/A", "hari": "Khamis"},
    "SD91": {"nama": "Azrul", "kelas": "N/A", "hari": "Khamis"},
    "AS01": {"nama": "Daniel Wazir", "kelas": "3 FIRDAUS 4", "hari": "Khamis"},
    "FB77": {"nama": "Muzaffar", "kelas": "3 FIRDAUS 1", "hari": "Khamis"},
    "9HF1": {"nama": "Aqil", "kelas": "5 FIRDAUS 2", "hari": "Khamis"},
    "XZ83": {"nama": "Alif Ramadani", "kelas": "N/A", "hari": "Khamis"},
    "HM48": {"nama": "Syed Amirul", "kelas": "3 FIRDAUS 1", "hari": "Khamis"},
    #Hari Jumaat
    "I9J0": {"nama": "Hikmatul", "kelas": "5 FIRDAUS 1", "hari": "Jumaat"},
    "VC12": {"nama": "Aqilah Ismail", "kelas": "2 FIRDAUS 1", "hari": "Jumaat"},
    "GI89": {"nama": "Khairunnisa", "kelas": "1 FIRDAUS 1", "hari": "Jumaat"},
    "EC00": {"nama": "Azzaliah", "kelas": "4 FIRDAUS 2", "hari": "Jumaat"},
    "01ZZ": {"nama": "Ummu Sumaiyah", "kelas": "2 FIRDAUS 2", "hari": "Jumaat"},
    "PS05": {"nama": "Alleiya Alleisyah", "kelas": "2 FIRDAUS 2", "hari": "Jumaat"},
    "PJ40": {"nama": "Nurqaseh", "kelas": "1 FIRDAUS 1", "hari": "Jumaat"},
    "UI09": {"nama": "Afifah", "kelas": "3 FIRDAUS 1", "hari": "Jumaat"},
    "MA73": {"nama": "Najwa", "kelas": "1 FIRDAUS 1", "hari": "Jumaat"},
}

ADMIN_CODES = {
    "A2DM": {"nama": "Fithree Firman", "peranan": "Guru PSS"},
    "C1OM": {"nama": "Hikmatul", "peranan": "Ketua Murid PSS"},
    "MRP7": {"nama": "Syed Asyraf", "peranan": "Pembangun"},
}

HARI_MALAY = {
    "Monday": "Isnin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Khamis",
    "Friday": "Jumaat",
    "Saturday": "Sabtu",
    "Sunday": "Ahad"
}

LOG_FILE = "attendance.json"

# Fungsi untuk mengosongkan log jika hari/tarikh sudah berganti
def check_and_reset_daily_log():
    if not os.path.exists(LOG_FILE):
        return

    today_str = datetime.now().strftime("%Y-%m-%d")
    logs = load_attendance()
    
    if logs:
        # Ambil tarikh daripada rekod terkini
        last_log_date = logs[-1].get("masa", "").split(" ")[0]
        
        # Jika tarikh rekod tidak sama dengan tarikh hari ini, kosongkan fail
        if last_log_date and last_log_date != today_str:
            with open(LOG_FILE, "w") as f:
                json.dump([], f)

def save_attendance(entry):
    logs = load_attendance()
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def load_attendance():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

@app.route("/", methods=["GET", "POST"])
def index():
    check_and_reset_daily_log()  # Semak pertukaran tarikh setiap kali halaman diakses
    
    if request.method == "POST":
        code = request.form.get("code", "").strip().upper()
        
        if code in STUDENT_CODES:
            student = STUDENT_CODES[code]
            
            today_en = datetime.now().strftime("%A")
            today_name = HARI_MALAY.get(today_en, today_en)
            
            if student["hari"] != today_name:
                flash(f"Capaian Ditolak: Anda Bertugas Pada Hari {student['hari']}. Hari ini ialah hari {today_name}.", "error")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = {
                    "nama": student["nama"],
                    "kelas": student["kelas"],
                    "kod": code,
                    "hari": today_name,
                    "masa": timestamp
                }
                save_attendance(log_entry)
                flash(f"Selamat datang, {student['nama']}! Kehadiran anda untuk hari {today_name} telah direkodkan.", "success")
            return redirect(url_for("index"))
            
        elif code in ADMIN_CODES:
            return redirect(url_for("dashboard", admin_code=code))
            
        else:
            flash("Kod 4-aksara tidak sah. Sila cuba lagi.", "error")
            return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    check_and_reset_daily_log()  # Resets log automatically if date changes
    
    admin_code = request.args.get("admin_code")
    if not admin_code or admin_code not in ADMIN_CODES:
        flash("Capaian tidak dibenarkan. Sila masukkan kod pentadbir yang sah di halaman utama.", "error")
        return redirect(url_for("index"))
        
    admin_info = ADMIN_CODES[admin_code]
    logs = load_attendance()
    # Pass admin_code into the template so the button URL knows who is logged in
    return render_template("dashboard.html", admin=admin_info, logs=logs, admin_code=admin_code)


@app.route("/clear_logs")
def clear_logs():
    admin_code = request.args.get("admin_code")
    if admin_code in ADMIN_CODES:
        with open(LOG_FILE, "w") as f:
            json.dump([], f)
        flash("Senarai kehadiran telah dikosongkan.", "success")
        return redirect(url_for("dashboard", admin_code=admin_code))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)