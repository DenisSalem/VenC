#! /usr/bin/env python3

#   Copyright 2016, 2021 Denis Salem
#
#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import os
import random
import shutil
import subprocess
import sys

BENCHMARCH_VERSION = "2.0.2"

CONTEXT = {
    "SAMPLE_CATEGORIES" : ["Movie","Computing","Music","Art","Sport","Literature","Diary","Photography","Science"],
    "CATEGORY_INDEX" : random.randint(0, 8),
    "CONTENT_SIZE_MULTIPLIER" : random.randint(0,10),
    "ENTRY_ID_COUNTER" : 0,
    "DATETIME" : datetime.datetime(2000, 1, 1, 0, 0).timestamp(),
}

ENVIRONMENT = {}

LOREM_IPSUM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sodales, dui ultrices interdum tincidunt, nibh tortor varius arcu, vitae fermentum velit nisl vel elit. Donec at lorem semper, pellentesque velit in, sodales metus. Fusce tempus arcu sit amet dui luctus, id rhoncus augue iaculis. Maecenas laoreet odio sit amet mauris porttitor feugiat. Aliquam nec elit congue, eleifend purus vitae, hendrerit felis. Proin vitae condimentum quam. Praesent suscipit nisl est, ac semper mauris eleifend et. Duis neque lorem, pharetra ut facilisis ac, rutrum et mauris. Pellentesque facilisis ex in metus semper vulputate. Vivamus ultrices justo et eros molestie, quis hendrerit tellus sollicitudin. Aenean id nisl a lacus finibus ullamcorper.
Cras auctor, dolor ut elementum vulputate, lectus arcu luctus turpis, quis laoreet augue dolor ac ex. Suspendisse molestie vestibulum erat, ut congue neque elementum et. Fusce nisl nulla, blandit ac sapien sed, vehicula vestibulum neque. Ut sit amet elementum urna. Vivamus bibendum commodo sem vel tempor. Donec nec magna sed diam ullamcorper pretium a ut felis. Phasellus elementum aliquet tempor. Proin quis orci non est mollis blandit sit amet vitae neque.
Aenean urna lacus, interdum ultricies arcu quis, laoreet venenatis orci. Integer mollis massa nec ipsum dignissim, eget vehicula nibh tristique. Cras sagittis sem in ornare tristique. Donec rhoncus massa et sem laoreet viverra. Aenean ultrices, tellus id placerat ultrices, arcu arcu venenatis justo, nec fringilla libero velit sit amet nulla. Mauris convallis sed purus ac consectetur. Fusce accumsan, arcu eget dignissim gravida, justo justo blandit felis, at ultrices ligula quam ac mi. Nulla facilisi. Curabitur erat tortor, molestie vitae sem ut, finibus iaculis risus. Aenean consequat laoreet leo, id auctor neque elementum sed. Etiam ante est, bibendum id dictum non, convallis sit amet ante. Aliquam tortor sem, venenatis vel euismod sed, egestas sit amet nulla. Maecenas magna ipsum, pretium sit amet urna id, tincidunt molestie sapien. Maecenas laoreet lobortis vehicula.
Donec eget sodales est. Aliquam porta nisi eget justo dictum, eu ultrices elit ullamcorper. Vivamus molestie condimentum sapien, non sollicitudin ex mollis sed. Proin consectetur elit quis turpis placerat, a mollis tellus laoreet. Etiam tristique sit amet ligula ac pulvinar. Donec arcu ante, ultrices id nisi vitae, hendrerit volutpat ante. Aliquam congue, nunc eu porttitor iaculis, lectus augue porta sapien, eu sagittis eros dolor sed erat. Ut nisi odio, facilisis vitae rutrum nec, molestie facilisis libero. Nullam at ullamcorper ante. Cras semper ex non quam blandit aliquet. Sed vestibulum purus finibus elit vulputate faucibus. Vivamus interdum velit eu nisl pulvinar fermentum sit amet et eros. Etiam sodales lacus nulla, et tincidunt leo faucibus quis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut sit amet ornare libero, eget luctus est. Mauris ornare et eros vel elementum.
In hac habitasse platea dictumst. Phasellus sapien enim, vehicula eu magna vel, rutrum convallis tortor. Integer fringilla libero et tortor ornare congue. Aliquam egestas dolor quis rutrum volutpat. Mauris metus tortor, eleifend sed velit non, consectetur iaculis nisi. Proin efficitur faucibus orci et commodo. Vestibulum eget felis dapibus, congue augue nec, auctor dolor. Sed nec dictum arcu, ut efficitur dolor. Donec venenatis lacus vel nulla pretium varius.
Morbi pellentesque convallis velit, ac semper massa eleifend eget. Proin condimentum pulvinar elit, faucibus euismod dolor bibendum non. Mauris scelerisque tristique est in volutpat. Pellentesque sit amet libero massa. Proin quam lectus, euismod eu interdum sagittis, vehicula id tellus. Duis et diam risus. Sed at lorem feugiat, molestie velit quis, molestie lorem. Nam sodales semper nulla in varius. Vivamus blandit condimentum nisi sed consectetur. Vestibulum lacinia, ligula eu bibendum ultrices, est nunc tempus quam, et facilisis dolor neque ac arcu. Suspendisse interdum hendrerit eros vel auctor. Aliquam sed elit sed dui mattis porttitor. Praesent a risus vitae odio pellentesque aliquam in sit amet urna.
Praesent tincidunt sapien eget enim vulputate, eu vehicula neque imperdiet. Donec aliquet tristique neque, eu dapibus lorem semper eget. Curabitur ullamcorper sem non justo placerat fermentum. Morbi dolor sem, commodo non velit ut, pretium tempor quam. Aenean sit amet odio velit. Praesent eget ante placerat, sodales purus non, dapibus lacus. Pellentesque eu quam ac nisl vestibulum pulvinar nec id tortor. Morbi ac vehicula metus, interdum viverra leo. Duis a tellus dapibus, lacinia justo eget, suscipit nunc. Pellentesque ultrices augue nec turpis luctus, vel eleifend elit varius. Fusce velit urna, semper in neque in, interdum sodales erat. In viverra nisi eu rhoncus sagittis. Sed accumsan, mi vitae placerat feugiat, velit ante ultrices massa, vitae scelerisque ipsum dui eu quam.
Sed vitae felis eleifend, imperdiet magna vitae, malesuada tellus. Cras egestas enim gravida, condimentum magna aliquet, bibendum urna. Maecenas fringilla odio sit amet ornare fermentum. Proin malesuada ex a est eleifend maximus. Fusce commodo leo in dui viverra congue. Vivamus vitae elit velit. Nulla tellus enim, elementum blandit tortor nec, tempor facilisis tellus. Praesent venenatis ex sem, sed luctus ante congue consectetur. Vestibulum eu leo sodales, elementum arcu a, mattis ante. Sed ultricies, lectus id fermentum lacinia, quam metus maximus quam, eget semper orci mi in augue. Nulla rhoncus metus dolor, vitae sodales erat dapibus sed. Aenean pharetra aliquam pretium. In semper varius enim eu hendrerit. Fusce ullamcorper arcu ac sagittis malesuada. Etiam tincidunt tortor tincidunt ex aliquam condimentum in at lacus. Suspendisse potenti.
Vivamus rutrum erat ut velit laoreet finibus. Integer semper consequat interdum. Suspendisse quis lorem nibh. Aliquam interdum lorem orci, at hendrerit mauris fringilla non. Suspendisse potenti. Mauris vitae nunc convallis, eleifend ante sit amet, auctor mauris. Etiam eget venenatis lectus. Donec sed lacus mattis massa sagittis placerat lacinia eget mi. Nullam neque orci, sodales sit amet nibh in, mollis suscipit nisi. Etiam fringilla malesuada metus, ut sollicitudin elit sodales nec. Aliquam fringilla sed velit vitae gravida. Duis ornare elementum metus sed porttitor. Cras tempor accumsan urna, ut placerat odio accumsan eu. Donec pharetra et ligula sed maximus. Sed semper eu ex et eleifend. Sed id ornare nulla.
Ut pretium, sapien nec maximus pulvinar, arcu magna consequat nibh, at viverra ligula odio non urna. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse non nisi quis felis tempus aliquam a id nulla. Vivamus orci neque, fermentum non facilisis sed, consectetur vel erat. Morbi eu massa eu erat tincidunt tempor sit amet eget mi. Duis hendrerit vel est a volutpat. Duis vel nibh magna. Nunc maximus a tortor ut fermentum. Donec in urna luctus, euismod mauris et, euismod risus. Duis pretium tempor imperdiet. In consequat mauris quis turpis placerat sagittis et sit amet sem. Sed euismod aliquet orci ac placerat. Nunc gravida ex at leo dapibus, convallis tempus nulla dictum. Duis sollicitudin magna ex, in scelerisque nulla dapibus sed.
Sed vehicula cursus cursus. Praesent in lacus mollis metus eleifend tincidunt sit amet at velit. Pellentesque lacinia suscipit tellus, vel malesuada metus vestibulum vel. Morbi at velit consectetur, dictum erat ut, luctus urna. Fusce maximus feugiat mi, sed posuere velit congue eu. Proin commodo consequat gravida. Etiam eget facilisis diam. Suspendisse orci lorem, feugiat sit amet viverra quis, vehicula nec nibh. Etiam ut ipsum erat. Aliquam dictum turpis id enim molestie pulvinar. Sed et massa a lectus volutpat feugiat. Cras nec sagittis elit. Cras sed viverra eros.
Suspendisse rhoncus quam mauris, at posuere sem blandit a. Ut laoreet ullamcorper elit ut elementum. Sed magna augue, luctus non tristique vitae, fringilla sit amet justo. Integer euismod nunc tortor, vel elementum purus placerat vel. Etiam id diam mattis, bibendum augue vitae, porttitor mi. Proin id finibus nunc. Morbi in sodales mi. Nam facilisis ac felis et ultricies. Proin lacinia, urna et tempor interdum, purus purus consequat leo, vitae placerat risus odio vel tellus. Nullam eu lacus cursus, aliquam ex in, consequat lorem. Sed venenatis pretium placerat. Donec aliquam consequat nibh id consequat. Donec quis lorem eleifend, fermentum tellus eu, bibendum ipsum.
Morbi placerat lectus nec eros vestibulum dictum. Nullam sed aliquam enim. Etiam a condimentum massa. Vivamus vulputate semper est vitae rhoncus. Donec malesuada, dui eu consectetur blandit, arcu sapien efficitur magna, quis dapibus justo ante quis dolor. Proin ut lorem eget sapien scelerisque suscipit. Sed efficitur consequat mauris ac condimentum. Suspendisse dictum elementum mi a egestas. Duis in gravida erat. Pellentesque facilisis leo id mi scelerisque sodales.
Nam a purus sollicitudin, porttitor urna eget, venenatis nisi. Integer nunc purus, vehicula ac enim non, vestibulum lacinia sapien. Donec dictum lectus ac diam elementum tincidunt. Aenean gravida ultrices urna eu iaculis. Nullam luctus dui in felis bibendum varius. Etiam facilisis mi quis lacus efficitur egestas. Nullam dignissim semper elit, at tristique purus. In hac habitasse platea dictumst. Phasellus mollis lacus ut urna ornare interdum. In ut elementum ligula. Quisque ipsum purus, facilisis quis massa ac, volutpat sagittis massa. Etiam imperdiet, nisl in hendrerit aliquet, purus purus facilisis felis, quis egestas risus mauris at neque. Maecenas maximus tristique pellentesque.
Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer vehicula vel neque a interdum. Donec arcu nibh, viverra vulputate lobortis at, ultrices ac eros. Cras at pharetra purus. Maecenas iaculis elementum nulla ut faucibus. Vestibulum nec orci quis nisi tempor semper. In vehicula, felis ut porta pulvinar, massa dui accumsan tellus, in ultrices risus mi id libero. Sed non nulla quis erat facilisis cursus id nec velit. Curabitur scelerisque augue sit amet congue iaculis. Mauris tincidunt scelerisque posuere. Fusce facilisis ipsum sed quam finibus, eget luctus dolor maximus. Fusce dapibus iaculis convallis. Cras neque eros, pulvinar in vehicula eu, condimentum id ante. Proin sit amet arcu non sapien congue consequat nec quis justo. Vestibulum sit amet turpis eu turpis faucibus viverra vel nec ex.
Morbi tellus mi, consectetur non mi quis, hendrerit interdum nisl. Praesent ut fringilla augue. Mauris ut diam eget dolor tincidunt vehicula eu non ipsum. In hac habitasse platea dictumst. Aliquam sollicitudin vitae tortor vitae ornare. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas erat diam, suscipit vitae mauris in, tristique ultricies massa. Cras ac metus pulvinar, convallis quam et, tempus turpis. Curabitur in porta sapien. Maecenas tincidunt rhoncus libero, quis interdum dolor. In quam lacus, tincidunt sit amet urna in, faucibus blandit nisl.
In pharetra nunc aliquet, fermentum arcu sit amet, venenatis odio. Nulla venenatis purus sem, vel faucibus neque hendrerit sed. Ut vitae dolor et elit mollis tincidunt id in lorem. Etiam placerat, enim a lobortis convallis, turpis quam sollicitudin sapien, non imperdiet lectus ligula ut lectus. Proin sit amet finibus est, at facilisis leo. Suspendisse quis ipsum eget elit condimentum maximus. Proin est arcu, tempus sed libero sed, rutrum pharetra arcu. In est libero, tristique vel lacus quis, finibus lobortis est. Etiam maximus orci in tellus lobortis viverra eu quis tortor.
Vivamus posuere sollicitudin odio at pulvinar. Aenean a ornare sapien. Mauris consequat tempus lorem id iaculis. Aenean iaculis purus quis suscipit scelerisque. Pellentesque tristique congue libero, porttitor pulvinar justo ullamcorper vitae. Vivamus bibendum egestas turpis sed viverra. Mauris elementum sapien in enim luctus dignissim. Nulla vel erat ipsum. Quisque venenatis est lorem, eget luctus augue sodales eu.
Sed a magna non magna blandit tristique sed quis augue. Donec lobortis tempus dui vel aliquam. Aliquam leo metus, malesuada in interdum sed, ultricies sit amet eros. Integer luctus ante vel arcu volutpat, vel rhoncus quam commodo. Morbi dapibus eleifend nisl, a vehicula lacus tincidunt vel. Ut molestie fermentum orci, eget eleifend nisi aliquet imperdiet. Vivamus aliquet blandit lectus vitae tincidunt. Donec maximus augue sed ex euismod convallis.
Cras ultrices orci erat, lobortis mollis est pellentesque ut. Morbi convallis consequat massa, vitae interdum lorem. Sed libero velit, commodo a varius eu, convallis in leo. Phasellus quis justo venenatis, semper mi sit amet, gravida mi. In pharetra ipsum a dolor rhoncus accumsan. Sed diam velit, tempus non massa ut, semper pellentesque sem. Suspendisse sagittis, nulla sed sagittis blandit, dolor erat lobortis sem, et elementum mi urna at dui. Duis felis lacus, malesuada sit amet enim ac, egestas malesuada orci. Duis iaculis erat quam, vel fermentum dui pretium quis. Praesent a lectus sem. Nullam est nulla, convallis at sodales et, sodales at nisi."""

PATH_TO_VENC = os.path.expanduser("~")+"/.local/bin/venc"

def clear_venc_blog():
    try:
        shutil.rmtree("venc-benchmark")
        
    except FileNotFoundError:
        pass

def gen_venc_entry():
    ID = CONTEXT["ENTRY_ID_COUNTER"]
    entry  = "title: benchmark entry "+str(ID)+'\n'
    entry += "authors: VenC Comparative Benchmark\n"
    entry += "categories: "+CONTEXT["SAMPLE_CATEGORIES"][CONTEXT["CATEGORY_INDEX"]]+'\n'
    entry += "tags: ''"
    entry += "---VENC-BEGIN-PREVIEW---\n"
    entry += "---VENC-END-PREVIEW---\n"+(LOREM_IPSUM*CONTEXT["CONTENT_SIZE_MULTIPLIER"])
    date = datetime.datetime.fromtimestamp(CONTEXT["DATETIME"])
    entry_date = str(date.month)+'-'+str(date.day)+'-'+str(date.year)+'-'+str(date.hour)+'-'+str(date.minute)
    output_filename = str(ID)+"__"+entry_date+"__"+"benchmark_entry_"+str(ID)
    open("venc-benchmark/entries/"+output_filename, 'w').write(entry)

def get_command_output(argv):       
    output = subprocess.Popen(argv, STDOUT=subprocess.PIPE, stderr= DEVNULL if not "-v" in sys.argv else sys.stderr)
    output.wait()
    return output.stdout.read().decode("utf-8").strip()

def init_entries():
    for i in range(0, 1000):
        gen_venc_entry()
        update_context()

def init_venc_blog():
    from venc3.commands.new import new_blog
    from venc3 import venc_version
    print("Benckmark VenC", venc_version)
    ENVIRONMENT["VenC"] = venc_version
    clear_venc_blog()
    new_blog(["venc-benchmark"])
    from distutils.dir_util import copy_tree
    copy_tree("venc-benchmark-config", "venc-benchmark")

def set_python_version():
    proc = subprocess.Popen("cat /proc/cpuinfo | grep \"model name\" | head -1 | cut -d ':' -f 2", shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, encoding = 'utf8')
    ENVIRONMENT["CPU"] = proc.stdout.read().strip()
    ENVIRONMENT["Python"] = sys.version.replace('\n', '')
    
def update_context():
    global CONTEXT
    CONTEXT["ENTRY_ID_COUNTER"] += 1
    CONTEXT["DATETIME"] += 86400
    CONTEXT["CONTENT_SIZE_MULTIPLIER"] = random.randint(0,5)
    CONTEXT["CATEGORY_INDEX"] = random.randint(0, 8)

set_python_version()
init_venc_blog()
init_entries()
