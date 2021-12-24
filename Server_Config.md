# 服务器配置

## Access

- Windows Remote Desktop
  - Computer: `server.waferlab.tk` or `172.18.217.168`
  - Default port
- OpenSSH
  - to-do
- Windows Admin Center
  - https://server.waferlab.tk or https://172.18.217.168
- SMB
  - D: was mapped to `\\server.waferlab.tk\Data`

## Hardware

### CPU

2 sockets

- Intel(R) Xeon(R) Gold 6248R CPU @ 3.00GHz, 2993 Mhz, 24 Core(s), 48 Logical Processor(s)
- Intel(R) Xeon(R) Gold 6248R CPU @ 3.00GHz, 2993 Mhz, 24 Core(s), 48 Logical Processor(s)

Reference Cinebench R23 score:

- Multi Core: 46351
- Single Core: 1032

### GPU

1 PCI-E slot

- NVIDIA GeForce RTX 3090

Driver:

- NVIDIA Studio Driver: Version 472.84

### Storage

- System (C:)
  - Samsung SSD 970 EVO Plus 2TB
- Data (D:)
  - Seagate ST4000DM004 4TB

### Ethernet

2 adapters

- Intel(R) I210-LM Gigabit Network
- Intel(R) I210-LM Gigabit Network

Driver version: 12.18.9.1

### Optical Drive

## Software

### To-dos

- [ ] Gig
- [ ] OneDrive
- [x] Windows Terminal
- [x] PowerShell 7
- [x] Anaconda
- [x] HFSS: AEDT v2021 R2, v2020 R2, ANSYS HFSS 15
- [x] CST: DS SIMULIA CST STUDIO SUITE 2019
- [ ] Magus: DS SIMULIA Antenna Magus
- [x] OpenSSH server
- [ ] WSL2
- [x] Configure SMB
- [ ] Configure auto backup
- [x] Internet Download Manager
- [x] `winget`

### Operating System

Microsoft Windows Server 2022 Datacenter

|Item|Value|
|:--|:--|
|Version|10.0.20348 Build 20348|
|System Name|EM-SERVER-4RSKT|
|System Model|Precision 7920 Tower|
|BIOS Version/Date|Dell Inc. 2.16.1, 2021/11/13|
|Secure Boot State|Off|
|Installed Physical Memory (RAM)|1.00 TB|

### HFSS

- AEDT 2021 R2
- AEDT 2020 R2 (not cracked yet)
- HFSS 15 (not cracked yet)

### CST

CST Studio Suite 2019

No SP update installed

### Utilities

- Windows Store (patched)
- WinRAR
- Windows Security
- Server Manager
- Dell Support Assist

### Browser

- Google Chrome
- Microsoft Edge

### Python

Anaconda3

Path: `C:\ProgramData\Miniconda3`