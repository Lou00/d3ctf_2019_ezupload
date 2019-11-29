<?php
class dir{
    public $userdir;
    public $url;
    public $filename;
    public function __construct($url,$filename) {
        $this->userdir = "upload/" . md5($_SERVER["REMOTE_ADDR"]);
        $this->url = $url;
        $this->filename  =  $filename;
        if (!file_exists($this->userdir)) {
            mkdir($this->userdir, 0777, true);
        }
    }
    public function checkdir(){
        if ($this->userdir != "upload/" . md5($_SERVER["REMOTE_ADDR"])) {
            die('hacker!!!');
        }
    }
    public function checkurl(){
        $r = parse_url($this->url);
        if (!isset($r['scheme']) || preg_match("/file|php/i",$r['scheme'])){
            die('hacker!!!');
        }
    }
    public function checkext(){
        if (stristr($this->filename,'..')){
            die('hacker!!!');
        }
        if (stristr($this->filename,'/')){
            die('hacker!!!');
        }
        $ext = substr($this->filename, strrpos($this->filename, ".") + 1);
        if (preg_match("/ph/i", $ext)){
            die('hacker!!!');
        }
    }
    public function upload(){
        $this->checkdir();
        $this->checkurl();
        $this->checkext();
        $content = file_get_contents($this->url,NULL,NULL,0,2048);
        if (preg_match("/\<\?|value|on|type|flag|auto|set|\\\\/i", $content)){
            die('hacker!!!');
        }
        file_put_contents($this->userdir."/".$this->filename,$content);
    }
    public function remove(){
        $this->checkdir();
        $this->checkext();
        if (file_exists($this->userdir."/".$this->filename)){
            unlink($this->userdir."/".$this->filename);
        }
    }
    public function count($dir) {
        if ($dir === ''){
            $num = count(scandir($this->userdir)) - 2;
        }
        else {
            $num = count(scandir($dir)) - 2;
        }
        if($num > 0) {
            return "you have $num files";
        }
        else{
            return "you don't have file";
        }
    }
    public function __toString() {
        return implode(" ",scandir(__DIR__."/".$this->userdir));
    }
    public function __destruct() {
        $string = "your file in : ".$this->userdir;
        file_put_contents($this->filename.".txt", $string);
        echo $string;
    }
}

if (!isset($_POST['action']) || !isset($_POST['url']) || !isset($_POST['filename'])){
    highlight_file(__FILE__);
    die();
}

$dir = new dir($_POST['url'],$_POST['filename']);
if($_POST['action'] === "upload") {
    $dir->upload();
}
elseif ($_POST['action'] === "remove") {
    $dir->remove();
}
elseif ($_POST['action'] === "count") {
    if (!isset($_POST['dir'])){
        echo $dir->count('');
    } else {
        echo $dir->count($_POST['dir']);
    }
}
