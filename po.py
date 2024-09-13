import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import os


def caesar_cipher(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                start = ord('a')
            else:
                start = ord('A')
            new_char = chr(start + (ord(char) - start + shift_amount) % 26)
            encrypted_text += new_char
        else:
            encrypted_text += char
    return encrypted_text


activity_log = []


def export_to_file(file_type):
    file = filedialog.asksaveasfilename(defaultextension=f".{file_type}",
                                        filetypes=[(file_type.upper(), f"*.{file_type}")])
    if file:
        with open(file, 'w') as f:
            for log in activity_log:
                f.write(f"{log}\n")
        messagebox.showinfo("نجاح", f"تم تصدير السجل إلى ملف {file_type.upper()} بنجاح")


def show_settings_window():
    settings_window = tk.Toplevel()
    settings_window.title("الإعدادات")
    settings_window.geometry("600x400")
    settings_window.configure(bg='lightgray')

    
    how_it_works_label = tk.Label(settings_window, text="كيف يعمل التطبيق:", font=("Arial", 14), bg='lightgray')
    how_it_works_label.pack(pady=10)
    how_it_works_desc = tk.Label(settings_window, text="التطبيق يقوم بتشفير النص باستخدام تشيفر سيزر البسيط.", bg='lightgray')
    how_it_works_desc.pack(pady=5)

    
    languages_label = tk.Label(settings_window, text="اللغات المتاحة:", font=("Arial", 14), bg='lightgray')
    languages_label.pack(pady=10)

    languages_frame = tk.Frame(settings_window, bg='lightgray')
    languages_frame.pack(pady=5)

    lang_var = tk.StringVar(value="Arabic")
    lang_options = [("العربية", "Arabic"), ("English", "English")]
    for lang, val in lang_options:
        lang_radio = tk.Radiobutton(languages_frame, text=lang, variable=lang_var, value=val, bg='lightgray')
        lang_radio.pack(side="left")

    
    rate_button = tk.Button(settings_window, text="تقييم التطبيق", font=("Arial", 12), bg='black', fg='white', 
                            command=lambda: messagebox.showinfo("تقييم", "شكراً لتقييمك!"))
    rate_button.pack(pady=20)

    
    export_label = tk.Label(settings_window, text="تصدير السجل:", font=("Arial", 14), bg='lightgray')
    export_label.pack(pady=10)

    export_frame = tk.Frame(settings_window, bg='lightgray')
    export_frame.pack(pady=5)

    export_txt_button = tk.Button(export_frame, text="تصدير كملف نصي", font=("Arial", 12), bg='black', fg='white', 
                                  command=lambda: export_to_file("txt"))
    export_txt_button.pack(side="left", padx=5)

    export_pdf_button = tk.Button(export_frame, text="تصدير كملف PDF", font=("Arial", 12), bg='black', fg='white', 
                                  command=lambda: export_to_file("pdf"))
    export_pdf_button.pack(side="left", padx=5)

    
    log_label = tk.Label(settings_window, text="سجل الأنشطة:", font=("Arial", 14), bg='lightgray')
    log_label.pack(pady=10)

    log_text = tk.Text(settings_window, height=8, width=50)
    log_text.pack(pady=5)

    for log in activity_log:
        log_text.insert(tk.END, log + "\n")
    log_text.config(state=tk.DISABLED)


def add_tooltip(widget, text):
    tooltip = tk.Label(widget, text=text, bg='yellow', relief='solid', bd=1, font=("Arial", 10))
    tooltip.place_forget()

    def on_enter(event):
        tooltip.place(x=event.x_root - widget.winfo_rootx(), y=event.y_root - widget.winfo_rooty() + 20)

    def on_leave(event):
        tooltip.place_forget()

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def show_main_screen():
    main_screen = tk.Tk()
    main_screen.title("الشاشة الرئيسية")
    main_screen.geometry("800x600")  
    main_screen.configure(bg='lightgray')

    
    frame = tk.Frame(main_screen, bg='lightgray')
    frame.pack(expand=True)

    
    message_label = tk.Label(frame, text="النص للتشفير:", font=("Arial", 14), bg='lightgray', fg='black')
    message_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")
    message_entry = tk.Entry(frame, width=50)
    message_entry.grid(row=0, column=1, pady=10, padx=10)

    
    def encrypt_text():
        text = message_entry.get()
        shift = 3  
        encrypted_text = caesar_cipher(text, shift)
        encrypted_text_display.config(state=tk.NORMAL)
        encrypted_text_display.delete(1.0, tk.END)
        encrypted_text_display.insert(tk.END, encrypted_text)
        encrypted_text_display.config(state=tk.DISABLED)
        activity_log.append(f"تم التشفير: {text} -> {encrypted_text} في {datetime.now()}")

    encrypt_button = tk.Button(frame, text="تشفير", font=("Arial", 12), bg='black', fg='white', command=encrypt_text)
    encrypt_button.grid(row=1, column=0, pady=10, padx=10, columnspan=2)
    add_tooltip(encrypt_button, "انقر لتشفير النص")

    
    encrypted_text_display = tk.Text(frame, height=4, width=50, wrap=tk.WORD, state=tk.DISABLED)
    encrypted_text_display.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    
    password_label = tk.Label(frame, text="كلمة المرور:", font=("Arial", 14), bg='lightgray', fg='black')
    password_label.grid(row=3, column=0, pady=10, padx=10, sticky="e")
    password_entry = tk.Entry(frame, width=50, show='*')
    password_entry.grid(row=3, column=1, pady=10, padx=10)

    
    def decrypt_text():
        encrypted_text = encrypted_text_display.get("1.0", tk.END).strip()
        shift = 3  
        decrypted_text = caesar_cipher(encrypted_text, -shift)
        messagebox.showinfo("نص مفكوك", decrypted_text)
        activity_log.append(f"تم فك التشفير: {encrypted_text} -> {decrypted_text} في {datetime.now()}")

    decrypt_button = tk.Button(frame, text="فك التشفير", font=("Arial", 12), bg='black', fg='white', command=decrypt_text)
    decrypt_button.grid(row=4, column=0, pady=10, padx=10, columnspan=2)
    add_tooltip(decrypt_button, "انقر لفك التشفير")

    
    def copy_text():
        encrypted_text = encrypted_text_display.get("1.0", tk.END).strip()
        main_screen.clipboard_clear()
        main_screen.clipboard_append(encrypted_text)
        messagebox.showinfo("نسخ", "تم نسخ النص المشفر!")
        activity_log.append(f"تم نسخ النص المشفر: {encrypted_text} في {datetime.now()}")

    copy_button = tk.Button(frame, text="نسخ النص المشفر", font=("Arial", 12), bg='black', fg='white', command=copy_text)
    copy_button.grid(row=5, column=0, pady=10, padx=10, columnspan=2)
    add_tooltip(copy_button, "انقر لنسخ النص")


    settings_button = tk.Button(main_screen, text="⚙️ إعدادات", font=("Arial", 12), bg='black', fg='white', command=show_settings_window)
    
    settings_button.place(relx=0.95, rely=0.05, anchor="ne")
    add_tooltip(settings_button, "انقر لفتح الإعدادات")

    main_screen.mainloop()


def show_login_screen():
    login_screen = tk.Tk()
    login_screen.title("تسجيل الدخول")
    login_screen.geometry("600x400")
    login_screen.configure(bg='lightgray')

    frame = tk.Frame(login_screen, bg='lightgray')
    frame.pack(expand=True)

    username_label = tk.Label(frame, text="اسم المستخدم:", font=("Arial", 14), bg='lightgray', fg='black')
    username_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")
    username_entry = tk.Entry(frame, width=40)
    username_entry.grid(row=0, column=1, pady=10, padx=10)

    password_label = tk.Label(frame, text="كلمة المرور:", font=("Arial", 14), bg='lightgray', fg='black')
    password_label.grid(row=1, column=0, pady=10, padx=10, sticky="e")
    password_entry = tk.Entry(frame, width=40, show='*')
    password_entry.grid(row=1, column=1, pady=10, padx=10)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username == "esraa" and password == "1234":
            login_screen.destroy()
            show_main_screen()
        else:
            messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")

    login_button = tk.Button(frame, text="تسجيل الدخول", font=("Arial", 12), bg='black', fg='white', command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=20)
    add_tooltip(login_button, "انقر لتسجيل الدخول")

    login_screen.mainloop()


def show_splash_screen():
    splash_screen = tk.Tk()
    splash_screen.title("المشفر")
    splash_screen.geometry("600x400")
    splash_screen.configure(bg='lightgray')

    label = tk.Label(splash_screen, text="🔒 المشفر", font=("Arial", 32), bg='lightgray', fg='black')
    label.pack(expand=True)

    splash_screen.after(3000, lambda: [splash_screen.destroy(), show_login_screen()])
    splash_screen.mainloop()


show_splash_screen()