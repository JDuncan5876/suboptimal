import io
import time
import os
import string
import sys
import random
import subprocess
import stringdist

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account

def strip_text(text):
    return "".join([i for i in text.replace("\n", "").lower() if i in string.ascii_lowercase or i in string.digits])

def analyze_image(file_name):
    # Load credentials
    credentials = service_account.Credentials. from_service_account_file('/home/pi/suboptimal-dbf800ff4b45.json')

    # Instantiates a client
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    return strip_text(texts[0].description) if len(texts) > 0 else ""

def wait_for_connection():
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname)
    while (response != 0):
        time.sleep(0.05)
        response = os.system("ping -c 1 " + hostname)

def say(text):
    cmd = "say \"{}\"".format(text)
    subprocess.call(cmd, shell=True)


def take_picture():
    n = random.randint(0, 100000)
    path = "/tmp/" + str(n) + ".jpg"
    cmd = "raspistill -o " + path
    print(cmd)
    subprocess.call(cmd, shell=True)
    return path

def match_station(input_text):
    station_map = {'astorpl': 'Astor Pl', 'canalst': 'Canal St', '50thst': '50th St', 'bergenst': 'Bergen St', 'pennsylvaniaave': 'Pennsylvania Ave', '238thst': '238th St', 'cathedralpkwy110thst': 'Cathedral Pkwy (110th St)', 'kingstonthroopaves': 'Kingston - Throop Aves', '65thst': '65th St', '36thst': '36th St', 'delanceystessexst': 'Delancey St - Essex St', 'vansiclenave': 'Van Siclen Ave', 'norwoodave': 'Norwood Ave', '104th102ndsts': '104th-102nd Sts', 'dekalbave': 'DeKalb Ave', 'beach105thst': 'Beach 105th St', 'beach90thst': 'Beach 90th St', 'freemanst': 'Freeman St', 'intervaleave': 'Intervale Ave', '182nd183rdsts': '182nd-183rd Sts', '174th175thsts': '174th-175th Sts', '167thst': '167th St', 'metswilletspoint': 'Mets - Willets Point', 'junctionblvd': 'Junction Blvd', 'flushingmainst': 'Flushing - Main St', 'buhreave': 'Buhre Ave', '3rdave138thst': '3rd Ave - 138th St', 'castlehillave': 'Castle Hill Ave', 'brooklynbridgecityhall': 'Brooklyn Bridge - City Hall', 'zeregaave': 'Zerega Ave', 'grandcentral42ndst': 'Grand Central - 42nd St', '33rdst': '33rd St', '96thst': '96th St', '77thst': '77th St', 'chaunceyst': 'Chauncey St', 'unionst': 'Union St', 'elmhurstave': 'Elmhurst Ave', 'ralphave': 'Ralph Ave', 'pelhampkwy': 'Pelham Pkwy', 'gunhillrd': 'Gun Hill Rd', 'nereidave238st': 'Nereid Ave (238 St)', 'franklinave': 'Franklin Ave', 'simpsonst': 'Simpson St', 'bronxparkeast': 'Bronx Park East', 'winthropst': 'Winthrop St', '149thstgrandconcourse': '149th St - Grand Concourse', '161ststyankeestadium': '161st St - Yankee Stadium', 'lexingtonave59thst': 'Lexington Ave - 59th St', 'e149thst': 'E 149th St', 'morrisonavsoundview': 'Morrison Av - Soundview', 'whitlockave': 'Whitlock Ave', 'stlawrenceave': 'St Lawrence Ave', 'woodside61stst': 'Woodside - 61st St', 'farrockawaymottave': 'Far Rockaway - Mott Ave', '72ndst': '72nd St', '168thst': '168th St', 'kingsbridgerd': 'Kingsbridge Rd', '42ndstbryantpk': '42nd St - Bryant Pk', 'prospectpark': 'Prospect Park', '55thst': '55th St', 'jamaicavanwyck': 'Jamaica - Van Wyck', 'kewgardensuniontpke': 'Kew Gardens - Union Tpke', 'sutphinblvdarcherav': 'Sutphin Blvd - Archer Av', 'courtsq23rdst': 'Court Sq - 23rd St', '67thave': '67th Ave', 'grandavenewtown': 'Grand Ave - Newtown', 'ditmasave': 'Ditmas Ave', 'classonave': 'Classon Ave', 'broadway': 'Broadway', 'lorimerst': 'Lorimer St', 'sutterave': 'Sutter Ave', 'wilsonave': 'Wilson Ave', 'halseyst': 'Halsey St', '8thave': '8th Ave', '36thave': '36th Ave', 'timessq42ndst': 'Times Sq - 42nd St', 'parkpl': 'Park Pl', '111thst': '111th St', 'w4thstwashingtonsqlower': 'W 4th St - Washington Sq (Lower)', '51stst': '51st St', '86thst': '86th St', '233rdst': '233rd St', '66thstlincolnctr': '66th St - Lincoln Ctr', 'huntspointave': 'Hunts Point Ave', 'middletownrd': 'Middletown Rd', '23rdst': '23rd St', 'courtsq': 'Court Sq', '59thstcolumbuscircle': '59th St - Columbus Circle', 'hunterspointave': 'Hunters Point Ave', 'houstonst': 'Houston St', '104thst': '104th St', 'broadchannel': 'Broad Channel', 'oceanpkwy': 'Ocean Pkwy', 'vernonblvdjacksonave': 'Vernon Blvd - Jackson Ave', '68thsthuntercollege': '68th St - Hunter College', 'queensboroplz': 'Queensboro Plz', 'rockawayblvd': 'Rockaway Blvd', 'unionsq14thst': 'Union Sq - 14th St', 'bedfordnostrandaves': 'Bedford - Nostrand Aves', '15thstprospectpark': '15th St - Prospect Park', '7thave': '7th Ave', 'fthamiltonpkwy': 'Ft Hamilton Pkwy', 'churchave': 'Church Ave', 'beverlyrd': 'Beverly Rd', 'newkirkave': 'Newkirk Ave', 'parksideave': 'Parkside Ave', 'grandarmyplaza': 'Grand Army Plaza', 'atlanticavbarclayscenter': "Atlantic Av - Barclay's Center", 'rockawayave': 'Rockaway Ave', 'fultonst': 'Fulton St', 'clintonwashingtonaves': 'Clinton - Washington Aves', 'boroughhall': 'Borough Hall', 'aqueductracetrack': 'Aqueduct Racetrack', 'morrispark': 'Morris Park', 'nostrandave': 'Nostrand Ave', 'nevinsst': 'Nevins St', 'easternpkwybklynmuseum': 'Eastern Pkwy - Bklyn Museum', 'brooklyncollegeflatbushave': 'Brooklyn College - Flatbush Ave', 'sterlingst': 'Sterling St', 'crownhtsuticaave': 'Crown Hts - Utica Ave', 'kingstonave': 'Kingston Ave', 'nassauave': 'Nassau Ave', 'greenpointave': 'Greenpoint Ave', 'marcyave': 'Marcy Ave', 'hewesst': 'Hewes St', '138thstgrandconcourse': '138th St - Grand Concourse', '5thave53rdst': '5th Ave - 53rd St', 'lexingtonave53rdst': 'Lexington Ave - 53rd St', '28thst': '28th St', 'heraldsq34thst': 'Herald Sq - 34th St', '1stave': '1st Ave', 'metropolitanave': 'Metropolitan Ave', 'grandst': 'Grand St', 'grahamave': 'Graham Ave', 'bedfordave': 'Bedford Ave', 'montroseave': 'Montrose Ave', 'longislandcitycourtsq': 'Long Island City - Court Sq', '21stst': '21st St', '39thave': '39th Ave', '145thst': '145th St', '157thst': '157th St', '103rdst': '103rd St', 'centralparknorth110thst': 'Central Park North (110th St)', '81stst': '81st St', '75thave': '75th Ave', '116thstcolumbiauniversity': '116th St - Columbia University', '125thst': '125th St', '135thst': '135th St', '116thst': '116th St', 'tremontave': 'Tremont Ave', '137thstcitycollege': '137th St - City College', '176thst': '176th St', 'burnsideave': 'Burnside Ave', '170thst': '170th St', '181stst': '181st St', '191stst': '191st St', '175thst': '175th St', 'beach44thst': 'Beach 44th St', 'beach60thst': 'Beach 60th St', 'beach98thst': 'Beach 98th St', 'rockawayparkbeach116st': 'Rockaway Park - Beach 116 St', 'beach36thst': 'Beach 36th St', 'beach25thst': 'Beach 25th St', 'parsonsblvd': 'Parsons Blvd', '169thst': '169th St', '103rdstcoronaplaza': '103rd St - Corona Plaza', '63rddrregopark': '63rd Dr - Rego Park', 'grantave': 'Grant Ave', '79thst': '79th St', 'atlanticave': 'Atlantic Ave', 'christopherstsheridansq': 'Christopher St - Sheridan Sq', 'ozoneparkleffertsblvd': 'Ozone Park - Lefferts Blvd', 'w8thstnyaquarium': 'W 8th St - NY Aquarium', 'pelhambaypark': 'Pelham Bay Park', 'westchestersqetremontave': 'Westchester Sq - E Tremont Ave', '18thst': '18th St', 'beach67thst': 'Beach 67th St', 'w4thstwashingtonsqupper': 'W 4th St - Washington Sq (Upper)', '85thstforestpky': '85th St - Forest Pky', 'woodhavenblvd': 'Woodhaven Blvd', '121stst': '121st St', 'myrtlewyckoffaves': 'Myrtle - Wyckoff Aves', 'newlotsave': 'New Lots Ave', 'clevelandst': 'Cleveland St', 'livoniaave': 'Livonia Ave', 'juniusst': 'Junius St', 'canarsierockawaypkwy': 'Canarsie - Rockaway Pkwy', 'e105thst': 'E 105th St', 'saratogaave': 'Saratoga Ave', 'sutteraverutlandroad': 'Sutter Ave - Rutland Road', 'broadwayjunction': 'Broadway Junction', 'alabamaave': 'Alabama Ave', 'shepherdave': 'Shepherd Ave', 'crescentst': 'Crescent St', 'cypresshills': 'Cypress Hills', '75thsteldertln': '75th St - Eldert Ln', '69thst': '69th St', '74thstbroadway': '74th St - Broadway', 'woodhavenblvdqueensmall': 'Woodhaven Blvd - Queens Mall', 'senecaave': 'Seneca Ave', '52ndst': '52nd St', '46thst': '46th St', 'northernblvd': 'Northern Blvd', '82ndstjacksonhts': '82nd St - Jackson Hts', '90thstelmhurstav': '90th St - Elmhurst Av', 'howardbeachjfkairport': 'Howard Beach - JFK Airport', 'aqueductnorthconduitav': 'Aqueduct - North Conduit Av', 'briarwoodvanwyckblvd': 'Briarwood - Van Wyck Blvd', 'foresthills71stav': 'Forest Hills - 71st Av', 'sutphinblvd': 'Sutphin Blvd', 'jamaicactrparsonsarcher': 'Jamaica Ctr - Parsons / Archer', '225thst': '225th St', 'elderave': 'Elder Ave', 'longwoodave': 'Longwood Ave', 'astoriablvd': 'Astoria Blvd', 'astoriaditmarsblvd': 'Astoria - Ditmars Blvd', 'jacksonave': 'Jackson Ave', 'prospectave': 'Prospect Ave', 'cypressave': 'Cypress Ave', '174thst': '174th St', 'allertonave': 'Allerton Ave', 'e143rdststmarysst': "E 143rd St - St Mary's St", 'bedfordparkblvdlehmancollege': 'Bedford Park Blvd - Lehman College', 'harlem148st': 'Harlem - 148 St', 'mtedenave': 'Mt Eden Ave', 'fordhamrd': 'Fordham Rd', 'bedfordparkblvd': 'Bedford Park Blvd', 'marblehill225thst': 'Marble Hill - 225th St', '231stst': '231st St', '215thst': '215th St', '207thst': '207th St', 'inwood207thst': 'Inwood - 207th St', 'vancortlandtpark242ndst': 'Van Cortlandt Park - 242nd St', 'westfarmssqetremontav': 'West Farms Sq - E Tremont Av', '219thst': '219th St', 'mosholupkwy': 'Mosholu Pkwy', 'norwood205thst': 'Norwood - 205th St', 'burkeave': 'Burke Ave', 'baychesterave': 'Baychester Ave', 'eastchesterdyreave': 'Eastchester - Dyre Ave', 'jamaica179thst': 'Jamaica - 179th St', 'wakefield241stst': 'Wakefield - 241st St', 'botanicgarden': 'Botanic Garden', 'bushwickaberdeen': 'Bushwick - Aberdeen', 'e180thst': 'E 180th St', 'dyckmanst': 'Dyckman St', 'franklinavefultonst': 'Franklin Ave - Fulton St', '3rdave149thst': '3rd Ave - 149th St', 'brookave': 'Brook Ave', '40thst': '40th St', '155thst': '155th St', 'uticaave': 'Utica Ave', 'steinwayst': 'Steinway St', 'kosciuszkost': 'Kosciuszko St', 'gatesave': 'Gates Ave', 'centralave': 'Central Ave', 'knickerbockerave': 'Knickerbocker Ave', '30thave': '30th Ave', 'jeffersonst': 'Jefferson St', 'morganave': 'Morgan Ave', 'queensplz': 'Queens Plz', '18thave': '18th Ave', 'bayridgeave': 'Bay Ridge Ave', '25thave': '25th Ave', 'baypky': 'Bay Pky', '20thave': '20th Ave', 'bayridge95thst': 'Bay Ridge - 95th St', '71stst': '71st St', '62ndst': '62nd St', 'newutrechtave': 'New Utrecht Ave', 'aveu': 'Ave U', 'kingshwy': 'Kings Hwy', 'brightonbeach': 'Brighton Beach', 'sheepsheadbay': 'Sheepshead Bay', 'neptuneave': 'Neptune Ave', 'avex': 'Ave X', 'bay50thst': 'Bay 50th St', 'gravesend86thst': 'Gravesend - 86th St', 'avep': 'Ave P', 'aven': 'Ave N', 'avem': 'Ave M', 'avei': 'Ave I', 'avej': 'Ave J', 'aveh': 'Ave H', 'neckrd': 'Neck Rd', '21ststqueensbridge': '21st St - Queensbridge', '47th50thstsrockefellerctr': '47th-50th Sts - Rockefeller Ctr', '57thst': '57th St', 'lexingtonave63rdst': 'Lexington Ave - 63rd St', 'rooseveltislandmainst': 'Roosevelt Island - Main St', '49thst': '49th St', '5thave59thst': '5th Ave - 59th St', '34thstpennstation': '34th St - Penn Station', 'chambersst': 'Chambers St', '42ndstportauthoritybusterm': '42nd St - Port Authority Bus Term', 'myrtlewilloughbyaves': 'Myrtle-Willoughby Aves', 'flushingave': 'Flushing Ave', 'hoytschermerhornsts': 'Hoyt - Schermerhorn Sts', 'jaystmetrotech': 'Jay St - MetroTech', 'eastbroadway': 'East Broadway', 'lowereastside2ndave': 'Lower East Side - 2nd Ave', 'myrtleave': 'Myrtle Ave', '4thav9thst': '4th Av - 9th St', 'smith9thsts': 'Smith - 9th Sts', 'courtst': 'Court St', '3rdave': '3rd Ave', 'libertyave': 'Liberty Ave', '59thst': '59th St', '45thst': '45th St', '9thave': '9th Ave', '53rdst': '53rd St', '25thst': '25th St', 'carrollst': 'Carroll St', 'springst': 'Spring St', '190thst': '190th St', 'princest': 'Prince St', '8thstnyu': '8th St - NYU', 'hoytst': 'Hoyt St', '183rdst': '183rd St', 'worldtradecenter': 'World Trade Center', 'canalsthollandtunnel': 'Canal St - Holland Tunnel', '163rdstamsterdamav': '163rd St - Amsterdam Av', 'cityhall': 'City Hall', 'southferry': 'South Ferry', 'bowlinggreen': 'Bowling Green', 'wallst': 'Wall St', 'whitehallst': 'Whitehall St', 'rectorst': 'Rector St', 'freshpondrd': 'Fresh Pond Rd', 'middlevillagemetropolitanave': 'Middle Village - Metropolitan Ave', 'cortlandtst': 'Cortlandt St', 'broadst': 'Broad St', 'broadwaylafayettest': 'Broadway - Lafayette St', 'bowery': 'Bowery', 'jacksonhtsrooseveltav': 'Jackson Hts - Roosevelt Av', '14thst': '14th St', '6thave': '6th Ave', 'clarkst': 'Clark St', 'forestave': 'Forest Ave', '110thst': '110th St', 'yorkst': 'York St', 'highst': 'High St', 'lafayetteave': 'Lafayette Ave', 'presidentst': 'President St', 'woodlawn': 'Woodlawn', 'bleeckerst': 'Bleecker St', 'euclidave': 'Euclid Ave', '88thst': '88th St', 'cortelyourd': 'Cortelyou Rd', 'parkchester': 'Parkchester', 'franklinst': 'Franklin St', '80thst': '80th St', '5thavebryantpk': '5th Ave - Bryant Pk', 'coneyislandstillwellav': 'Coney Island - Stillwell Av', '34thsthudsonyards': '34th St - Hudson Yards'}
    station_map_list = [(k, v) for k, v in station_map.items()]
    return [i[1] for i in sorted(station_map_list, key=lambda x:stringdist.levenshtein_norm(x[0], input_text))][0]

def main():
    wait_for_connection()
    f = take_picture()
    print("got image")
    text = analyze_image(f)
    print(text)
    best_match = match_station(text)
    print(best_match)
    say(best_match)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--loop':
        while True:
            main()
    else:
        main()
