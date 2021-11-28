const int around = 1600; //1周分のステッピングモーター回転の数
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
int currentY;
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

void loop(){
}


//rotate stepping moter
void rotate(int angle, int pul, int dir, int ena){
  if(angle == 0) return;
  
  //calculate amount of rotation
  int amount = floor((float)around / (float)360  * angle);
  
  //rotate
  for (int i=0; i < abs(amount); i++){
    //if amount of rotation is generate than 0
    if(amount > 0){
      //forward rotate
      digitalWrite(DIR, HIGH);
    }
    //if amount of rotation were less than 0
    else if(amount < 0){
      //backward rotate
      digitalWrite(DIR, LOW);
    }
    
    digitalWrite(ENA,HIGH);
    digitalWrite(PUL,HIGH);
    delayMicroseconds(100);
    digitalWrite(PUL,LOW);
    delayMicroseconds(100);
  }
  
  //回転後の事後処理
  //これをしないと、ノイズが発生してしまう
  digitalWrite(PUL,LOW);
  digitalWrite(DIR,LOW);
  digitalWrite(ENA,LOW);
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
