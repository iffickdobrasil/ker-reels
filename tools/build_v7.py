import sys,json; sys.path.insert(0,'/home/claude/work')
from themes4 import T
import reel4
R="/home/claude/ker-reels"; M="/home/claude/work/music"
VOL={"bzh_rock":0.42,"bzh_electro":0.5,"bzh_bagad":0.75}
OVR={"perdrix":"bzh_rock","kervilzic":"bzh_mer","gourmandises":"bzh_sax","balades":"bzh_festnoz","pontlabbe":"bzh_bagad"}
jobs=[]
for s,t,m,it in T:
    m=OVR.get(s,m); jobs.append((s,t,m,it))
mp={x[0]:x[2] for x in json.load(open('/home/claude/work/mapping.json'))}
v3=[("Une journée à Kermenhir",[1,20,45,95],{1:"Réveils au calme",20:"Grandes tablées",45:"Au coin du feu",95:"Couchers de soleil"},"bzh_festnoz","journee"),
 ("Soirées au coin du feu",[78,72,81,94],{78:"Cheminée de granit",72:"Soirées entre amis",81:"Cocooning breton",94:"Nuits étoilées"},"bzh_festnoz","soirees"),
 ("Le charme des vieilles pierres",[24,38,13,14],{24:"Poutres et mezzanine",38:"Salon de caractère",13:"Granit centenaire",14:"Pignons bretons"},"bzh_soft","charme"),
 ("Chambres & nuits paisibles",[39,29,41,48],{39:"Nuits douces",29:"Chambre claire",41:"Charme ancien",48:"Sous les combles"},"bzh_soft","chambres"),
 ("Jardin & lumières de Bretagne",[33,86,89,5],{33:"Hortensias de Bretagne",86:"Jardin fleuri",89:"Grange et hortensias",5:"Lumières du soir"},"bzh_nature","jardin"),
 ("Le domaine au fil des saisons",[98,17,15,87],{98:"Le menhir",17:"Chemins creux",15:"Murets de pierre",87:"Ciels bretons"},"bzh_nature","domaine")]
for t,ph,caps,m,s in v3:
    jobs.append((s,t,m,[dict(k=mp[n],cap=caps[n]) for n in ph]))
only=sys.argv[1:]
for s,t,m,it in jobs:
    if only and s not in only: continue
    print("==",s,flush=True)
    reel4.build(t,it,f"{M}/{m}.mp3",f"{R}/ker-reel-{s}-v7.mp4",vol=VOL.get(m,0.6))
print("ALL DONE",flush=True)
