# ⚡ QUICK START - 5 MINUTES

## For the impatient developer 🚀

### 1️⃣ Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### 2️⃣ Setup Database (1 min)
```bash
python manage.py migrate
```

### 3️⃣ Create Admin Account (1 min)
```bash
python manage.py createsuperuser
```
When prompted, enter:
- **Username:** `admin` (or your choice)
- **Email:** `admin@example.com`
- **Password:** (create a strong one)

### 4️⃣ Run Server (1 min)
```bash
python manage.py runserver
```

### 5️⃣ Open in Browser (1 min)
Visit: **http://127.0.0.1:8000**

---

## 🎯 That's it! You're ready to go!

### First Things to Try:
- ✅ Login with your admin credentials
- ✅ Click "Quick Add" to add an application
- ✅ Go to Dashboard to see statistics
- ✅ Check Analytics for charts
- ✅ Export to CSV/Excel

---

## 📱 Important URLs
| Page | URL |
|------|-----|
| Dashboard | http://127.0.0.1:8000/ |
| All Applications | http://127.0.0.1:8000/applications/ |
| Analytics | http://127.0.0.1:8000/analytics/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |
| Register | http://127.0.0.1:8000/accounts/register/ |

---

## 🆘 Common Issues?

**Port already in use?**
```bash
python manage.py runserver 8001
```

**Database error?**
```bash
python manage.py migrate
```

**Static files not showing?**
```bash
python manage.py collectstatic --noinput
```

---

## 📚 Need More Help?
- See **README.md** for complete documentation
- See **SETUP.txt** for detailed commands
- Check Django logs for errors

---

## ✨ Features You Have

✅ Dashboard with statistics & charts  
✅ Add applications (quick or detailed)  
✅ Advanced filtering & search  
✅ Status tracking with updates  
✅ Follow-up reminders  
✅ Resume version tracking  
✅ Export to CSV & Excel  
✅ Analytics & trends  
✅ User authentication  
✅ Admin panel  

---

**Ready? Let's go!** 🚀

```bash
python manage.py runserver
```

Then open: http://127.0.0.1:8000
