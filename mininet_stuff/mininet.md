# Fájlok megosztása

Fájlokat kétféleképpen tudunk átadni könnyen a virtuális gépünk, az első, ha működik a gépen belül az internet akkor le is tudjuk tölteni a benne lévő böngészővel, vagy létrehozni egy megosztott mappát a gazda gépen és arról megosztani:

UbuntuVM: Devices -> Shared Folder -> Shared Folder Settings
Jobb felül, zöld Add gomb felhoz egy kis ablakot, ahol meg lehet adni, az új mappa adatait. 
Path: ahol van a mappa, pl: ...\telekom\mininet\megosztott
Name: mappa neve, pl: megosztott
Mount point: a Vm-ben a neve, pl: \mnt
Kattintsuk be a Auto-mount és Make permanent gombokat.

(Opcionális)
Ha ezután se működik, akkor adjuk ki a következő parancsot:
Rakjátok át a hálózati kártyát bridge módba.
Adjátok ki a következő parancsot:
sudo apt-get install virtualbox-guest-utils
Újraindítás és:
sudo mount -t vboxsf megosztottmappanev /mnt/

# Képerenyő méret növelése

Ha a virtuális Ubuntu képernyője nem tölti ki a teljes VirtualBox ablakot, azaz nagyon kicsi a felbontás, hajtsuk végre a következőket.

VM: Devices -> Import Guest additions CD image -> jelszó, meg kell várni míg települ és végén enter
Shutdown Ubuntu VM
Oracle: VMSettings -> Display -> Enable 3D acceleration
Oracle: File -> Preferences -> Maximum Guest Screen Size: Hint -> 1920x1080 -> OK
Start Ubuntu VM
VM: (legyen kitéve maximum méretbe az ablak) View -> Auto-resize Guest Display

# Mininet telepítése

Töltsetek le a 2GB-os zippet, és csomagoljátok ki (nagy fájl 6-8GB):

https://ikelte-my.sharepoint.com/:u:/g/personal/afbdpk_inf_elte_hu/EfAwBnSEDudLuU6cR-sb4WMBu1atz4ll3Ivsmg1gQDtb8Q?download=1

Ha ez megvan, akkor "8.gyakorlat.pdf" 4 oldalán lévö beállításokat tegyétek meg. 
Ha ez megvan és működik a Ubuntu VM a "8.gyakorlat.pdf" diáit nézzétek át (MobaXterm-re nem lesz szükség).