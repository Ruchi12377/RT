const int second = 304; //1周分のステッピングモーター回転の数

//X stepping moter drive
const int PULX = 7;
const int DIRX = 6;
const int ENAX = 5;

//Y stepping moter drive
const int PULY = 10;
const int DIRY = 11;
const int ENAY = 12;
//ここまで定数

//設定値
bool initialized;
//x,yの黒板の大きさ
int xSize;
int ySize;
//押す距離
int zDepth;

int currentX;
int currentY;
int currentZ;
//ここまで変数

void setup() {
  pinMode (PULX, OUTPUT);
  pinMode (DIRX, OUTPUT);
  pinMode (ENAX, OUTPUT);

  pinMode (PULY, OUTPUT);
  pinMode (DIRY, OUTPUT);
  pinMode (ENAY, OUTPUT);

  // シリアル通信を初期化する。通信速度は9600bps
  Serial.begin( 9600 );
}

int split(String data, char delimiter, String *dst){
    int index = 0;
    int arraySize = (sizeof(data)/sizeof((data)[0]));  
    int datalength = data.length();
    for (int i = 0; i < datalength; i++) {
        char tmp = data.charAt(i);
        if ( tmp == delimiter ) {
            index++;
            if ( index > (arraySize - 1)) return -1;
        }
        else dst[index] += tmp;
    }
    return (index + 1);
}

void loop(){
  String cmd = Serial.readString();
  if(cmd != ""){
    String cmds[10] = {"\0"}; // 分割された文字列を格納する配列 
    // 分割数 = 分割処理(文字列, 区切り文字, 配列) 
    int index = split(cmd, ' ', cmds);

    if(cmds[0].equals("rot")){
      long r = cmds[1].toInt();
      Serial.println(r);
      rotate(r, PULX, DIRX, ENAX);
      Serial.println("rotate!");
    }
  }
}


//rotate stepping moter
void rotate(long angle, int pul, int dir, int ena){
  if(angle == 0) return;
  
  bool gen = angle > 0;

  Serial.println(angle * 1000);
  //rotate
  for (int i=0; i < abs(angle * 1000); i++){
    //if amount of rotation is generate than 0
    if(gen){
      //forward rotate
      digitalWrite(dir, HIGH);
    }
    //if amount of rotation were less than 0
    else{
      //backward rotate
      digitalWrite(dir, LOW);
    }
    
    digitalWrite(ena,HIGH);
    digitalWrite(pul,HIGH);
    delayMicroseconds(50);
    digitalWrite(pul,LOW);
    delayMicroseconds(50);
  }
  
  //回転後の事後処理
  //これをしないと、ノイズが発生してしまう
  digitalWrite(pul,LOW);
  digitalWrite(dir,LOW);
  digitalWrite(ena,LOW);
}

#pragma Serial call
//大文字で始まる関数はシリアル通信を用いて呼び出す
//それぞれの大きさを引数に取る
//serial call
void Init(int x, int y, int z){
  //初期化した
  initialized = true;
  xSize = x;
  ySize = y;
  zDepth = z;

  //初期の座標を0にする(一応)
  currentX = 0;
  currentY = 0;
  currentZ = 0;
}

//初期位置に戻す
void Reset(){

}

//serial call
void MoveX(){
  if(initialized == false) return;
}

//serial call
void MoveY(){
  if(initialized == false) return;
}

//serial call
//押すか押さないか
void MoveZ(){
  if(initialized == false) return;
}

void nonInitializeErro(){
  Serial.println("please call Init() before call Move~()");
}
#pragma endregion
