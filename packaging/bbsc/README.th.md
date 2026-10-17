# BBSC Server สำหรับ Linux x86_64

แพ็กเกจนี้มี shadNet สำหรับบัญชีและ matchmaking พร้อม game server และ UDP relay
ใช้งานบนเครื่องเล่นเกมเครื่องเดียวกันหรือเครื่อง Linux อีกเครื่องได้ โดยไม่ต้องมีไฟล์เกมบน server

สำหรับ Unraid แบบ Bridge พร้อม Tailscale hook และ IP แยกต่อ container ดู [คู่มือ Unraid](UNRAID.th.md)

## เริ่มด้วย Podman

แตกไฟล์แล้วโหลด image:

```sh
tar -xzf BBSC-Server-Linux-x86_64-unraid-tailscale.tar.gz
cd bbsc-server
podman load -i images.tar
```

เปลี่ยน IP ตัวอย่างเป็น IPv4 ของเครื่อง server ใน LAN หรือ Tailscale
ถ้าทดลองเล่นบนเครื่องเดียวใช้ `127.0.0.1` ได้:

```sh
export BBSC_SERVER_IP=100.101.102.103
podman run -d --init --name bbsc-shadnet --network host --restart unless-stopped \
  -e BBSC_SERVER_IP -v bbsc-shadnet-data:/data:Z localhost/bbsc-shadnet:0.6-pre1
podman run -d --init --name bbsc-gameserver --network host --restart unless-stopped \
  -e BBSC_SERVER_IP -v bbsc-game-data:/data:Z localhost/bbsc-gameserver:0.6-pre1
podman exec bbsc-shadnet python3 /opt/bbsc-container/server.py health-shadnet
podman exec bbsc-gameserver python3 /opt/bbsc-container/server.py health-gameserver
```

คำสั่ง health สำเร็จจะไม่แสดงข้อความและคืนค่า 0 จากนั้นสร้างบัญชีแยกให้ผู้เล่นแต่ละคน
ชื่อใช้ตัวอักษรอังกฤษ ตัวเลข `_` หรือ `-` ความยาว 3–16 ตัว และใช้อีเมลต่างกัน:

```sh
podman exec -it bbsc-shadnet python3 /opt/bbsc-container/server.py register HunterOne hunter1@example.com
```

ระบบจะถามรหัสผ่าน บัญชีจาก public server ไม่ได้ย้ายมาอัตโนมัติ

## ตั้งค่า launcher ทุกเครื่อง

เปิด **Play online** และ **Seamless co-op (BBSC)** แล้วใช้ IP เดียวกับด้านบน:

| ช่อง | ตัวอย่าง |
| --- | --- |
| Server | `100.101.102.103:31313` |
| WebAPI | `http://100.101.102.103:31315` |
| Community server | `http://100.101.102.103` |
| Account | บัญชีใหม่ของผู้เล่นคนนั้น |

ทุกเครื่องต้องติดต่อกันได้ผ่าน LAN หรือ Tailscale ใช้เฉพาะเครือข่ายที่ไว้ใจได้
เพราะโปรโตคอล login ของ shadNet ไม่เข้ารหัสเอง ถ้าใช้ Tailscale ให้ปิด UPnP
ฝั่งโฮสต์ใช้ Hunt Bell ส่วนผู้เข้าร่วมใช้ Kin Bell

หยุด server ด้วย `podman stop bbsc-gameserver bbsc-shadnet`
เปิดอีกครั้งด้วย `podman start bbsc-shadnet bbsc-gameserver`
ข้อมูลบัญชีอยู่ใน named volumes อย่าลบ volume หากต้องการเก็บข้อมูลเดิม
ตัว BBSC server ใช้สิทธิ์ 99:100 ส่วน startup เริ่มด้วย root เพื่อรองรับ Tailscale hook และย้ายสิทธิ์ข้อมูลรุ่นเก่า

การใช้ Docker Compose, พอร์ต firewall, backup และ build จาก source ดู [คู่มือฉบับเต็ม](README.md)
