# foren01 #
  
- **Tipo:** Forense 
- **Autor:** Deloitte
- **Autor del Writeup:** [dtorresss](https://github.com/dtorresss)
- **Flag:** `flag{Th3_4rt_0f_M3m0ry_F0r3ns1c}`

## WriteUp ##

Al descomprimir el zip nos encontramos con el archivo `cyberarena2023.mem`. Para poder analizarlo voy a usar [volatility](https://www.volatilityfoundation.org/releases). 
Para empezar usamos el comando `imageinfo` para saber algo más del archivo. Este comando nos devuelve este output:

```
./volatility_2.5_linux_x64 -f cyberarena2023.mem imageinfo
Volatility Foundation Volatility Framework 2.5
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP0x64, Win7SP1x64, Win2008R2SP0x64, Win2008R2SP1x64
                     AS Layer1 : AMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/dtorres/Desktop/WriteUps_Sucio/CyberArena/forense01/cyberarena2023.mem)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf80002830120L
          Number of Processors : 2
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff80002832000L
                KPCR for CPU 1 : 0xfffff880009eb000L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2023-03-11 08:55:55 UTC+0000
     Image local date and time : 2023-03-11 09:55:55 +0100

```
Podemos ver que nos sugiere varios perfiles. Vamos a probar con `Win7SP0x64`.
Ejecutamos ahora `pslist` indicando "Win7SP0x64" como profile.

```
./volatility_2.5_linux_x64 -f cyberarena2023.mem --profile=Win7SP0x64 pslist
Volatility Foundation Volatility Framework 2.5
Offset(V)          Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
------------------ -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0xfffffa8004805040 System                    4      0     89      547 ------      0 2023-03-11 08:52:03 UTC+0000                                 
0xfffffa8005be6b00 smss.exe                284      4      2       30 ------      0 2023-03-11 08:52:03 UTC+0000                                 
0xfffffa800748e8d0 csrss.exe               364    348     10      475      0      0 2023-03-11 08:52:03 UTC+0000                                 
0xfffffa8006f5f060 wininit.exe             408    348      3       78      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa8006f63540 csrss.exe               428    416     10      304      1      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa80075c1b00 services.exe            476    408     14      217      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa80075b9800 winlogon.exe            504    416      6      120      1      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa80075e2b00 lsass.exe               532    408      9      817      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa8007631b00 lsm.exe                 540    408     11      154      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa800779b550 svchost.exe             652    476     12      367      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa80077d2060 VBoxService.ex          712    476     13      134      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa80077ed470 svchost.exe             788    476      8      286      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa800781ab00 svchost.exe             872    476     24      574      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa800783fb00 svchost.exe             924    476     25      439      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa8007869b00 svchost.exe             960    476     24      540      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa80078899b0 svchost.exe            1008    476     39      983      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa800777e2b0 audiodg.exe             348    872      8      132      0      0 2023-03-11 08:52:04 UTC+0000                                 
0xfffffa80078f5220 svchost.exe            1048    476     19      490      0      0 2023-03-11 08:52:05 UTC+0000                                 
0xfffffa80079b0b00 spoolsv.exe            1204    476     15      285      0      0 2023-03-11 08:52:05 UTC+0000                                 
0xfffffa80079c99b0 svchost.exe            1232    476     19      323      0      0 2023-03-11 08:52:05 UTC+0000                                 
0xfffffa800789bb00 svchost.exe            1320    476     13      220      0      0 2023-03-11 08:52:05 UTC+0000                                 
0xfffffa8007a88470 svchost.exe            1364    476     23      310      0      0 2023-03-11 08:52:05 UTC+0000                                 
0xfffffa8007c034e0 taskhost.exe           1928    476     12      283      1      0 2023-03-11 08:52:10 UTC+0000                                 
0xfffffa8007cabb00 dwm.exe                1996    924      4      102      1      0 2023-03-11 08:52:10 UTC+0000                                 
0xfffffa8007cbbb00 explorer.exe           1028   1984     23      749      1      0 2023-03-11 08:52:10 UTC+0000                                 
0xfffffa8007ce9b00 VBoxTray.exe           1816   1028     14      142      1      0 2023-03-11 08:52:10 UTC+0000                                 
0xfffffa8007c208e0 calc.exe               2164   1028      4       77      1      0 2023-03-11 08:52:16 UTC+0000                                 
0xfffffa800758fb00 SearchIndexer.         2200    476     15      644      0      0 2023-03-11 08:52:17 UTC+0000                                 
0xfffffa8007ed1860 wmpnetwk.exe           2368    476     15      429      0      0 2023-03-11 08:52:17 UTC+0000                                 
0xfffffa8007f958e0 WmiPrvSE.exe           2684    652      7      121      0      0 2023-03-11 08:52:18 UTC+0000                                 
0xfffffa8007fadb00 svchost.exe            2736    476     12      356      0      0 2023-03-11 08:52:18 UTC+0000                                 
0xfffffa8005698b00 SnippingTool.e         2920   1028     10      171      1      0 2023-03-11 08:52:24 UTC+0000                                 
0xfffffa800567da60 wisptis.exe            2968    924      8      139      1      0 2023-03-11 08:52:25 UTC+0000                                 
0xfffffa800803eb00 notepad.exe             864   1028      2       61      1      0 2023-03-11 08:52:37 UTC+0000                                 
0xfffffa8008068060 iexplore.exe           1896   1028     13      577      1      0 2023-03-11 08:52:42 UTC+0000                                 
0xfffffa80056fdb00 iexplore.exe           2424   1896     21      644      1      1 2023-03-11 08:52:42 UTC+0000                                 
0xfffffa80081b3b00 iexplore.exe            680   1896     31      774      1      1 2023-03-11 08:52:48 UTC+0000                                 
0xfffffa8007e18700 sppsvc.exe             3764    476      6      160      0      0 2023-03-11 08:54:57 UTC+0000                                 
0xfffffa800793a060 svchost.exe            3800    476     15      356      0      0 2023-03-11 08:54:57 UTC+0000                                 
0xfffffa80047e0060 FTK Imager.exe         2380   1028     20      367      1      0 2023-03-11 08:55:14 UTC+0000  
```
Esto es lo que nos devuelve. En el enunciado del reto, decia algo relacionado con apuntar cosas por lo que vamos a intentar dumpear la memoria del porceso 864 el cual corresponde a `notepad.exe`. Para ello usamos el comando `volatility_2.5_linux_x64 -f cyberarena2023.mem --profile=Win7SP0x64 memdump -p 864 --dump-dir=./`
Esto nos creará un archivo 864.dmp. Tras mucho buscar la flag nos damos cuenta que esta encodeada por lo que podemos usar el comando `strings -e l 864.dmp | grep "flag" | head ` y veremos que entre el texto se encuentra la flag.
