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
      long z = cmds[1].toInt();
      Serial.println("z test");
      rotate(z, PULZ, DIRZ, ENAZ);
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
  if (initialized == false) return;

  targetXRate = constrain(targetXRate, 0, 100);
  int targetX = xSize * targetXRate / 100;
  int currentX = xSize * currentXRate / 100;
  //範囲外に行ってしまわないように
  int minX = -currentX;
  int maxX = xSize - currentX;
  int moveDiff = targetX - currentX;
  moveDiff = constrain(moveDiff, minX, maxX);
  rotate(moveDiff, PULX, DIRX, ENAX);
  currentXRate = targetXRate;
}

//serial call
//targetYRate 0~100
void MoveY(int targetYRate) {
  if (initialized == false) return;

  targetYRate = constrain(targetYRate, 0, 100);
  int targetY = ySize * targetYRate / 100;
  int currentY = ySize * currentYRate / 100;
  //範囲外に行ってしまわないように
  int minY = -currentY;
  int maxY = ySize - currentY;
  int moveDiff = targetY - currentY;
  moveDiff = constrain(moveDiff, minY, maxY);
  rotate(moveDiff, PULY, DIRY, ENAY);
  currentYRate = targetY;
}

//serial call
//押すか押さないか
//targetZRate 0~100
void MoveZ(int targetZRate) {
  if (initialized == false) return;

  targetZRate = constrain(targetZRate, 0, 100);
  int targetZ = zDepth * targetZRate / 100;
  int currentZ = zDepth * currentZRate / 100;
  //範囲外に行ってしまわないように
  int minZ = -currentZ;
  int maxZ = zDepth - currentZ;
  int moveDiff = targetZ - currentZ;
  moveDiff = constrain(moveDiff, minZ, maxZ);
  Serial.println(moveDiff);
  rotate(moveDiff, PULZ, DIRZ, ENAZ);
  currentZRate = targetZ;
}

void nonInitializeErro() {
  Serial.println("please call Init() before call Move~()");
}
#pragma endregion
