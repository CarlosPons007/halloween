import string
from array import array
from tokenize import String

from flask import Flask, render_template, request
import pickle, time, os
from flask_apscheduler import APScheduler

from model.item import Item
from model.player import Player
from model.product import Product

app = Flask(__name__, static_folder="static")

global player_dictionary
player_dictionary = {
    1: {
        "name": "Lilliana de Har Ganeth (Silvia)",
        "desc": 'Una hermosa elfa oscura con ojos amatista penetrantes y cabello negro sedoso que cae hasta su cintura. Lillian es una maestra de la magia de sombras y las pociones alquímicas, conocida por su agudeza y gracia letal. Su actitud tranquila a menudo oculta su oscuro pasado como asesina en el Bastión del Norte, en la frontera con el reino del Caos, donde obtuvo el apodo de "Velo Silencioso".',
        "itemList": [9, 20, 53, 54, 55, 59, 63, 65, 22],
        "goalList": [18, 1, 19],
        "hitPoint": 10,
        "gold": 800,
    },
    2: {
        "name": "Thalric Draleth (Manolo)",
        "desc": 'Un guerrero experimentado de mandíbula marcada y piel oscura, Thalric lleva las cicatrices de muchas batallas. Sus ojos, tan afilados como sus dos espadas, revelan una determinación feroz por conseguir sus objetivos. Conocido como "La Hoja Susurrante", tiene un silencio casi sobrenatural en sus movimientos, habilidad adquirida durante años en las filas ocultas de la Legión Subterránea y en su estancia en el Bastión del Norte.',
        "itemList": [1, 59, 67, 6, 24, 81],
        "goalList": [2, 12, 19],
        "hitPoint": 10,
        "gold": 200,
    },
    3: {
        "name": "Seraphine Noctharis (Daniela)",
        "desc": 'Una misteriosa hechicera elfa oscura con un aura que atrae e inquieta al mismo tiempo. El cabello plateado de Seraphine brilla bajo la luz de la luna, y sus ojos verdes, salpicados de tonos dorados, reflejan una sabiduría más allá de su edad. Experta en magia de ilusiones y reverenciada por su poder para doblar la mente de quienes se le oponen, es conocida como "El Oráculo".',
        "itemList": [59, 63, 69, 8, 26, 81],
        "goalList": [3, 13, 34],
        "hitPoint": 10,
        "gold": 100,
    },
    4: {
        "name": "Kaelen Vasharil (Kaja)",
        "desc": 'Una figura alta y esbelta con un aire de resolución estoica, Kaelen maneja una antigua espada familiar forjada en acero meteórico. Sus ojos cobalto y las runas grabadas en sus brazos lo identifican como un soldado de alto rango. Conocido como "Sombras de Acero", es altamente disciplinado y posee un raro talento en la magia oscura elemental, que usa para ser más letal.',
        "itemList": [13, 7, 28, 81, 82, 82, 59, 67],
        "goalList": [4, 14, 21],
        "hitPoint": 10,
        "gold": 100,
    },
    5: {
        "name": "Elara Duskwraith (Laura)",
        "desc": 'Una ladrona de una belleza inquietante y con una habilidad incomparable en el sigilo y el engaño. Su piel púrpura oscura y su cabello blanco la convierten en una figura impactante en el inframundo. La agudeza mental y agilidad de Elara le han ganado el título de "Filo Espectral", ya que puede infiltrarse en las defensas más vigiladas sin ser detectada. A menudo trabaja como espía, recopilando secretos para la supervivencia de su gente.',
        "itemList": [59, 77, 5, 10, 30, 81],
        "goalList": [5, 15],
        "hitPoint": 10,
        "gold": 100,
    },
    6: {
        "name": "Zareth Neleum (Luis)",
        "desc": 'Un elfo oscuro corpulento y melancólico, de piel gris ceniza y una red de tatuajes que simbolizan su conexión con la magia de fuego y metal. Zareth es un maestro herrero y luchador formidable, creando armas con oscuros encantamientos. Durante su estancia en el Bastión del Norte, fue conocido como la "Mano del Infierno", por su talento incomparable para dominar las llamas a su antojo, creando infernos que pueden arrasar campos de batalla enteros.',
        "itemList": [59, 32, 82, 61, 65],
        "goalList": [6, 16, 21],
        "hitPoint": 10,
        "gold": 50,
    },
    7: {
        "name": "Nimeria Morvine (Ma Angeles)",
        "desc": 'Una hechicera de élite conocida por su control sobre la magia de sangre, Nimeria es una figura de belleza inquietante y oscura atracción. Su cabello negro enmarca su piel pálida y perfecta, mientras sus ojos color rubí parecen ver el alma de cada persona. Temida y respetada, es llamada "El Susurro Carmesí", ya que puede controlar la fuerza vital de sus enemigos con solo un encantamiento.',
        "itemList": [59, 8, 2, 4, 81, 63, 71],
        "goalList": [7, 17],
        "hitPoint": 10,
        "gold": 10,
    },
    8: {
        "name": "Karl Vraneth (Jose)",
        "desc": 'Un elfo oscuro sombrío y enigmático, cuyo dominio de la nigromancia le ha ganado una temible reputación. Con cabello largo salpicado de plata y ojos de ónix penetrantes, Vareth es una figura solitaria, prefiriendo la compañía de antiguos textos y sombras. Conocido como "El Invocador de Almas", tiene el poder de convocar y controlar espectros, lo que lo convierte en una figura que infunde terror entre sus enemigos.',
        "itemList": [59, 3, 73, 79],
        "goalList": [8, 11],
        "hitPoint": 10,
        "gold": 50,
    },
    9: {
        "name": "Celithra Gilganesh",
        "desc": 'Una elfa oscura de inigualable habilidad en la magia de ilusiones, Celithra es capaz de hacerse invisible o cambiar su apariencia al antojo. Sus ojos de un gris brumoso y su cabello negro como la noche le dan un aspecto casi fantasmal, ganándose el nombre de "El Velo de la Noche". Se dice que puede hacer desaparecer ejércitos completos bajo un hechizo de niebla, confundiendo a sus enemigos hasta su derrota.',
        "itemList": [59, 63],
        "goalList": [9, 11, 20],
        "hitPoint": 10,
        "gold": 100,
    },
    10: {
        "name": "Draz'ir Indraugnir",
        "desc": "Un guerrero y cazador de temeraria fuerza física, Draz'ir es reconocido por su aguda intuición y habilidades en rastreo. Su piel oscura casi se funde con las sombras del bosque donde vive. Llamado \"Espina Negra\", Draz'ir es experto en emboscadas y se le conoce por usar espinas encantadas en sus trampas para inmovilizar a sus presas. Prefiere observar antes de atacar, y su astucia es tan temida como sus mortales habilidades.",
        "itemList": [59, 75, 80, 11],
        "goalList": [10],
        "hitPoint": 10,
        "gold": 250,
    },
}
file = open("player_dictionary_file.pkl", "wb")
pickle.dump(player_dictionary, file)
file.close()
global item_dictionary
item_dictionary = {
    1: {
        "name": "Espada de Sombras",
        "desc": "Una antigua espada de obsidiana que puede atravesar la materia como si fuera aire. Se dice que esta espada se nutre de la oscuridad y otorga invisibilidad a su portador cuando se encuentra en sombras profundas. <Un uso. Causa [3D4-3] daños a otro personaje>",
        "outDesc": "Una espada oscura y afilada, emitiendo un aura sombría.",
        "damage": 3,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    2: {
        "name": "Amuleto del Susurro Eterno",
        "desc": "Un amuleto que permite a quien lo lleva escuchar los susurros de los muertos. Es usado por hechiceros para comunicarse con espíritus y obtener información oculta.",
        "outDesc": "Un amuleto con una piedra azul pálida, envuelta en runas antiguas.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    3: {
        "name": "Anillo de Penumbra",
        "desc": "Este anillo otorga la habilidad de fundirse con las sombras. Los usuarios pueden moverse sin ser detectados siempre que no entren en contacto directo con la luz.",
        "outDesc": "Un anillo de plata negra con un misterioso brillo oscuro.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    4: {
        "name": "Vial de Sangre Oscura",
        "desc": "Un pequeño vial que contiene una esencia mágica capaz de fortalecer a quien lo bebe, otorgando resistencia y poder temporal en combate.",
        "outDesc": "Un frasco oscuro que parece brillar con un tenue resplandor rojo.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    5: {
        "name": "Capa de Ocultamiento",
        "desc": "Una capa encantada que permite al usuario volverse invisible bajo la noche. Es particularmente efectiva en la hora del crepúsculo.",
        "outDesc": "Una capa negra con bordes plateados, muy liviana y fluida.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    6: {
        "name": "Talisman de los Espectros",
        "desc": "Este talismán permite al usuario invocar un espectro que puede ser usado como mensajero o espía en la distancia.",
        "outDesc": "Un talismán plateado con una gema negra en su centro.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    7: {
        "name": "Guantelete de Oscuridad",
        "desc": "Un guantelete de metal oscuro que absorbe la energía de los hechizos enemigos, dándole al portador resistencia mágica adicional.",
        "outDesc": "Unos guanteletes negros con grabados arcanos en su superficie.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    8: {
        "name": "Cetro de las Sombras",
        "desc": "Un cetro de poder que permite canalizar magia de sombras, usado por hechiceros oscuros para lanzar conjuros de control mental.",
        "outDesc": "Un cetro alto, terminado en una gema oscura que parece absorber la luz.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    9: {
        "name": "Piedra de Desaparición",
        "desc": "Esta piedra, al activarse, permite al usuario teletransportarse a una distancia corta sin dejar rastro. <Puedes moverte de una localización a otra, aunque este bloqueado el paso.>",
        "outDesc": "Un anillo con una piedra grisácea con un brillo fugaz en su interior.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    10: {
        "name": "Máscara de los Secretos",
        "desc": "Una máscara que oculta la identidad del usuario y le permite comprender cualquier lenguaje mientras la lleva puesta.",
        "outDesc": "Una máscara de metal oscuro con grabados antiguos y complejos.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    11: {
        "name": "Botas VientoNocturno",
        "desc": "Botas encantadas que permiten al usuario moverse con increíble velocidad y sin hacer ruido alguno.",
        "outDesc": "Un par de botas ligeras de cuero negro con bordes oscuros.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    12: {
        "name": "Medallón de Niebla",
        "desc": "Un medallón que permite al usuario convocar una niebla espesa que oscurece el área, confundiendo a los enemigos.<Al usar objetos no puedes ser detectado.>",
        "outDesc": "Un medallón con una gema opaca que parece tener niebla dentro.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    13: {
        "name": "Daga de Penumbra",
        "desc": "Una daga pequeña y liviana, encantada para causar heridas que no se curan fácilmente y que drenan energía.<Un uso. Causa [2D4-2] daños a otro personaje y lo deja ENVENENADO.>",
        "outDesc": "Una daga negra y afilada con un brillo siniestro.",
        "damage": 2,
        "state": "Envenenado",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    14: {
        "name": "Collar de Protección Espectral",
        "desc": "Un collar que genera un campo de protección contra ataques espirituales y espectros hostiles.<Cuando se habrá algún Portal Mágico todos los personajes en la zona quedan CEGADOS excepto tu.>",
        "outDesc": "Un collar de plata con una gema traslúcida en el centro.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    15: {
        "name": "Libro Conjuros Mekhem",
        "desc": "Un libro de hechizos antiguos que contiene conocimientos perdidos y conjuros poderosos de magia oscura.<Mientras tengas este objeto ganas NIGROMANTE.>",
        "outDesc": "Un libro grueso y viejo, con tapas de cuero desgastado.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 74,
    },
    16: {
        "name": "Escudo de la Medianoche",
        "desc": "Un escudo de metal oscuro que absorbe ataques mágicos y redirige su energía contra el enemigo.<Cuando alguien use un ataque contra ti, reduce el daño a la mitad.>",
        "outDesc": "Un escudo grande y opaco con bordes relucientes.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    17: {
        "name": "Medallón de Obsidiana",
        "desc": "Este medallón permite al usuario almacenar energía mágica oscura y usarla en combate para aumentar su poder.<Hay conjuros extremadamente poderosos que requieren tener este objeto.>",
        "outDesc": "Un medallón con una increible gema oscura.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    18: {
        "name": "Lámpara de las Almas Perdidas",
        "desc": "Una lámpara antigua que puede atrapar y retener almas, utilizada para interrogaciones sobrenaturales.<Cuando se habrá algún Portal Mágico habla con el Master.>",
        "outDesc": "Una lámpara pequeña que emite una luz espectral.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    19: {
        "name": "Anillo de Invisibilidad Temporal",
        "desc": "Un anillo que permite al usuario volverse invisible por un breve período. Útil para infiltraciones rápidas.<Al usar objetos no puedes ser detectado.>",
        "outDesc": "Un anillo sencillo, pero con un leve resplandor oscuro.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    20: {
        "name": "Corona Hierro Meteórico",
        "desc": "Esta corona, forjada a partir de hierro meteórico, emite un brillo opaco y grisáceo que refleja su naturaleza extraterrestre. Su estructura está marcada por bordes afilados y ornamentaciones que parecen fragmentos de estrellas. <Eres el Señor de Har Ganeth>.",
        "outDesc": 'La corona de aspecto amenazador del "Señor de Har Ganeth".',
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    21: {
        "name": "Polvo de Sueños Oscuros",
        "desc": "Un polvo que, al ser inhalado por el enemigo, provoca alucinaciones y confusión durante un tiempo prolongado.<Al usarlo contra otro personaje lo deja ATURDIDO.>",
        "outDesc": "Un pequeño frasco de vidrio con polvo oscuro y brillante.",
        "damage": 0,
        "state": "Aturdido",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    22: {
        "name": "Manual para crear: Espada de Sombra y Sigilo",
        "desc": "Manual para crear una espada de sombras que, al ser empuñada, le otorga invisibilidad permanente al portador. <Se necesita Espada de Sombras y Capa de Ocultamiento.>",
        "outDesc": "Un viejo libro",
        "damage": 0,
        "state": "",
        "listPrevItem": [1, 5],
        "evolveItem": 23,
    },
    23: {
        "name": "Espada de Sombra y Sigilo",
        "desc": "Una espada que vuelve completamente invisible a su portador, otorgando al portador la habilidad de moverse sin ser detectado.",
        "outDesc": "Una espada afilada y etérea que desaparece en las sombras.",
        "damage": 3,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    24: {
        "name": "Manual para crear: Cetro del Susurro Oscuro",
        "desc": "Manual para crear un cetro que permite canalizar la magia de sombras y escuchar los ecos de los muertos para obtener secretos oscuros. <Se necesita Cetro de las Sombras y Amuleto del Susurro Eterno.>",
        "outDesc": "Un tomo polvoriento",
        "damage": 0,
        "state": "",
        "listPrevItem": [8, 2],
        "evolveItem": 25,
    },
    25: {
        "name": "Cetro del Susurro Oscuro",
        "desc": "Un cetro antiguo que permite al portador comunicarse con los muertos y controlar la magia de las sombras.",
        "outDesc": "Un cetro adornado con runas ancestrales y una gema que susurra secretos oscuros.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    26: {
        "name": "Manual para crear: Talisman de Teletransporte Sombrío",
        "desc": "Manual para crear un talismán que invoca un espectro para guiar al portador en su teletransportación, dejándolo invisible durante su desplazamiento. <Se necesita Talisman de los Espectros y Piedra de Desaparición.>",
        "outDesc": "Un codice antiguo",
        "damage": 0,
        "state": "",
        "listPrevItem": [6, 9],
        "evolveItem": 27,
    },
    27: {
        "name": "Talisman de Teletransporte Sombrío",
        "desc": "Un talismán que permite teletransportarse rápidamente mientras se invoca un espectro que oculta al usuario durante el proceso.",
        "outDesc": "Un talismán que emite una oscura luz azul, con una figura espectral flotando alrededor.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    28: {
        "name": "Manual para crear: Guantelete Oscuro del Poder Supremo",
        "desc": "Manual para crear un guantelete oscuro que absorbe energía mágica mientras aumenta la resistencia física del portador, usando la esencia mágica del vial. <Se necesita Guantelete de Oscuridad y Vial de Sangre Oscura.>",
        "outDesc": "Un viejo libro",
        "damage": 0,
        "state": "",
        "listPrevItem": [7, 4],
        "evolveItem": 29,
    },
    29: {
        "name": "Guantelete Oscuro del Poder Supremo",
        "desc": "Un guantelete que otorga al portador un poder abrumador, reforzado por la magia oscura de un vial.",
        "outDesc": "Un guantelete de metal negro con líneas rojas brillando en su superficie.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    30: {
        "name": "Manual para crear: Máscara Arcana",
        "desc": "Manual para crear una capa que hace invisible al portador y una máscara que oculta su identidad, permitiéndole comprender cualquier lenguaje mientras permanece oculto. <Se necesita Capa de Ocultamiento y Máscara de los Secretos.>",
        "outDesc": "Un tomo polvoriento",
        "damage": 0,
        "state": "",
        "listPrevItem": [5, 10],
        "evolveItem": 31,
    },
    31: {
        "name": "Máscara Arcana",
        "desc": "Una máscara que no solo oculta al portador, sino que también le otorga la capacidad de entender y hablar todos los idiomas secretos.",
        "outDesc": "Una capa que emite un resplandor tenue, junto con una máscara que brilla sutilmente.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    32: {
        "name": "Manual para crear: Daga del Sueño Eterno",
        "desc": "Manual para crear una daga encantada que no solo drena energía, sino que también envenena a quien la recibe, dejándolo atrapado en una espiral de alucinaciones. <Se necesita Daga de Penumbra y Polvo de Sueños Oscuros.>",
        "outDesc": "Un codice antiguo",
        "damage": 2,
        "state": "Aturdido",
        "listPrevItem": [13, 21],
        "evolveItem": 33,
    },
    33: {
        "name": "Daga del Sueño Eterno",
        "desc": "Una daga encantada que no solo causa daño, sino que deja a su víctima atrapada en un estado de alucinaciones interminables.",
        "outDesc": "Una daga fina, negra como la noche, con partículas de polvo flotando a su alrededor.",
        "damage": 3,
        "state": "Aturdido",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    34: {
        "name": "Manual para crear: Portal mágico",
        "desc": "Manual para crear un portal mágico al reino del caos. <Se necesita Cetro de las Sombras.>",
        "outDesc": "Un codice con runas mágicas",
        "damage": 0,
        "state": "",
        "listPrevItem": [8],
        "evolveItem": 35,
    },
        35: {
        "name": "Portal mágico",
        "desc": "Abre un portal mágico al reino del caos. <Solo se puede usar hablando con el Master en el BOSQUE.>",
        "outDesc": "Un fulgor mágico recorre el cuerpo del portador",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },    
    53: {
        "name": "Botas de cuero",
        "desc": "Botas resistentes hechas de cuero curtido, ideales para largos viajes por caminos difíciles. <No tienen efecto en combate, pero mejoran la velocidad de desplazamiento en terreno complicado.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    54: {
        "name": "Cuerda de cáñamo",
        "desc": "Una cuerda gruesa y resistente, usada para escalar o asegurar cargas pesadas. <Puede utilizarse en combate para inmovilizar a enemigos o en misiones de exploración.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    55: {
        "name": "Manta de viaje",
        "desc": "Una manta gruesa, tejida con lana de oveja, que mantiene el calor en noches frías. <Restaura un poco de energía durante el descanso en exteriores.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
        "evolveItem": 0,
    },
    56: {
        "name": "Saco con grano",
        "desc": "Un saco de lino lleno de grano, básico para el sustento en épocas de escasez. <En combate, puede ser arrojado para obstaculizar al enemigo o cubrir una retirada.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    57: {
        "name": "Odre de vino",
        "desc": "Un odre de vino para transportar líquidos. <Puede ser arrojado para distraer al enemigo o utilizado para apagar fuego en situaciones de emergencia.>",
        "outDesc": "",
        "damage": 1,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    58: {
        "name": "Linterna de aceite",
        "desc": "Una linterna de metal y vidrio que funciona con aceite, útil para iluminar caminos en la oscuridad. <En combate, puede ser lanzada para provocar fuego si hay una llama.>",
        "outDesc": "",
        "damage": 1,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    59: {
        "name": "Alforja de cuero",
        "desc": "Una alforja de cuero utilizada para transportar suministros y herramientas. <Puede ser utilizada en misiones para llevar objetos adicionales.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    60: {
        "name": "Pequeño espejo de bronce",
        "desc": "Un espejo de bronce pulido, utilizado para la higiene personal o para señales de luz. <Puede reflejar luz para distraer en combate o usarse como herramienta de exploración.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    61: {
        "name": "Manual del guerrero",
        "desc": "<Puedes usarlo para generar una ACCIÓN GUERRERO. Se lo puedes dar a otro personaje para que cumpla su misión. Representa tu tiempo ayudando a otro jugador. Solo se puede usar tres veces en toda la partida.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 62,
    },
    62: {
        "name": "ACCIÓN GUERRERO",
        "desc": "<Representa tiempo invertido por un GUERRERO para ayudar a conseguir una misión.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    63: {
        "name": "Manual del hechicero",
        "desc": "<Puedes usarlo para generar una ACCIÓN HECHICERO. Se lo puedes dar a otro personaje para que cumpla su misión. Representa tu tiempo ayudando a otro jugador. Solo se puede usar tres veces en toda la partida.>",
        "outDesc": "Tienes habilidades de HECHICERO.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 64,
    },
    64: {
        "name": "ACCIÓN HECHICERO",
        "desc": "<Representa tiempo invertido por un HECHICERO para ayudar a conseguir una misión.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    65: {
        "name": "Manual del alquimista",
        "desc": "<Puedes usarlo para generar una ACCIÓN ALQUIMISTA. Se lo puedes dar a otro personaje para que cumpla su misión. Representa tu tiempo ayudando a otro jugador. Solo se puede usar tres veces en toda la partida.>",
        "outDesc": "Tiene habilidades de ALQUIMISTA.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 66,
    },
    66: {
        "name": "ACCIÓN ALQUIMISTA",
        "desc": "<Representa tiempo invertido por un ALQUIMISTA para ayudar a conseguir una misión.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    67: {
        "name": "Manual del guerrero",
        "desc": "<Puedes usarlo para generar una ACCIÓN GUERRERO. Se lo puedes dar a otro personaje para que cumpla su misión. Representa tu tiempo ayudando a otro jugador. Solo se puede usar tres veces en toda la partida.>",
        "outDesc": "Tiene habilidades de GUERRERO.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 68,
    },
    68: {
        "name": "ACCIÓN GUERRERO",
        "desc": "<Representa tiempo invertido por un GUERRERO para ayudar a conseguir una misión.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    69: {
        "name": "Manual del adivinador",
        "desc": "<Puedes usarlo para generar una ACCIÓN ADIVINADOR. Se lo puedes dar a otro personaje para que cumpla su misión. Representa tu tiempo ayudando a otro jugador. Solo se puede usar tres veces en toda la partida.>",
        "outDesc": "Tiene habilidades de ADIVINADOR.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 70,
    },
    70: {
        "name": "ACCIÓN ADIVINADOR",
        "desc": "<Representa tiempo invertido por un ADIVINADOR para ayudar a conseguir una misión.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    71: {
        "name": "Manual del taumaturgo",
        "desc": "<Puedes usarlo para generar una ACCIÓN TAUMATURGO. Se lo puedes dar a otro personaje para que cumpla su misión. Representa tu tiempo ayudando a otro jugador. Solo se puede usar tres veces en toda la partida.>",
        "outDesc": "Tiene habilidades de TAUMATURGO.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 72,
    },
    72: {
        "name": "ACCIÓN TAUMATURGO",
        "desc": "<Representa tiempo invertido por un TAUMATURGO para ayudar a conseguir una misión.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    73: {
        "name": "Manual del nigromante",
        "desc": "<Puedes usarlo para generar una ACCIÓN NIGROMANTE. Se lo puedes dar a otro personaje para que cumpla su misión. Representa tu tiempo ayudando a otro jugador. Solo se puede usar tres veces en toda la partida.>",
        "outDesc": "Tiene habilidades de NIGROMANTE.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 74,
    },
    74: {
        "name": "ACCIÓN NIGROMANTE",
        "desc": "<Representa tiempo invertido por un NIGROMANTE para ayudar a conseguir una misión.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    75: {
        "name": "Manual del explorador",
        "desc": "<Puedes usarlo para generar una ACCIÓN EXPLORADOR. Se lo puedes dar a otro personaje para que cumpla su misión. Representa tu tiempo ayudando a otro jugador. Solo se puede usar tres veces en toda la partida.>",
        "outDesc": "Tiene habilidades de EXPLORADOR.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 76,
    },
    76: {
        "name": "ACCIÓN EXPLORADOR",
        "desc": "<Representa tiempo invertido por un EXPLORADOR para ayudar a conseguir una misión.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    77: {
        "name": "Manual del ladrón",
        "desc": "<Puedes usarlo para generar una ACCIÓN LADRÓN. Se lo puedes dar a otro personaje para que cumpla su misión. Representa tu tiempo ayudando a otro jugador. Solo se puede usar tres veces en toda la partida.>",
        "outDesc": "Tiene habilidades de LADRÓN.",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 78,
    },
    78: {
        "name": "ACCIÓN LADRÓN",
        "desc": "<Representa tiempo invertido por un LADRÓN para ayudar a conseguir una misión.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    79: {
        "name": "Ejército personal la Casa de Uber",
        "desc": "Tienes un poderoso ejército acampado fuera de las murallas de la ciudad, esperando tus órdenes. <Puedes decidir, una vez por partida, durante todo un ACTO que bloqueas el paso entre el BOSQUE y la FORTALEZA. Solo se podría acceder por medios mágicos.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    80: {
        "name": "Amuleto Negro",
        "desc": "Este objeto, forjado en las profundidades de los oscuros reinos subterráneos de Naggarond, es un símbolo de la perversidad y la magia negra que caracteriza a la raza elfica.",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    81: {
        "name": "Consejo de la Ciudad",
        "desc": "Eres miembro del consejo de la ciudad de Har Ganeth. Solo sois cinco. Es un cargo muy importante que permite votar en las decisiones de la ciudad.",
        "outDesc": "Lleva un medallón del 'Consejo de la Ciudad'",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    },
    82: {
        "name": "Adorador de Tzeentch",
        "desc": "Eres miembro de una sociedad secreta de adoradores caóticos de Tzeentch, el Dios de la Hechicería y la Transformación. <Puedes dar este objeto, si lo tienes duplicado, a otro elfo que esté de acuerdo, para que se convierta en adorador.>",
        "outDesc": "",
        "damage": 0,
        "state": "",
        "listPrevItem": [],
        "evolveItem": 0,
    }
}

file = open("item_dictionary_file.pkl", "wb")
pickle.dump(item_dictionary, file)
file.close()
global goal_dictionary
goal_dictionary = {
    1: {
        "name": "Recuperar el Corazón de Sombras",
        "desc": "La gema mística fue robada y necesita ser devuelta antes del solsticio de Nimrod. Necesitarás un explorador para buscar su ubicación, pero solo colaborará si un taumaturgo le proporciona ciertos ingredientes prohibidos.",
    },
    2: {
        "name": "La protección del Bosque Muerto",
        "desc": "Frente a la bahía de Devdorer se encuentra el Bosque Muerto, la magia que protege el bosque está debilitándose, y solo un hechicero conoce el conjuro para restaurarla. Sin embargo, para completar el ritual, un guerrero debe protegerlo de los espíritus del oscuro bosque durante la ceremonia.",
    },
    3: {
        "name": "Los verdugos de Hag Ganeth",
        "desc": "Los verdugos de Hag Ganeth está planeando un ataque contra nuestro clan. Para evitarlo, necesitamos un general de gran valía que lidere a nuestro clan y un ejército que disuada a nuestro enemigo. Otra opción es buscar a un ladrón que nos consiga el Amuleto Negro, el objeto más preciado de los verdugos.",
    },
    4: {
        "name": "Operación de Contraespionaje",
        "desc": "Los altos elfos envían espías a nuestras aldeas. Necesitamos un taumaturgo puede realizar un ritual que desenmascare a los infiltrados antes de que actúen.",
    },
    5: {
        "name": "Ladrones de joyas",
        "desc": "La interminable guerra del norte y una serie de robos han dejado a nuestro clan al borde de la quiebra. Un ladrón experto puede identificar al culpable, pero requiere la ayuda de una adivinadora para prever el próximo robo y atrapar al ladrón en el acto.",
    },
    6: {
        "name": "Conseguir hidras de guerra",
        "desc": "Una plaga ha infectado las cuevas de Naggaroth. Un taumaturgo puede realizar un ritual para purificar la zona, pero necesita la protección de varios guerreros para defenderlo de criaturas corrompidas durante el proceso.",
    },
    7: {
        "name": "La Visión de la Adivinadora",
        "desc": "Un ataque se cierne sobre las murallas de Har Ganeth, y solo una adivinadora conoce detalles precisos. Sin embargo, compartirá su visión solo si un nigromante y un taumaturgo colaboran para abrir un Portal Mágico hacia Ragnandu. Si el ataque no se evita, todos los personajes sufrirán daños.",
    },
    8: {
        "name": "El Rito de Ascensión",
        "desc": "Deseas ascender al trono y necesita el respaldo de un hechicero. El hechicero, sin embargo, solo acepta realizar el rito si un guerrero y un nigromante ayudan a estabilizar los efectos mágicos de la ceremonia.",
    },
    9: {
        "name": "Recuperar el Tótem de Hexoatl",
        "desc": "El poderoso tótem ha sido robado por los eslizones. Un nigromante sabe cómo encontrarlo, pero solicita la ayuda de un explorador para infiltrarse en el santuario Hexoatl donde se encuentra escondido, y de un guerrero para proteger la reliquia en el regreso.",
    },
    10: {
        "name": "Eliminar la Maldición de los Cuervos",
        "desc": "Un poderoso conjuro ha sido lanzado desde una torre de hechicería sobre Har Ganeth. Un hechicero poderoso puede disipar el conjuro, pero para ello necesita la ayuda de una adivinadora para ubicar el origen exacto de la maldición.",
    },
    11: {
        "name": "Conseguir oro",
        "desc": "Necesitas conseguir un total de 500 monedas para mantener al ejército mercenario.",
    },
    12: {
        "name": "Conseguir la Espada de Sombra y Sigilo",
        "desc": "Una espada que se vuelve completamente invisible en la oscuridad. Consigue la Espada de Sombra y Sigilo para moverte sin ser detectado.",
    },
    13: {
        "name": "Conseguir el Cetro del Susurro Oscuro",
        "desc": "Un cetro antiguo que permite al portador comunicarse con los muertos y controlar la magia de las sombras. Consigue el Cetro del Susurro Oscuro para desvelar oscuros secretos.",
    },
    14: {
        "name": "Conseguir el Talisman de Teletransporte Sombrío",
        "desc": "Un talismán que permite teletransportarse rápidamente mientras se invoca un espectro para ocultar al usuario. Consigue el Talisman de Teletransporte Sombrío para moverte rápidamente entre los planos.",
    },
    15: {
        "name": "Conseguir el Guantelete Oscuro del Poder Supremo",
        "desc": "Un guantelete que otorga al portador un poder abrumador, reforzado por la magia oscura de un vial. Consigue el Guantelete Oscuro del Poder Supremo para aumentar tu poder físico y mágico.",
    },
    16: {
        "name": "Conseguir la Máscara Arcana",
        "desc": "Una máscara que no solo oculta al portador, sino que le otorga la capacidad de entender y hablar todos los idiomas secretos. Consigue la Máscara Arcana para desbloquear secretos olvidados.",
    },
    17: {
        "name": "Conseguir la Daga del Sueño Eterno",
        "desc": "Una daga encantada que drena energía y deja a la víctima atrapada en alucinaciones interminables. Consigue la Daga del Sueño Eterno para causar estragos en tus enemigos.",
    },
    18: {
        "name": "Dominar Har Ganeth",
        "desc": "Al final del TERCER ACTO debes tener en tu inventario la 'Corona Hierro Meteórico' para demostrar tu poder.",
    },
    19: {
        "name": "Descubrir a los adoradores",
        "desc": "Cuando estuviste en el Bastión del Norte viste el poder de los demonios del caos. Sabes que algunos de tus compañeros [Lilliana de Har Ganeth (Silvia), Zareth Neleum (Luis) y Thalric Draleth (Manolo)] se dejaron seducir por el Caos. Descubre al menos un 'Adorador de Tzeentch'.",
    },
    20: {
        "name": "Abrazar las enseñanzas de Tzeentch, dios del caos ",
        "desc": "Debes convertirte en un 'Adorador de Tzeentch' para acceder a nuevas esferas de poder. Sabes que en el Bastión del Norte cerca de la frontera con el mundo de los demonios, se han creado muchos adoradores.",
    },  
    21: {
        "name": "Abrir un Portal",
        "desc": "Debes encontrar al otro 'Adorador de Tzeentch'. Sabes que en el Bastión del Norte cerca de la frontera con el mundo de los demonios, se han creado muchos adoradores. Debes crear un Portal Mágico en el BOSQUE en el ACTO DOS.",
    },  
}
file = open("goal_dictionary_file.pkl", "wb")
pickle.dump(goal_dictionary, file)
file.close()
global state_dictionary
state_dictionary = {
    1: {
        "name": "Asustado",
        "efect": "(Un uso) Un personaje asustado debe dar uno de sus objetos a quien se lo pida. Puede negarse sufriendo 3 daños.",
    },
    2: {
        "name": "Aturdido",
        "efect": "El personaje aturdido solo puede abstenerse en las votaciones.",
    },
    3: {"name": "Cegado", "efect": ""},
    4: {"name": "Inconsciente", "efect": ""},
    5: {"name": "Envenenado", "efect": ""},
    6: {"name": "Hechizado", "efect": ""},
    7: {"name": "Paralizado", "efect": ""},
}
file = open("state_dictionary_file.pkl", "wb")
pickle.dump(state_dictionary, file)
file.close()
saveObject = (player_dictionary, item_dictionary, goal_dictionary, state_dictionary)
file = open("dictionary_file.pkl", "wb")
pickle.dump(saveObject, file)
file.close()


@app.route("/<player_id>")
def menu(player_id):
    file = open("dictionary_file.pkl", "rb")
    dictionary = pickle.load(file)
    file.close()
    return render_template(
        "/index.html", retrieve_dictionary=dictionary, player_id=player_id
    )


# GET
@app.route("/use_item/<player_id>")
def use_item(player_id):
    file = open("dictionary_file.pkl", "rb")
    dictionary = pickle.load(file)
    file.close()
    return render_template(
        "/use_item.html", retrieve_dictionary=dictionary, player_id=player_id
    )


# POST
@app.route("/use_item/<player_id>", methods=["POST"])
def use_item_post(player_id):
    file = open("dictionary_file.pkl", "rb")
    dictionary = pickle.load(file)
    file.close()

    html_target_id = request.form["target_id"]
    html_item_id = request.form["item_id"]
    item: Item = dictionary[1][int(html_item_id)]
    if int(player_id) == int(html_target_id):
        if int(item["evolveItem"]) == 0:
            return render_template(
                "/use_item_fail.html",
                error_msg="item[evolveItem] es cero",
                player_id=player_id,
            )
        player: Player = dictionary[0][int(player_id)]
        if item["listPrevItem"] != None:
            for item_id in item["listPrevItem"]:
                found = False
                for player_item_id in player["itemList"]:
                    if player_item_id == item_id:
                        found = True
                if not found:
                    return render_template(
                        "/use_item_fail.html",
                        error_msg="no tienes los objetos necesarios",
                        player_id=player_id,
                    )
        itemList: array = player["itemList"]
        itemList.append(item["evolveItem"])
        for item_id in item["listPrevItem"]:
            itemList.remove(item_id)
        player["itemList"] = itemList
        dictionary[0][int(player_id)] = player
        ok_msg = (
            "Se añade "
            + dictionary[1][int(item["evolveItem"])]["name"]
            + " a tu inventario"
        )
    else:
        if (int(item["damage"]) == 0) and (item["state"] == ""):
            return render_template(
                "/use_item_fail.html",
                error_msg="item[damage] es cero y tb item[state] está vacío",
                player_id=player_id,
            )
        if int(item["damage"] != 0):
            target_player: Player = dictionary[0][int(html_target_id)]
            target_player["hitPoint"] = int(target_player["hitPoint"]) - 2 * int(
                item["damage"]
            )
            # TODO: Generate random damage
            dictionary[0][int(html_target_id)] = target_player
            if (target_player["hitPoint"]>0):
                ok_msg = (
                    "El objetivo del ataque tiene ahora "
                    + str(target_player["hitPoint"])
                    + " puntos de vida"
                )
            else:
                ok_msg = (
                    "El objetivo del ataque esta MUERTO"
                )
            player: Player = dictionary[0][int(player_id)]
            itemList: array = player["itemList"]
            itemList.remove(int(html_item_id))
            player["itemList"] = itemList
            dictionary[0][int(player_id)] = player
        if int(item["state"] != ""):
            target_player: Player = dictionary[0][int(html_target_id)]
            target_player["state"] = item["state"]
            dictionary[0][int(html_target_id)] = target_player
            ok_msg = "El objetivo del ataque esta ahora " + target_player["state"]
            player: Player = dictionary[0][int(player_id)]
            itemList: array = player["itemList"]
            itemList.remove(int(html_item_id))
            player["itemList"] = itemList
            dictionary[0][int(player_id)] = player

    file = open("dictionary_file.pkl", "wb")
    pickle.dump(dictionary, file)
    file.close()
    return render_template(
        "/use_item_success.html",
        ok_msg=ok_msg,
        retrieve_dictionary=dictionary,
        player_id=player_id,
        other_player_id=html_target_id,
    )


@app.route("/give_item/<player_id>")
def give_item(player_id):
    file = open("dictionary_file.pkl", "rb")
    dictionary = pickle.load(file)
    file.close()
    return render_template(
        "/give_item.html", retrieve_dictionary=dictionary, player_id=player_id
    )


# POST
@app.route("/give_item/<player_id>", methods=["POST"])
def give_item_post(player_id):
    file = open("dictionary_file.pkl", "rb")
    dictionary = pickle.load(file)
    file.close()

    html_target_id = request.form["target_id"]
    html_item_id = request.form["item_id"]
    player: Player = dictionary[0][int(player_id)]
    itemList0: array = player["itemList"]
    itemList0.remove(int(html_item_id))
    player["itemList"] = itemList0
    dictionary[0][int(player_id)] = player
    target_player: Player = dictionary[0][int(html_target_id)]
    itemList: array = target_player["itemList"]
    itemList.append(int(html_item_id))
    target_player["itemList"] = itemList
    dictionary[0][int(html_target_id)] = target_player

    file = open("dictionary_file.pkl", "wb")
    pickle.dump(dictionary, file)
    file.close()
    return render_template(
        "/give_item_success.html",
        retrieve_dictionary=dictionary,
        player_id=player_id,
        other_player_id=html_target_id,
    )


# GET
@app.route("/get_goal_elements/<player_id>")
def get_goal_elements(player_id):
    file = open("dictionary_file.pkl", "rb")
    dictionary = pickle.load(file)
    file.close()
    return render_template(
        "/get_goal_elements.html", retrieve_dictionary=dictionary, player_id=player_id
    )


# GET
@app.route("/send_gold/<player_id>")
def send_gold(player_id):
    file = open("dictionary_file.pkl", "rb")
    dictionary = pickle.load(file)
    file.close()
    return render_template(
        "/send_gold.html", retrieve_dictionary=dictionary, player_id=player_id
    )


# POST
@app.route("/send_gold/<player_id>", methods=["POST"])
def send_gold_post(player_id):
    file = open("dictionary_file.pkl", "rb")
    dictionary = pickle.load(file)
    file.close()

    html_target_id = request.form["target_id"]
    html_gold = request.form["gold"]
    player: Player = dictionary[0][int(player_id)]
    player["gold"] -= int(html_gold)
    dictionary[0][int(player_id)] = player
    target_player: Player = dictionary[0][int(html_target_id)]
    target_player["gold"] += int(html_gold)
    dictionary[0][int(html_target_id)] = target_player

    file = open("dictionary_file.pkl", "wb")
    pickle.dump(dictionary, file)
    file.close()

    return render_template(
        "/send_gold_success.html",
        retrieve_dictionary=dictionary,
        player_id=player_id,
        other_player_id=html_target_id,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
