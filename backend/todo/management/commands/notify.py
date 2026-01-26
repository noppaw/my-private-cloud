import os  # ✅ 1. import os มาใช้งาน
from django.core.management.base import BaseCommand
from django.utils import timezone
from todo.models import Task
import requests
from datetime import timedelta

class Command(BaseCommand):
    help = 'Checks for upcoming tasks and sends Telegram notifications'

    def handle(self, *args, **options):
        # ✅ 2. ดึงค่าจาก ENV
        token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')

        if not token or not chat_id:
            self.stdout.write(self.style.ERROR("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing in .env"))
            return

        # ----------------------------------------------------
        # ส่วน Logic ด้านล่างเหมือนเดิมครับ แค่เปลี่ยนตัวแปร token/chat_id
        # ----------------------------------------------------
        
        now = timezone.now()
        upcoming_window = now + timedelta(minutes=10) 
        
        tasks = Task.objects.filter(
            start_time__isnull=False,
            is_completed=False,
            notify_telegram=True,
            is_notification_sent=False,
            start_time__lte=upcoming_window,
            start_time__gt=now - timedelta(hours=1)
        )

        if not tasks.exists():
            self.stdout.write("No tasks to notify.")
            return

        for task in tasks:
            message = f"🔔 <b>เตือนงานใกล้ถึงเวลา!</b>\n\n📝 <b>งาน:</b> {task.title}\n⏰ <b>เวลา:</b> {task.start_time.strftime('%H:%M')} น."
            
            if task.description:
                message += f"\n📌 <b>รายละเอียด:</b> {task.description}"

            # ✅ 3. ใช้ตัวแปร token ใน URL
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {
                "chat_id": chat_id, # ✅ 4. ใช้ตัวแปร chat_id
                "text": message,
                "parse_mode": "HTML"
            }
            
            try:
                response = requests.post(url, data=data)
                
                if response.status_code == 200:
                    task.is_notification_sent = True
                    task.save()
                    self.stdout.write(self.style.SUCCESS(f"Sent notification for: {task.title}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Failed to send: {task.title} - {response.text}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error: {e}"))