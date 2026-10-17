# Unraid: Bridge และ Tailscale แยกสอง container

image รุ่นนี้มี Tailscale และเครื่องมือที่ hook ต้องใช้แล้ว จึงไม่ต้องติดตั้งแพ็กเกจตอนเริ่ม container
Unraid จะรัน `tailscale_container_hook` ก่อน แล้วจึงรัน BBSC startup ตาม Entrypoint/CMD เดิม
Tailscale เริ่มด้วย root ส่วน BBSC server ลดสิทธิ์เป็น **99:100**

## โหลด image รุ่นใหม่

นำแพ็กเกจไปไว้บน Unraid แล้วเปิด Terminal จากโฟลเดอร์นั้น:

```sh
tar -xzf BBSC-Server-Linux-x86_64-unraid-tailscale.tar.gz
cd bbsc-server
docker load -i images.tar
```

ใช้ชื่อ image เดิม `localhost/bbsc-shadnet:0.6-pre1` และ `localhost/bbsc-gameserver:0.6-pre1`
หลังโหลดแล้วให้สร้าง container เดิมใหม่จากหน้าตั้งค่า เพื่อใช้ image ที่โหลดใหม่
ปิดการ auto-update จาก registry ของสอง image นี้ เพราะเป็น image ที่โหลดจากไฟล์ในเครื่อง
เก็บ path ของ appdata เดิมไว้ทั้งสองตัว ไม่ต้องลบข้อมูลหรือสร้างบัญชีใหม่

## ตั้งค่าทั้งสอง container

ใน Docker → Edit → Advanced View:

| ช่อง | shadNet | Game server |
| --- | --- | --- |
| Name | `bbsc-shadnet` | `bbsc-gameserver` |
| Repository | `localhost/bbsc-shadnet:0.6-pre1` | `localhost/bbsc-gameserver:0.6-pre1` |
| Network Type | `Bridge` | `Bridge` |
| Use Tailscale | เปิด | เปิด |
| Tailscale hostname | `bbsc-shadnet` | `bbsc-gameserver` |
| Tailscale Userspace Networking | ปิด | ปิด |
| Tailscale State Directory | `/data/.tailscale_state` | `/data/.tailscale_state` |
| Serve / Funnel | ปิด | ปิด |
| Privileged | ปิด | ปิด |
| Extra Parameters | `--init --pull=never` | `--init --pull=never` |
| Host Path (Read/Write) | `/mnt/user/appdata/bbsc/shadnet` | `/mnt/user/appdata/bbsc/gameserver` |
| Container Path | `/data` | `/data` |

Unraid ต้องให้ `/dev/net/tun` และ capability `NET_ADMIN` แก่แต่ละ container สำหรับ kernel networking
หากคำสั่ง Docker ที่ Unraid สร้างยังไม่มี ให้เพิ่ม `--device=/dev/net/tun --cap-add=NET_ADMIN` ใน Extra Parameters
อย่าใส่ `--user 99:100`: hook ต้องเริ่มด้วย root และ BBSC startup จะลดสิทธิ์ให้เอง
อย่า override Entrypoint/CMD หรือเรียก hook ซ้ำใน Post Arguments เพราะ Unraid จัดการให้เมื่อเปิด Use Tailscale
ไม่ต้องเพิ่ม Port Mapping สำหรับการเชื่อมผ่าน Tailscale IP โดยตรง

## ลงทะเบียน Tailscale และตั้ง IP

ตอนเปิดครั้งแรกยังไม่ทราบ IP ให้ใช้ `BBSC_SERVER_IP=127.0.0.1` ชั่วคราวทั้งสองตัว
เปิด Logs แล้วใช้ลิงก์ login ของ Tailscale เพื่อลงทะเบียนแต่ละ container เข้าสู่ Tailnet
hook จะรอให้ Tailscale online ก่อนเปิด BBSC server
หากใช้ ACL/Grants แบบจำกัด ให้เครื่องผู้เล่นทุกเครื่องเข้าถึง IP และพอร์ตที่ระบุด้านล่างได้

ตรวจ IPv4 ของแต่ละตัวจาก Unraid Terminal:

```sh
docker exec bbsc-shadnet /usr/bin/tailscale ip -4
docker exec bbsc-gameserver /usr/bin/tailscale ip -4
```

ตัวอย่าง shadNet ได้ `100.101.102.10` และ game server ได้ `100.101.102.11`
ให้เพิ่ม/แก้ Variable ในหน้าตั้งค่า แล้ว Apply:

| Variable | shadNet | Game server |
| --- | --- | --- |
| `BBSC_SERVER_IP` | `100.101.102.10` | `100.101.102.11` |
| `BBSC_SHADNET_IP` | ไม่ต้องใส่ | `100.101.102.10` |

ถ้าไม่กำหนด `BBSC_SHADNET_IP` จะใช้ `BBSC_SERVER_IP` เป็นค่าเริ่มต้น เพื่อรองรับเครื่องที่ใช้ IP เดียวกัน
ทั้งสอง IP ต้องเป็นของ container นั้นจริงและทุกเครื่องผู้เล่นต้องเข้าถึงได้

## ตรวจและสร้างบัญชี

```sh
docker exec bbsc-shadnet python3 /opt/bbsc-container/server.py health-shadnet
docker exec bbsc-gameserver python3 /opt/bbsc-container/server.py health-gameserver
docker exec -it bbsc-shadnet python3 /opt/bbsc-container/server.py register HunterOne hunter1@example.com
```

คำสั่ง health สำเร็จจะไม่มีข้อความและคืนค่า 0 ใช้บัญชีเดิมได้ถ้าเก็บ appdata เดิมไว้
สร้างบัญชีแยกต่อผู้เล่น ชื่อ 3–16 ตัว ใช้อักษรอังกฤษ ตัวเลข `_` หรือ `-` และอีเมลต่างกัน

## ตั้งค่า launcher

เปิด Play online และ Seamless co-op (BBSC) ทุกเครื่อง:

| ช่อง | ค่า |
| --- | --- |
| Server | `100.101.102.10:31313` |
| WebAPI | `http://100.101.102.10:31315` |
| Community server | `http://100.101.102.11` |
| UPnP | ปิด |

พอร์ตของ shadNet: TCP 31313/31315, UDP 31314 ส่วน game server: TCP 20443, UDP 3478
ผู้เล่นต้องอยู่ใน Tailnet ที่อนุญาตให้ติดต่อกันด้วย เพราะเกมใช้การเชื่อมต่อ P2P

## ข้อมูลและสิทธิ์

startup จะตั้งเจ้าของ `/data` เป็น 99:100 และย้ายไฟล์ของ image รุ่นเก่าที่เป็น UID 10001 ให้เป็น 99:100
ไม่ตาม symlink และไม่เปลี่ยนสิทธิ์ภายใน `.tailscale_state` ซึ่งเป็น state ของ Tailscale ที่ root ดูแล
อย่ารันเครื่องมือเปลี่ยนสิทธิ์แบบ recursive ครอบ `.tailscale_state`
สำรอง appdata ทั้งสองโฟลเดอร์ขณะ container หยุด โดยรักษาสิทธิ์ไฟล์และไม่เปิดเผย state/key ให้ผู้อื่น

อ้างอิงพฤติกรรม hook และ networking: [เอกสาร Tailscale ของ Unraid](https://docs.unraid.net/unraid-os/system-administration/secure-your-server/tailscale/)
การทดสอบในแพ็กเกจนี้ยังไม่ครอบคลุมการ login Tailscale บน Unraid จริงหรือ co-op สองเครื่อง
