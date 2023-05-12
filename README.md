# WRO_Future_Engineers_Xenoplex1

## Motivation und Hintergrund:
Jetzt im 21. Jahrhundert, in der Zeit von Digitalisierung und 
Automatisierung sämtlicher Prozesse, rückt auch die Technik rund 
um autonomes Fahren immer mehr in den Vordergrund der 
Wissenschaft. Deshalb wollten wir dieses Sachgebiet nun auch 
bei der World Robotic Olympiad thematisieren. Auch dieses 
vereinfachte Abbild der Realität hat uns gezeigt wie komplex solche für 
uns scheinbar einfachen Vorgänge in Wirklichkeit sind. Aber genau 
diese Schwierigkeit war für uns letztendlich der Anreiz 
diese Herausforderung zu bewältigen.

## Der Aufbau des Fahrzeugs: 
Als Basis des Fahrzeugs dient das Chassis eines autonom fahrenden 
Fahrzeugs von Fischertechnik. Der Mikrocontroller Arduino UNO 
fungiert dabei als "Gehirn" des Fahrzeugs und steuert alle 
Abläufe. Als Antrieb für dieses Roboterfahrzeug benutzen wir einen
schwarzen Encodermotor von Fischertechnik welcher über eine
H-Brücke l298n angesteuert wird. Diese versorgt mit Hilfe des 
integrierten Spannungswandlers den Controller und alle 
Sensoren mit der Betriebsspannung von 5 Volt. Zur Lenkung 
verwenden wir einen handelsüblichen Servomotor. Links und rechts besitzt das Fahrzeug je einen Ultraschallsensor HC-SR04. 
Die Bilderkennung und -auswertung übernimmt eine Kamera Pixy V2.1 von CMU und Charmed Labs. Außerdem ist ein NiMH Akku von Fischertechnik mit 8,4 Volt und 1800mAh verbaut. Um die bereits gefahrenen Runden zu zählen benutzen wir einen Kompasssensor.

## Programme:
Für jede der beiden gestellten Aufgabe haben wir speziell für diese Aufgabe angepasstes Programm entwickelt.
#### Aufgabe 1:
Für Aufgabe 1 werden zu Beginn vorgefertigte Bibliotheken für Kompass und Servo 
hinzugefügt, über die die Sensoren des Fahrzeugs angesteuert 
werden können. Außerdem werden Variablen erstellt, z.B. für
die Entfernungsmessung mit einem Ultraschallsensor oder für das 
Auslesen der Werte des Kompasssensors.
Im Hauptteil dieses Programms werden zunächst die beiden Starttaster für links und rechts abgefragt, 
damit das Fahrzeug auf Kommando gestartet werden kann. Beim Drücken der Starttasten links oder rechts 
wird festgelegt ob der Roboter 
entsprechend im oder gegen den Uhrzeigersinn fährt. Nach der 
Eingabe durch einen der Taster wird der Motor für das Fahren 
nach vorne gestartet und die Vorderräder mit Hilfe des Servos 
geradeaus gerichtet. Im Programm wird jetzt durchgehend der 
Ultraschall abgefragt, der für die entsprechende Richtung vorgesehen 
ist. Dieser ist für die Erkennung des Abstands zur inneren
Wand vorgesehen. Fährt der Roboter näher als 20 Zentimeter an die 
innere Wand, lenkt der Servo nach außen, um den Roboter in einem
möglichst konstanten Abstand zur inneren Wand zu halten. Ist 
der Abstand größer als 20 Zentimeter, so lenkt der Roboter auf 
die Wand zu, um den Abstand zu verringern. Wenn der Abstand 
aufgrund einer Ecke nun größer als 1,5 Meter gemessen wird, so 
fährt der Roboter eine Kurve, bis er schließlich wieder eine 
Wand registriert. Mithilfe des Kompasses und den Ecken wird 
der Rundenzähler erhöht. Nach drei vollständig gefahrenen Runden 
beziehungsweise nach zwölf Kurven stoppt das Fahrzeug, idealerweise für 
die volle Punktzahl in dieser Disziplin.
#### Aufgabe 2:
Zu Beginn ist dieses Programm ähnlich aufgebaut wie für die erste 
Aufgabe. Es werden die benötigten Bibliotheken für die Sensoren 
implementiert und alle Variablen deklariert.
Im Hauptteil des Programmes für Aufgabe 2 werden erneut die Taster für die 
Auswahl der Richtung abgefragt. Im Gegensatz zum Programm für 
Aufgabe 1 orientiert sich der Roboter nun an beiden Wänden, um 
möglichst mittig zu fahren. Somit werden die farbigen 
Hindernisse vor dem Roboter in jedem Fall erkannt und der 
Roboter erhält genug Platz um diese korrekt zu umfahren. Für die 
Erkennung der Objekte mit entsprechender Zuordnung der 
Farben sorgt nun die Pixy Kamera. Dafür wurden die Hindernisse 
der Pixy angelernt, sodass sie nun zwischen grün und rot 
unterscheiden kann. Erkennt die Pixy ein rotes Hindernis auf der 
Fahrbahn, so lenkt der Roboter mit dem Servo rechts um das 
Hindernis herum. Ein grünes Hindernis umfährt das Fahrzeug links. 
Ist das eben umfahrene Hindernis aus dem Blickfeld der
Kamera verschwunden, markiert der Roboter es als umfahren 
und positioniert sich wieder mittig auf der Fahrbahn. Wie auch
schon im Programm für die erste Aufgabe implementiert,
erkennt das Fahrzeug alle Ecken mit den Ultraschallsensoren auf 
der entsprechenden Seite. Aufgrund von Problemen mit 
Hindernissen in den Ecken entschieden wir uns dazu, die
Ultraschallsensoren durch ein Unterprogramm auszulesen und
die Ergebnisse auszuwerten. So können Werte mit nur 
kurzzeitig erkannten Hindernissen aussortiert werden, sodass die 
Ecken nun besser wahrgenommen werden. Wie auch schon im 
ersten Programm fährt der Roboter bei einem Abstand von mehr als 
1,5 Meter auf der entsprechenden Seite eine Kurve, mit dem 
Unterschied, dass dies erst nach einer kurzen Verzögerung 
stattfindet, damit das Fahrzeug auch in der Kurve möglichst 
mittig fährt. Auch in diesem Programm werden die Kurven mit Ultraschall
und Kompasssensor gezählt und der Roboter bleibt im Idealfall 
nach drei ganzen Runden im Startfeld stehen.