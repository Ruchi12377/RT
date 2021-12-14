const int second = 304; //1周分のステッピングモーター回転の数

//X stepping moter drive
const int PULX = 7;
const int DIRX = 6;
const int ENAX = 5;

//Y stepping moter drive
const int PULY = 10;
const int DIRY = 9;
const int ENAY = 8;

//Z stepping moter drive
//Temp
const int PULZ = 13;
const int DIRZ = 12;
const int ENAZ = 11;
//ここまで定数

//設定値
bool initialized;
//x,yの黒板の大きさ
int xSize;
int ySize;
//押す距離
int zDepth;

int currentXRate;
int currentYRate;
int currentZRate;
//ここまで変数

void setup() {
  pinMode (PULX, OUTPUT);
  pinMode (DIRX, OUTPUT);
  pinMode (ENAX, OUTPUT);

  pinMode (PULY, OUTPUT);
  pinMode (DIRY, OUTPUT);
  pinMode (ENAY, OUTPUT);

  pinMode (PULZ, OUTPUT);
  pinMode (DIRZ, OUTPUT);
  pinMode (ENAZ, OUTPUT);

  // シリアル通信を初期化する。通信速度は9600bps
  Serial.begin(9600);
}

int split(String data, char delimiter, String *dst) {
  int index = 0;
  int arraySize = (sizeof(data) / sizeof((data)[0]));
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

void loop() {
  String cmd = Serial.readString();
  if (cmd != "") {
    //分割された文字列を格納する配列
    //とりあえず引数は10(コマンド1と引数9で合計10)個で登録しておく
    String cmds[10] = {"\0"};
    //分割数 = 分割処理(文字列, 区切り文字, 配列)
    int index = split(cmd, ' ', cmds);

    //コマンド解析
    if(cmds[0].equals("init")){
      long x = cmds[1].toInt();
      long y = cmds[2].toInt();
      long z = cmds[3].toInt();
      Init(x, y, z);
    }else if(cmds[0].equals("reset")){
      Reset();
    }else if(cmds[0].equals("moveX")){
      long xRate = cmds[1].toInt();
      MoveX(xRate);
    }else if(cmds[0].equals("moveY")){
      long yRate = cmds[1].toInt();
      MoveY(yRate);
    }else if(cmds[0].equals("moveZ")){
      long zRate = cmds[1].toInt();
      Serial.println("z");
      MoveZ(zRate);
    }else if(cmds[0].equals("rot")){
      long index = cmds[1].toInt();
      long r = cmds[2].toInt();
      if(index == 0){
        Serial.println("x test");
        rotate(r, PULX, DIRX, ENAX);
      }else if(index == 1){
        Serial.println("y test");
        rotate(r, PULY, DIRY, ENAY);
      }else if(index == 2){
        Serial.println("z test");
        rotate(r, PULZ, DIRZ, ENAZ);
      }
    }
  }
}


//rotate stepping moter
void rotate(long angle, int pul, int dir, int ena) {
  if (angle == 0) return;

  bool gen = angle > 0;

  Serial.println(angle * 1000);
  //rotate
  for (int i = 0; i < abs(angle * 1000); i++) {
    //if amount of rotation is generate than 0
    if (gen) {
      //forward rotate
      digitalWrite(dir, HIGH);
    }
    //if amount of rotation were less than 0
    else {
      //backward rotate
      digitalWrite(dir, LOW);
    }

    digitalWrite(ena, HIGH);
    digitalWrite(pul, HIGH);
    delayMicroseconds(50);
    digitalWrite(pul, LOW);
    delayMicroseconds(50);
  }

  //回転後の事後処理
  //これをしないと、ノイズが発生してしまう
  digitalWrite(pul, LOW);
  digitalWrite(dir, LOW);
  digitalWrite(ena, LOW);
}

#pragma Serial call
//大文字で始まる関数はシリアル通信を用いて呼び出す
//serial call
void Init(int x, int y, int z) {
  //初期化した
  initialized = true;
  xSize = x;
  ySize = y;
  zDepth = z;

  //初期の座標を0にする(一応)
  currentXRate = 0;
  currentYRate = 0;
  currentZRate = 0;

  Serial.println("Init");
}

//初期位置に戻す
void Reset() {
  MoveX(0);
  MoveY(0);
  MoveZ(0);
  Serial.println("Reset");
}

//serial call
//targetXRate 0~100
void MoveX(int targetXRate) {
  Serial.println("MoveX");
  currentXRate = sharedMove(targetXRate, currentXRate, xSize, PULX, DIRX, ENAX);
}

//serial call
//targetYRate 0~100
void MoveY(int targetYRate) {
  Serial.println("MoveY");
  currentYRate = sharedMove(targetYRate, currentYRate, ySize, PULY, DIRY, ENAY);
}

//serial call
//押すか押さないか
//targetZRate 0~100
void MoveZ(int targetZRate) {
  Serial.println("MoveZ");
  currentZRate = sharedMove(targetZRate, currentZRate, zDepth, PULZ, DIRZ, ENAZ);
}

void nonInitializeError() {
  Serial.println("please call Init() before call Move~()");
}

int sharedMove(int targetRate, int currentRate, int boardSize, int pul, int dir, int ena){
  if (initialized == false) {
    nonInitializeError();
    return currentRate;
  }

  targetRate = constrain(targetRate, 0, 100);
  int target = boardSize * targetRate / 100;
  int current = boardSize * currentRate / 100;
  //範囲外に行ってしまわないように
  int moveDiff = target - current;
  moveDiff = constrain(moveDiff, -current, boardSize - current);
  Serial.println(moveDiff);
  rotate(moveDiff, pul, dir, ena);
  currentRate = target;
  return currentRate;
}
#pragma endregion
